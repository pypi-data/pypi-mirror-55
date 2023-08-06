#!python
# ------------------------------------------------------------------------------
#
# Copyright (c) 2019 Jonathan Sambrook and Codethink Ltd.
#
#    This file is part of Topplot.
#
#    Topplot is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Topplot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Topplot.  If not, see <https://www.gnu.org/licenses/>.
#
# Topplot munges top logs in to graphs.
#
# Written for Python 3.7 and matplotlib
#
# ------------------------------------------------------------------------------

VERSION = "0.0.3"

# ------------------------------------------------------------------------------
#
# TODO:  'x)' indicates implemented/fixed
#        'W)' indicates (probably) won't fix
#        'L)' indicates problem with mpl (or other library) that might be looked upon favourably by upstream
#        '*)' indicates remains outstanding
#        '?)' indicates brain(storm|fart)
#
#       *) Make use of Pandas data manipulation capabilities.
#
#       *) Cache initial parsing since re-running with varying config is likely
#          Check whether this is worth the coin.
#
#       *) Refactor everything for efficiency
#
#       *) Refactor everything for maintainability
#
# ------------------------------------------------------------------------------

import argparse
import csv
import datetime as dt
from datetime import time
from io import StringIO
import numpy as np
import os
import pandas as pd
from pandas import Series
import re
import signal
import sys
import tempfile
import time

from topplot.graphs import Grapher, rcParams
from topplot.utils import die

# ------------------------------------------------------------------------------
# Convert HH:MM:SS to seconds

# Convert DD:HH:MM:SS to seconds (re based to flexibly handle optional day/hour/minutes)
def dhms_to_sec(text):
    m = re.match(
        "^((?P<d>\d+):){0,1}?((?P<h>\d+):){0,1}?((?P<m>\d+):){0,1}?(?P<s>\d\d)$", text
    )
    if m:
        groups = m.groupdict()
        d = int(groups["d"]) if groups["d"] else 0
        h = int(groups["h"]) if groups["h"] else 0
        m = int(groups["m"]) if groups["m"] else 0
        s = int(groups["s"])
        # print(f"{text} → d: {d}  h: {h}  m: {m}  s: {s}")
        return d * 24 * 3600 + h * 3600 + m * 60 + s
    else:
        die(f"'{text}' doesn't parse as a timestamp with format [[[D:]HH:]MM:]SS")


# ------------------------------------------------------------------------------
# Parse the command line

cpu_columns = ["user", "system", "nice", "idle", "wait", "hw_irq", "sw_irq"]
cpu_active_columns = ["user", "system", "nice", "hw_irq", "sw_irq"]
musthave_columns = ["%CPU", "COMMAND", "%MEM", "PID"]
has_cpu_column = False
has_cpu_rows = False
poi_acc_cpu_default = 10

parser = argparse.ArgumentParser(
    description="Munge data logged from the top utility in to graphs using GnuPlot.\nNote that Processes of Interest (POI) is a common-or-garden bucket, so however you select the processes, once they're in the bucket, they're just another process sloshing around in the bucket."
)

parser.add_argument(
    "-f",
    "--file",
    dest="toplog_filename",
    metavar="PATH",
    default="top.log",
    help="Name of the file to munge (default: top.log)",
)


parser.add_argument(
    "-s",
    "--start",
    dest="start_time",
    metavar="TIMESTAMP",
    help="Start with timestamp TIMESTAMP ([D:]HH:MM:SS or >[[[D:]H+:]M+:]SS where the prefix '>' indicates an offset from the earliest log entry)",
)

parser.add_argument(
    "-S",
    "--stop",
    dest="stop_time",
    metavar="TIMESTAMP",
    help="Stop  with timestamp TIMESTAMP ([D:]HH:MM:SS or (+|<)[[[D:]H+:]M+:]SS where the prefix '<'indicates an offset from the earliest log entry and the + prefix an offset from the starting entry's timestamp)",
)


parser.add_argument(
    "-c",
    "--acc-cpu",
    dest="poi_acc_cpu",
    metavar="N",
    nargs="?",
    type=int,
    const=poi_acc_cpu_default,
    help="Top N processes ranked by accumulated CPU use (default: 10)",
)

parser.add_argument(
    "-m",
    "--acc-mem",
    dest="poi_acc_mem",
    metavar="N",
    nargs="?",
    type=int,
    const=10,
    help="Top N processes ranked by accumulated MEM use (default: 10)",
)

parser.add_argument(
    "--peak-cpu",
    dest="poi_peak_cpu",
    metavar="N",
    nargs="?",
    type=int,
    const=10,
    help="Top N processes ranked by peak CPU use (default: 10)",
)

parser.add_argument(
    "--peak-mem",
    dest="poi_peak_mem",
    metavar="N",
    nargs="?",
    type=int,
    const=10,
    help="Top N processes ranked by peak MEM use (default: 10)",
)

parser.add_argument(
    "--pct-cpu",
    dest="poi_cpu",
    metavar="PCT",
    nargs="?",
    type=int,
    const=20,
    help="Any process using more than pct%% of memory will be graphed (default: 20)",
)

parser.add_argument(
    "--pct-mem",
    dest="poi_mem",
    metavar="PCT",
    nargs="?",
    type=int,
    const=3,
    help="Any process using more than pct%% of cpu will be graphed (default: 3)",
)


