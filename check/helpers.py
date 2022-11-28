"""
* SPDX-License-Identifier: GPL-3.0-or-later
*
* Author: Tommy McGee (tommy.mcgee@opensource.wdc.com)
*
* Copyright (c) 2022 Western Digital Corporation or its affiliates.
*
* This module is used to provide kernel configuration information
* to determine if Zone Block Support is available
"""
import ast
import gzip
import io
import os
import platform
import re
import sys

def header(title):
    """Print title in between 2 lines of 72 "-"
    """
    print(72*"-")
    print(title)
    print(72*"-")


def get_kernel_config_info():
    """Scan through specific modules for zone arguments
       using the the config file/s,
    """
    long_uname = platform.uname()
    printed_kernel_version = long_uname.release.strip('.#')
    file_path_check = r'/proc/config.gz'
    flag = os.path.isfile(file_path_check)
    if flag:
        file_name = '/proc/config.gz'
        gz_open_file = gzip.open(file_name, 'rb')
        open_file = io.TextIOWrapper(gz_open_file, encoding='utf-8')
    else:
        long_uname = platform.uname()
        printed_kernel_version = long_uname.release.strip('.#')
        file_name = '/boot/config-' + printed_kernel_version
        open_file = open(file_name)
    for _, line in enumerate(open_file):
        if line.startswith('#'):
            continue
        if txt_pattern := re.match(r'([0-9a-zA-Z_]+)(.*)', line):
            name, val = txt_pattern.groups()
            yield name, val


def get_distro_general_information():
    """
            Check the distro to use os-release for pretty name
            a) Checks to see if the file exits in either location
            b) When found strip the whitespace skip the commented lines
            c) Match the pattern that is being asked in the pretty name
               using regex
            d) if no matched are found show the unmatched lines.
    """
    try:
        file_name = '/etc/os-release'
        open_file = open(file_name)
    except FileNotFoundError:
        file_name = '/usr/lib/os-release'
        open_file = open(file_name)
    for each_line, line in enumerate(open_file):
        line = line.rstrip()
        if not line or line.startswith('#'):
            continue
        if txt_pattern := re.match(r'([a-zA-Z0-9_]+)=(.*)', line):
            name, val = txt_pattern.groups()
            if val and val[0] in '"\'':
                val = ast.literal_eval(val)
            yield name, val
        else:
            print(f'{file_name}:{each_line + 1}: bad line {line!r}',
                  file=sys.stderr)


def get_kernel_general_information():
    """ Kernel Version information formatted, and determine if the
        system kernel is supported.
    """
    characters = 4
    uname = platform.uname()
    kernel_version = uname.release
    format_kernel = (kernel_version[:characters]) + "#"
    display_kernel = (format_kernel).strip('.#')
    numeric_value = float(display_kernel)
    min_numeric_value = float('4.10')
    strdisplay = '- Kernel Version: ' + display_kernel
    if numeric_value >= min_numeric_value:
        print(
            strdisplay
        )
    else:
        print(
            strdisplay
        )
