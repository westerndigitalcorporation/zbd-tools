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

import os
import shutil
import stat

def install_checker():
    """
    Install the zbc-check script to usr/bin
    Then install this helper modules to /use/share/zbd-tools
    """
    path = '/usr/sbin/zbd-check'
    directory_name = 'zbd-tools'
    parent_path = '/usr/share'
    final_path = os.path.join(parent_path, directory_name)
    if os.path.exists(path):
        os.remove(path)
        if os.path.exists(final_path):
            shutil.rmtree(final_path)
    current_path_check_sh = os.getcwd() + '/zbd-check'
    current_path_check_py = os.getcwd() + '/zbd-check.py'
    current_path_helper = os.getcwd() + '/helpers.py'
    shutil.copy(current_path_check_sh, '/usr/sbin')
    os.chmod('/usr/sbin/zbd-check', stat.S_IXOTH)
    os.mkdir(final_path)
    shutil.copy(current_path_helper, '/usr/share/zbd-tools')
    shutil.copy(current_path_check_py, '/usr/share/zbd-tools')

def remove_checker():
    """Uninstall  zbd-checker and the helper module"""
    rm_path_checker = '/usr/sbin/zbd-check'
    rm_path_helper = '/usr/share/zbd-tools'
    if os.path.exists(rm_path_checker):
        os.remove(rm_path_checker)
        if os.path.exists(rm_path_helper):
            shutil.rmtree(rm_path_helper)