parser.add_argument(
    "--prio",
    dest="poi_prio",
    metavar="cmpPRIO",
    nargs="?",
    type=str,
    const="=RT",
    help="Any process with priority =, <=, >=, <, or > to PRIO (default: '=RT', note the prefixed comparison operator)",
)

parser.add_argument(
    "-C",
    "--only-proc-cpu",
    dest="include_process_mem",
    action="store_false",
    help="Don't plot processes' mem info",
)

parser.add_argument(
    "-M",
    "--only-proc-mem",
    dest="include_process_cpu",
    action="store_false",
    help="Don't plot processes' cpu info",
)


parser.add_argument(
    "--with-cpu-steal", dest="with_cpu_steal", help="Plot CPU steal data"
)


parser.add_argument(
    "poi_regex",
    metavar="REGEX",
    nargs="?",
    help="Python style regex for names of processes to graph",
)

parser.add_argument(
    "-I",
    "--ignore",
    dest="ignore_processes_regex",
    metavar="REGEX",
    help="Python style regex for names of processes to ignore",
)

parser.add_argument(
    "-i", dest="ignore_case", action="store_true", help="Use case insensitive matching"
)

parser.add_argument(
    "--dont-plot-cpu-lines",
    dest="plot_poi_cpu_lines",
    action="store_false",
    help="Don't display the individual processes' cpu usage. Implies --plot-cpu-sum",
)

parser.add_argument(
    "--dont-plot-mem-lines",
    dest="plot_poi_mem_lines",
    action="store_false",
    help="Don't display the individual processes' mem usage. Implies --plot-mem-sum",
)

parser.add_argument(
    "--plot-cpu-sum",
    dest="plot_poi_cpu_sum",
    action="store_true",
    help="Add a line for the sum of the ploted processes' cpu usage",
)

parser.add_argument(
    "--plot-mem-sum",
    dest="plot_poi_mem_sum",
    action="store_true",
    help="Add a line for the sum of the ploted processes' mem usage",
)

parser.add_argument(
    "-G",
    "--no-graph",
    dest="do_graph",
    action="store_false",
    help='Don\'t plot a graph. Useful with "-v" to get just get info from stdout',
)

parser.add_argument(
    "-g",
    "--graph",
    dest="which_graph",
    metavar="N",
    help="Display just one pane of the overview graph (1-4), the cpu data by core (C), or the poi data by core (c).",
)


parser.add_argument(
    "--rcParams",
    dest="display_rc_params",
    action="store_true",
    help="Display MatPlotLib rcParams and exit",
)


parser.add_argument(
    "-l",
    "--list",
    dest="list_processes",
    action="count",
    default=0,
    help="List the processes recorded in the top logs (-ll and -lll increase info)",
)

parser.add_argument(
    "-v",
    "--verbose",
    dest="verbosity",
    action="count",
    default=0,
    help="Increase verbosity to stdout (can be given multiple times)",
)

parser.add_argument(
    "-V", "--version", dest="version", action="version", version=VERSION
)


args = parser.parse_args()

args.version = VERSION

if args.display_rc_params:
    rcParams()
    sys.exit(0)

# Preflight checks and conversions

if not args.plot_poi_cpu_lines:
    args.plot_poi_cpu_sum = True

if not args.plot_poi_mem_lines:
    args.plot_poi_mem_sum = True

if not os.path.exists(args.toplog_filename):
    print(f"Can't see a file '{args.toplog_filename}'.")
    parser.print_usage()
    sys.exit(0)

if not args.include_process_cpu and not args.include_process_mem:
    die("Can't disable processing both processes' cpu and processes' mem")

if args.poi_prio:
    if args.poi_prio[0:1] not in "=<>":
        die("--prio argument must start with =, <=, >=, <, or >")

if args.start_time:
    check = re.compile("^([>0-9])")
    result = check.match(args.start_time[0:1])
    if not result:
        die(
            f"-s | --start : offset requires leading '>'. Dunno about {args.start_time[0:1]}"
        )

    if result.group(0) != ">":
        args.start_time = dhms_to_sec(args.start_time)

if args.stop_time:
    check = re.compile("^([<+0-9])")
    result = check.match(args.stop_time[0:1])
    if not result:
        die(
            f"-S | --stop : offset requires leading '+' or '<'. Dunno about {args.stop_time[0:1]}"
        )

    if result.group(0) != "+" and result.group(0) != "<":
        args.stop_time = dhms_to_sec(args.stop_time)

re_ignore_processes_regex = None

if args.ignore_processes_regex:
    flags = 0
    if args.ignore_case:
        flags = re.IGNORECASE

    re_ignore_processes_regex = re.compile(args.ignore_processes_regex, flags)

# ------------------------------------------------------------------------------
# Set up for the temporary data files

tmpdir_context_manager = tempfile.TemporaryDirectory()
tmpdir = tmpdir_context_manager.name

print(f"tmpdir: {tmpdir}")
cpu_data_filename = os.path.join(tmpdir, "cpu.data")
mem_data_filename = os.path.join(tmpdir, "mem.data")
task_data_filename = os.path.join(tmpdir, "task.data")
poi_combined_data_filename = os.path.join(tmpdir, "poi combined.data")
poi_data_filename = os.path.join(tmpdir, "poi.data")

# ------------------------------------------------------------------------------
# Processes of interest are identified by filter through a list of lambda functions
# and by creating top-N lists of cpu and mem values

processes_of_interest = {}
args.poi_categories = "categories: "  # subtitle of processes graph key
filterfoos = []


def filterfoo(command, pid, timestamp):
    for foo in filterfoos:
        if foo(command, pid, timestamp):
            return True
    return False


no_specific_interest = not (
    args.poi_cpu
    or args.poi_mem
    or args.poi_acc_cpu
    or args.poi_acc_mem
    or args.poi_peak_cpu
    or args.poi_peak_mem
    or args.poi_prio
    or args.poi_regex
)

if args.poi_mem:
    filterfoos.append(
        lambda command, pid, timestamp: float(
            processes[command][pid]["timestamps"][timestamp]["mem"]
        )
        > args.poi_mem
    )
    args.poi_categories += f"mem>{args.poi_mem} "

if args.poi_cpu:
    filterfoos.append(
        lambda command, pid, timestamp: float(
            processes[command][pid]["timestamps"][timestamp]["cpu"]
        )
        > args.poi_cpu
    )
    args.poi_categories += f"cpu>{args.poi_cpu} "

if args.poi_prio:
    if args.poi_prio[0:1] == "=" or args.poi_prio[0:2] == "==":
        i = 2 if args.poi_prio[0:2] == "==" else 1
        filterfoos.append(
            lambda command, pid, timestamp: processes[command][pid]["timestamps"][
                timestamp
            ]["priority"]
            == args.poi_prio[i:]
        )
    elif args.poi_prio[0:2] == "<=":
        filterfoos.append(
            lambda command, pid, timestamp: processes[command][pid]["timestamps"][
                timestamp
            ]["priority"]
            <= args.poi_prio[2:]
        )
    elif args.poi_prio[0:2] == ">=":
        filterfoos.append(
            lambda command, pid, timestamp: processes[command][pid]["timestamps"][
                timestamp
            ]["priority"]
            >= args.poi_prio[2:]
        )
    elif args.poi_prio[0:1] == "<":
        filterfoos.append(
            lambda command, pid, timestamp: processes[command][pid]["timestamps"][
                timestamp
            ]["priority"]
            < args.poi_prio[1:]
        )
    elif args.poi_prio[0:1] == ">":
        filterfoos.append(
            lambda command, pid, timestamp: processes[command][pid]["timestamps"][
                timestamp
            ]["priority"]
            > args.poi_prio[1:]
        )

    args.poi_categories += f"prio{args.poi_prio} "

if args.poi_regex:
    flags = 0
    if args.ignore_case:
        flags = re.IGNORECASE

    poi_regex = re.compile(args.poi_regex, flags)
    filterfoos.append(lambda command, pid, timestamp: poi_regex.match(command) != None)
    args.poi_categories += f"/{args.poi_regex}/{'i' if args.ignore_case else ''} "

if args.poi_acc_cpu or no_specific_interest:
    if not args.poi_acc_cpu:
        args.poi_acc_cpu = poi_acc_cpu_default

    args.poi_categories += f"cpu+{args.poi_acc_cpu} "

if args.poi_acc_mem:
    args.poi_categories += f"mem+{args.poi_acc_mem} "

if args.poi_peak_cpu:
    args.poi_categories += f"cpu^{args.poi_peak_cpu} "

if args.poi_peak_mem:
    args.poi_categories += f"mem^{args.poi_peak_mem} "

args.poi_categories = args.poi_categories.strip()

# ------------------------------------------------------------------------------
# Different versions of top require slightly different handling
#
# This is being handled by setting variables when what parses (!) for version
# detection occurs.
# This is performed by optionally passing tuples of ((var1_name, var1_value), (varN_name, varN_value))
# in with regexes to Re_Variants instances.

mem_in_kb = True
swap_in_kb = True


# Some versions of top have values that other don't
# So far it's either mem_cached or mem_available
mem_cached_or_available = "mem_cached"

# ------------------------------------------------------------------------------
# Since top has variance in output across versions, handle regex variants


class Re_Variants:
    def __init__(self, name, first_entry, var_substs=None):
        self.name = name
        self.re_arr = []
        self.re_arr.append(first_entry)
        self.index = 0
        self.var_substs = [var_substs]

    def append(self, re, var_substs=None):
        self.re_arr.append(re)
        self.var_substs.append(var_substs)

    def name(self):
        return self.name

    # Override match([..]) to fallback on regex variants
    def match(self, *args, **kwargs):
        i = self.index
        response = None

        while response == None and i < len(self.re_arr):
            response = self.re_arr[i].match(*args, **kwargs)
            if response == None:
                i += 1
            else:
                if i != self.index:
                    if self.var_substs[i] != None:
                        for (var_name, var_value) in self.var_substs[i]:
                            exec(f'{var_name}="{var_value}"', globals())

        if response != None:
            self.index = i

        return response

    def pattern(self):
        return [regex.pattern for regex in self.re_arr]

    # Delegate all other functionality to current regex
    def __getattr__(self, attr):
        print(f"attr: >{attr}<")
        return getattr(self.re_arr[self.index], attr)


# ------------------------------------------------------------------------------
# Precompile regexps
#
# The group names, i.e the "word" in (?P<word>pattern), are used later on as dictionary keys

# top - 06:40:46 up 0 min,  0 users,  load average: 20.84, 5.41, 1.83
re_top = re.compile(
    "^top - (?P<timestamp>[^ ]+) .*load average: (?P<load_average>[0-9.]+), .*"
)

# Tasks: 301 total,  23 running, 209 sleeping,   0 stopped,   0 zombie
re_tasks = re.compile(
    "^Tasks: (?P<task_total>[0-9]+) total, +(?P<task_running>[0-9]+) running, +(?P<task_sleeping>[0-9]+) sleeping, +(?P<task_stopped>[0-9]+) stopped, +(?P<task_zombie>[0-9]+) zombie"
)

# Cpu(s): 51.8%us, 28.7%sy,  0.5%ni, 13.9%id,  1.4%wa,  0.0%hi,  3.7%si,  0.0%st
re_cpu = re.compile(
    "^%?Cpu(\(s\)|(?P<cpu_id>[0-9]+) +): *(?P<cpu_user>[0-9.]*)[% ]us, *(?P<cpu_system>[0-9.]+)[% ]sy, *(?P<cpu_nice>[0-9.]+)[% ]ni, *(?P<cpu_idle>[0-9.]+)[% ]id, *(?P<cpu_wait>[0-9.]+)[% ]wa, *(?P<cpu_hw_irq>[0-9.]+)[% ]hi, *(?P<cpu_sw_irq>[0-9.]+)[% ]si, *(?P<cpu_steal>[0-9.]+)[% ]st"
)


# Mem:   4046364k total,  2847408k used,  1198956k free,    37528k buffers
re_mem = Re_Variants(
    "re_mem",
    re.compile(
        "^Mem: +(?P<mem_total>[0-9]+)k total, +(?P<mem_used>[0-9]+)k used, +(?P<mem_free>[0-9]+)k free, +(?P<mem_buffers>[0-9]+)k buffers"
    ),
)

# MiB Mem :  15653.4 total,   6178.4 free,   7285.0 used,   2189.9 buff/cache
re_mem.append(
    re.compile(
        "^MiB Mem : +(?P<mem_total>[.0-9]+) total, +(?P<mem_free>[.0-9]+) free, +(?P<mem_used>[.0-9]+) used, +(?P<mem_buffers>[.0-9]+) buff/cache"
    ),
    (("mem_in_kb", "False"),),
)

# Swap:  2047996k total,        0k used,  2047996k free,  1468792k cached
re_swap = Re_Variants(
    "re_swap",
    re.compile(
        "^Swap: +(?P<swap_total>[0-9]+)k total, +(?P<swap_used>[0-9]+)k used, +(?P<swap_free>[0-9]+)k free, +(?P<mem_cached>[0-9]+)k cached"
    ),
)

# MiB Swap:  15792.0 total,  10146.5 free,   5645.5 used.   7242.8 avail Mem
re_swap.append(
    re.compile(
        "^MiB Swap: +(?P<swap_total>[.0-9]+) total, +(?P<swap_free>[.0-9]+) free, +(?P<swap_used>[.0-9]+) used\. +(?P<mem_available>[.0-9]+) avail"
    ),
    (("mem_cached_or_available", "mem_available"), ("swap_in_kb", "False")),
)

# 2019-01-31 06:40:41:709
re_timestamp = re.compile("^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d:\d\d\d$")

re_process = None
re_process_header = None


def generate_re_process(line):
    columnheader_to_regex = {
        "%CPU": "(?P<cpu>[\d.]+)",
        "COMMAND": "(?P<commandline>(?P<command>[^ ]+).*)",
        "%MEM": "(?P<mem>[\d.]+[mg]?)",
        "NI": "(?P<nice>[\d-]+)",
        "P": "(?P<cpuid>\d+)",
        "PID": "(?P<pid>[0-9]+)",
        "PR": "(?P<priority>[\drRtT-]+)",
        "RES": "(?P<res>[\d.]+[mg]?)",
        "S": "(?P<state>[DIRSTtXZ]+)",
        "SHR": "(?P<shr>[\d.]+[mg]?)",
        "SWAP": "(?P<swap>[\d.]+[mg]?)",
        "TIME+": "(?P<time>[\d:.]+)",
        "USER": "(?P<user>[\w+-]+)",
        "VIRT": "(?P<virt>[\d.]+[mg]?)",
    }

    found = {}
    header_pattern = "^"
    process_pattern = "^"
    prespace = " *"

    line = line.rstrip("\n")

    for columnheader in re.findall("([^ ]+)", line):
        found[columnheader] = True
        header_pattern += prespace + columnheader.replace("+", "\\+")

        if columnheader in columnheader_to_regex:
            process_pattern += prespace + columnheader_to_regex[columnheader]
            prespace = " +"
        else:
            print(
                f">INFO: header line contains unhandled columnheader '{columnheader}'",
                file=sys.stderr,
            )
            process_pattern += prespace + "(?:[^ ]+)"

    header_pattern += "\s*$"
    process_pattern += "$"

    missing = []

    for musthave in musthave_columns:
        if musthave not in found:
            missing.append(musthave)

    if len(missing) > 0:
        print(
            f">ERR: missing essential process column(s): {missing}\nAborting.",
            file=sys.stderr,
        )
        sys.exit(1)

    return (
        header_pattern,
        re.compile(header_pattern),
        process_pattern,
        re.compile(process_pattern),
    )


# ------------------------------------------------------------------------------
# Main

top_entries = []
processes = {}

cpu_id = None
prev_secs = None
current_entry = None
first_secs = None

line_count = 0

with open(args.toplog_filename) as top_log:
    for line in top_log:
        line_count += 1
        line = line.rstrip()
        if 0 == len(line):
            continue

        #    print(f'{line_count}: len: {len(line)}', file=sys.stderr)

        top_line_match = re_top.match(line)

        if top_line_match:
            # starting a new entry, so stash previous one
            if current_entry:
                top_entries.append(current_entry)

            groupdict = top_line_match.groupdict()

            try:
                timestamp = groupdict["timestamp"]
            except:
                print(f"ERR: Expected a timestamp field at line {line_count} !?")
                next

            current_entry = groupdict

            # Handle start/stop times
            current_secs = dhms_to_sec(current_entry["timestamp"])

            if first_secs is None:
                first_secs = current_secs

            if prev_secs is not None:
                # Handle midnight wrapping
                # Not sure that
                while current_secs < prev_secs:
                    current_secs += 24 * 60 * 60

            # Convert to play nicely with matplotlib
            current_entry["timestamp"] = current_secs

            prev_secs = current_secs

            if args.start_time:
                if isinstance(args.start_time, str):
                    offset = dhms_to_sec(args.start_time[1:])

                    args.start_time = current_secs + offset

                if current_secs < args.start_time:
                    current_entry = None
                    continue

            if args.stop_time:
                if isinstance(args.stop_time, str):
                    offset = dhms_to_sec(args.stop_time[1:])

                    if args.stop_time[0:1] == "+":
                        args.stop_time = current_secs + offset

                    elif args.stop_time[0:1] == "<":
                        args.stop_time = first_secs + offset

                if current_secs >= args.stop_time:
                    current_entry = None
                    break

            # By default the header lines are of structure:
            #   Tasks:
            #   Cpu(s):
            #   Mem:
            #   Swap:
            #
            #   PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
            #
            # But Cpu can be aggregate or split out by core, and the process header line is mutable

            have_all_expected_header_lines = True
            pull_line = True
            for regex in [re_tasks, re_cpu, re_mem, re_swap]:
                if pull_line:
                    line = top_log.readline()
                pull_line = True

                if line:
                    line_count += 1
                    match = regex.match(line)
                    if match:
                        if regex is re_cpu:
                            cpu_id = match.group("cpu_id")
                            if cpu_id is not None:
                                # Handle split out CPU info
                                has_cpu_rows = True
                                pull_line = False
                                while match:
                                    line_count += 1
                                    cpu_id = match.group("cpu_id")
                                    temp_dict = match.groupdict()
                                    for key in [
                                        "user",
                                        "system",
                                        "nice",
                                        "idle",
                                        "wait",
                                        "hw_irq",
                                        "sw_irq",
                                        "steal",
                                    ]:
                                        temp_dict[f"cpu{cpu_id}_{key}"] = temp_dict.pop(
                                            "cpu_" + key
                                        )
                                    current_entry.update(temp_dict)
                                    line = top_log.readline()
                                    match = regex.match(line)
                                line_count -= 1
                            else:
                                current_entry.update(match.groupdict())
                        else:
                            current_entry.update(match.groupdict())
                    else:
                        have_all_expected_header_lines = False
                        print(
                            f">ERR: line {line_count}: >{line}<\n   : Unexpected match failure for {regex.pattern()}",
                            file=sys.stderr,
                        )
                else:
                    have_all_expected_header_lines = False

            if have_all_expected_header_lines:
                # Blank line
                line = top_log.readline()  # blank line
                if 1 != len(line):  # 1 for newline char
                    print(
                        f">ERR: line {line_count}: >{line}<\nExpected a blank line here.",
                        file=sys.stderr,
                    )

                # Process header line
                line = top_log.readline()
                if not re_process_header:
                    (
                        process_header_pattern,
                        re_process_header,
                        process_pattern,
                        re_process,
                    ) = generate_re_process(line)
                    if " +P " in re_process_header.pattern:
                        has_cpu_column = True
                if not re_process_header.match(line):
                    print(
                        f">ERR: line {line_count}: expected a process header line ({process_header_pattern}),\n got>{line}<",
                        file=sys.stderr,
                    )

                line_count += 2

        else:
            #  There won't be a current_entry if the start of the file is corrupted or we're skipping content until args.start_time
            if current_entry:
                # Expecting a process line at this point
                #       print(f'{line_count} : >{line}<', file=sys.stderr)
                process_match = re_process.match(line)

                if process_match:
                    groupdict = process_match.groupdict()

                    pid = process_match.group("pid")
                    del groupdict["pid"]

                    command = process_match.group("command")
                    del groupdict["command"]

                    # Just the basename please (but don't munge bracketed kernel processes)
                    if command[0:1] != "[" and command[0:7] != "kworker":
                        slash = command.rfind("/")
                        if slash > -1:
                            command = command[slash + 1 :]

                    if command == "" or len(command) == 0:
                        print("WARN: command empty")

                    # Skip this process if it matches the ignore regex and doesn't match the POI regex
                    if (
                        re_ignore_processes_regex
                        and re_ignore_processes_regex.match(command)
                    ) and not (poi_regex and poi_regex.match(command)):
                        continue

                    if command not in processes:
                        processes[command] = {}

                    if pid not in processes[command]:
                        processes[command][pid] = {}
                        processes[command][pid]["timestamps"] = {}

                        # Storing at this point obviously won't cope with processes that update their own ARGV[0]
                        processes[command][pid]["commandline"] = groupdict[
                            "commandline"
                        ]

                        if args.poi_acc_cpu:
                            processes[command][pid]["acc_cpu"] = 0
                        if args.poi_acc_mem:
                            processes[command][pid]["acc_mem"] = 0
                        if args.poi_peak_cpu:
                            processes[command][pid]["max_cpu"] = 0
                        if args.poi_peak_mem:
                            processes[command][pid]["max_mem"] = 0

                    # Bizarrely top can throw out reports where all processes' CPU column entries are negative
                    cpu_value = float(groupdict["cpu"])
                    if cpu_value < 0:
                        groupdict["cpu"] = str(cpu_value * -1)

                    if args.poi_acc_cpu:
                        processes[command][pid]["acc_cpu"] += float(groupdict["cpu"])

                    if args.poi_acc_mem:
                        processes[command][pid]["acc_mem"] += float(groupdict["mem"])

                    if (
                        args.poi_peak_cpu
                        and float(groupdict["cpu"]) > processes[command][pid]["max_cpu"]
                    ):
                        processes[command][pid]["max_cpu"] = float(groupdict["cpu"])

                    if (
                        args.poi_peak_mem
                        and float(groupdict["mem"]) > processes[command][pid]["max_mem"]
                    ):
                        processes[command][pid]["max_mem"] = float(groupdict["mem"])

                    processes[command][pid]["timestamps"][
                        current_entry["timestamp"]
                    ] = groupdict
                else:
                    if re_timestamp.match(line):
                        pass  # Dunno where these timestamps come from, but skipping them here is fine since they presage a new top entry
                        # They occassionally appear ectopically, and the error tracing has helped manually reconstruction
                    else:
                        print(
                            f">ERR: line {line_count}: expected process line ({process_pattern}),\ngot: >{line}<",
                            file=sys.stderr,
                        )

if current_entry:  # stash the final entry
    top_entries.append(current_entry)

# ------------------------------------------------------------------------------
# Early non-graphing output

if args.list_processes:
    for command in sorted(processes.keys()):
        pids = []
        for pid in sorted(processes[command].keys()):
            if args.list_processes >= 2:
                print(f"{command} [{pid}] {processes[command][pid]['commandline']}")
            else:
                pids.append(pid)

        if args.list_processes == 0:
            print(f"{command}")
        elif args.list_processes == 1:
            print(f"{command} x{len(pids)} {pids}")

    sys.exit(0)

# ------------------------------------------------------------------------------
# Parsing done. Let's munge! Start with munging top's header info


def write_datafile(filename, source, keys):
    with open(filename, "w") as data_file:
        # Header
        line = '"timestamp"'
        for key in keys:
            key = key.replace("_", " ")
            line = f'{line} "{key}"'
        data_file.write(line + "\n")

        # Data
        # First with an integrated timestamp
        if type(source) is list:
            for entry in source:
                added = False
                line = entry["timestamp"]
                for key in keys:
                    added = True
                    line = f"{line} {entry[key]}"
                if added:
                    data_file.write(line + "\n")
        elif type(source) is dict:
            # Otherwise the key *is* the timestamp
            for timestamp, columns in source.items():
                line = timestamp
                for key in keys:
                    line = f"{line} {columns[key]}"
                data_file.write(line + "\n")


cores = 1

if cpu_id is None:
    cpu_keys = [
        "load_average",
        "cpu_user",
        "cpu_system",
        "cpu_nice",
        "cpu_idle",
        "cpu_wait",
        "cpu_hw_irq",
        "cpu_sw_irq",
        "cpu_steal",
    ]
    ps = "ps 2"

else:
    cores = int(cpu_id) + 1
    cpu_keys = ["load_average"]
    column_index = 3
    columns = cpu_columns
    if args.with_cpu_steal:
        columns.append("steal")
    for i in range(0, cores):
        for column in columns:
            cpu_keys.append(f"cpu{i}_{column}")
            column_index += 1

write_datafile(cpu_data_filename, top_entries, cpu_keys)

mem_keys = ["mem_used", "mem_free", "mem_buffers", mem_cached_or_available, "swap_free"]

write_datafile(mem_data_filename, top_entries, mem_keys)

task_keys = ["task_running", "task_sleeping", "task_stopped", "task_zombie"]

write_datafile(task_data_filename, top_entries, task_keys)

# ------------------------------------------------------------------------------
# Munge Processes Of Interest (POI)

# Used to select third element of a tuple
def take_third(item):
    return item[2]


# Keep sorted lists of top N processes
class TopNList:
    def __init__(self, total, name):
        self.n = total
        self.name = name
        self.list = [("", "", 0)]

    def append(self, command, pid, value):
        if (len(self.list) < self.n) or (value > self.list[-1][2]):
            self.list.append((command, pid, value))
            self.list.sort(key=take_third, reverse=True)

            if len(self.list) > self.n:
                index = self.n - 1
                self.list = self.list[0:index]

    def complete(self):
        if args.verbosity > 0:
            print(f"Top {self.n} by {self.name}:")

        for command, pid, value in self.list:
            if command == "":
                print(f"WARN: Missing command in TopNList (?)")
            else:
                if command not in processes_of_interest:
                    processes_of_interest[command] = {}

                processes_of_interest[command][pid] = True

                if args.verbosity > 0:
                    print(f"  {command} [{pid}] {round(value,2)}")


# Keep track of top N lists on request
if args.poi_acc_cpu:
    acc_cpu = TopNList(args.poi_acc_cpu, "accumlated cpu")

if args.poi_acc_mem:
    acc_mem = TopNList(args.poi_acc_mem, "accumlated mem")

if args.poi_peak_cpu:
    peak_cpu = TopNList(args.poi_peak_cpu, "peak cpu")

if args.poi_peak_mem:
    peak_mem = TopNList(args.poi_peak_mem, "peak mem")

# Loop over all processes, keeping tabs on top N lists and filtering for POI
for command in processes.keys():
    for pid in processes[command].keys():
        # Update top-N lists if required
        if args.poi_acc_cpu:
            acc_cpu.append(command, pid, processes[command][pid]["acc_cpu"])

        if args.poi_acc_mem:
            acc_mem.append(command, pid, processes[command][pid]["acc_mem"])

        if args.poi_peak_cpu:
            peak_cpu.append(command, pid, processes[command][pid]["max_cpu"])

        if args.poi_peak_mem:
            peak_mem.append(command, pid, processes[command][pid]["max_mem"])

        # Run main filters
        for timestamp in processes[command][pid]["timestamps"].keys():
            if filterfoo(command, pid, timestamp):
                if command not in processes_of_interest:
                    if command == "":
                        print(f"ERR: adding empty command (?)")
                    processes_of_interest[command] = {}

                processes_of_interest[command][pid] = True
                continue

# Extract POI from top-N lists if required. Also dump info to stdout on request
if args.poi_acc_cpu:
    acc_cpu.complete()

if args.poi_acc_mem:
    acc_mem.complete()

if args.poi_peak_cpu:
    peak_cpu.complete()

if args.poi_peak_mem:
    peak_mem.complete()

if len(processes_of_interest) < 1:
    print(
        f"INFO: No processes of interest according to selection criteria: {args.poi_categories}",
        file=sys.stderr,
    )
    sys.exit(0)

# ------------------------------------------------------------------------------
# Munge data for processes of interest to its file(s)


class CpuFiles:
    def __init__(self, dir, cpus):
        self.cpus = cpus
        self.dir = dir

        self.files = []
        self.blockindexes = []
        self.poi_combined_data = {}
        self.registry = {}
        for core in range(0, cpus):
            self.files.append(open(f"{dir}/cpu{core}_process.data", "a"))
            self.blockindexes.append(-1)

    def close(self):
        if len(self.files):
            for f in self.files:
                f.close()
            self.files = []

            poi_keys = []
            for core in range(0, self.cpus):
                poi_keys.append(f"cpu{core} poi cpu")
                poi_keys.append(f"cpu{core} poi mem")

            for core in range(0, self.cpus):
                if args.plot_poi_cpu_sum or args.plot_poi_mem_sum:
                    # Generate data file
                    write_datafile(
                        poi_combined_data_filename, self.poi_combined_data, poi_keys
                    )

    #  def __del__(self):
    #    self.close()

    def increment_block_index(self, n):
        self.blockindexes[core] += 1

    def write(self, core, header, txt):
        if core not in self.registry:
            self.registry[core] = self.files[core]
            self.increment_block_index(core)
            self.files[core].write(header)

        self.files[core].write(txt)

    def seal_register(self):
        for cpu_id in self.registry.keys():
            self.registry[cpu_id].write("\n")
        self.registry = {}

    def init_poi_timestamp(self, timestamp):
        self.poi_combined_data[timestamp] = {}
        for i in range(0, self.cpus):
            self.poi_combined_data[timestamp][f"cpu{i} poi cpu"] = 0
            self.poi_combined_data[timestamp][f"cpu{i} poi mem"] = 0

    def add_poi_cpu(self, core, timestamp, value):
        if timestamp not in self.poi_combined_data:
            self.init_poi_timestamp(timestamp)
        self.poi_combined_data[timestamp][f"cpu{core} poi cpu"] += float(value)

    def add_poi_mem(self, core, timestamp, value):
        if timestamp not in self.poi_combined_data:
            self.init_poi_timestamp(timestamp)
        self.poi_combined_data[timestamp][f"cpu{core} poi mem"] += float(value)


data_by_core = CpuFiles(tmpdir, cores)

if has_cpu_rows:
    columns = cpu_columns

    if args.with_cpu_steal:
        columns.append("steal")

with open(poi_data_filename, "w") as poi_data:
    keys = ["cpu", "mem"]

    # Data
    block_index = -1

    for command in processes_of_interest.keys():
        if command == "":
            print("Warn: empty command (?)")
            continue

        pids = processes_of_interest[command].keys()

        for pid in pids:
            if not len(processes[command][pid]["timestamps"]):
                print(f"WARN: Unexpected lack of timestamps")
                continue

            block_index += 1

            if len(pids) > 1:
                qualified_command = f"{command}:{pid}"
            else:
                qualified_command = f"{command}"

            # Header
            line = "timestamp"
            for key in keys:
                key = key.replace("_", " ")
                line = f'{line} "{qualified_command} - {key}"'

            header = f"\n{line}\n"
            poi_data.write(header)

            # Data
            for timestamp in processes[command][pid]["timestamps"].keys():
                line = f"{timestamp}"
                for key in keys:
                    line = f"{line} {processes[command][pid]['timestamps'][timestamp][key]}"
                txt = line + "\n"
                poi_data.write(txt)
                if has_cpu_column:
                    core = int(
                        processes[command][pid]["timestamps"][timestamp]["cpuid"]
                    )

                    # Write data to split out file
                    data_by_core.write(core, header, txt)

                    # Update per core aggregate pile(s) as appropriate
                    if args.plot_poi_cpu_sum:
                        data_by_core.add_poi_cpu(
                            core,
                            timestamp,
                            float(
                                processes[command][pid]["timestamps"][timestamp]["cpu"]
                            ),
                        )

                    if args.plot_poi_mem_sum:
                        data_by_core.add_poi_mem(
                            core,
                            timestamp,
                            processes[command][pid]["timestamps"][timestamp]["mem"],
                        )

            poi_data.write("\n")

            if has_cpu_column:
                data_by_core.seal_register()

    data_by_core.close()


# ------------------------------------------------------------------------------
# Parsed, munged, and dumped: render the pretty pretties

if args.do_graph:

    # --------------------------------------------------------------------------

    def from_csv(f):
        df = pd.read_csv(f, sep=" ")
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df.set_index("timestamp", inplace=True)
        return df

    # --------------------------------------------------------------------------

    def munge_process_graph_data(datafile):
        df_mono = None
        with open(datafile) as poi_data:
            process_name = None
            lines = []
            re_starts_with_timestamp = re.compile('^timestamp "(.*) - cpu"')
            re_parse_data = re.compile("^(\d+) ([0-9.]+) ([0-9.]+)\n$")
            for line in poi_data.readlines():
                if line == "\n":
                    continue
                match = re_starts_with_timestamp.match(line)
                if match:
                    if process_name is not None:
                        # close off and process current set
                        csv = StringIO("".join(lines))
                        df = from_csv(csv)
                        if df_mono is None:
                            df_mono = df
                        else:
                            df_mono = pd.concat([df_mono, df], axis=1)

                    process_name = match.group(1)
                    lines = [line]
                else:
                    match = re_parse_data.match(line)
                    if match:
                        lines.append(line)
                    else:
                        print(
                            f"ERR: poi graphing Don't know what to do with line: '{line}'",
                            file=sys.stderr,
                        )

        return df_mono

    # --------------------------------------------------------------------------

    cpus_graph_title = "cpu data"
    tasks_graph_title = "task data"
    poi_graph_title = f"processes of interest (poi)\n{args.poi_categories}"
    mem_graph_title = "mem data"

    args.cpus_df = from_csv(cpu_data_filename)
    args.tasks_df = from_csv(task_data_filename)
    args.poi_df = munge_process_graph_data(poi_data_filename)
    args.mem_df = from_csv(mem_data_filename)

    # Add extra column(s) for summary CPU info
    ns = [""] if cores == 1 else range(cores)
    for n in ns:
        args.cpus_df[f"cpu{n} exec"] = (
            args.cpus_df[f"cpu{n} system"]
            + args.cpus_df[f"cpu{n} user"]
            + args.cpus_df[f"cpu{n} nice"]
        )

    # Prep the poi-by-core data
    args.core_dfs = []
    if cores > 1:
        for core in range(cores):
            args.core_dfs.append(
                munge_process_graph_data(f"{tmpdir}/cpu{core}_process.data")
            )

    # Awkward initialize sequence to allow graph_map to reference grapher functions
    graph_map = {}

    graphs = Grapher(graph_map, args, cores, mem_in_kb, mem_cached_or_available)

    # Order here determines display order in overview figure
    graph_map[poi_graph_title] = {
        "fn": graphs.graph_poi,
        "fig": None,
        "data": args.poi_df,
    }
    graph_map[cpus_graph_title] = {
        "fn": graphs.graph_cpus,
        "fig": None,
        "data": args.cpus_df,
    }
    graph_map[mem_graph_title] = {
        "fn": graphs.graph_mem,
        "fig": None,
        "data": args.mem_df,
    }
    graph_map[tasks_graph_title] = {
        "fn": graphs.graph_tasks,
        "fig": None,
        "data": args.tasks_df,
    }

    graphs.doit()

# ------------------------------------------------------------------------------
# vi: sw=2:ts=2:et:tw=0
