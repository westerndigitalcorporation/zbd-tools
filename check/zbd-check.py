#!/usr/bin/python3
"""
* SPDX-License-Identifier: GPL-3.0-or-later
*
* Author: Tommy McGee (tommy.mcgee@opensource.wdc.com)
*
* Copyright (c) 2022 Western Digital Corporation or its affiliates.
*
* This script is used to determine if Zone Block Device is supported
"""
import glob
import argparse
import os
import sys
import shutil
sys.path.append('/usr/share/zbd-tools')
import helpers


def evaluate_using_modinfo():
    """ Review the current modinfo data.

    Check for null_blk and scsi_debug Zoned support
    """
    cmd_scsi_debug = os.popen('/sbin/modinfo scsi_debug | grep zbc')
    cmd_null_blk = os.popen('/sbin/modinfo null_blk | grep zoned:')
    scsi_debug_result = str(cmd_scsi_debug.read())
    null_blk_reslut = str(cmd_null_blk.read())
    check_scsi_debug_result = len(scsi_debug_result)
    check_null_blk_reslut = len(null_blk_reslut)
    if check_scsi_debug_result == 0:
        print(
            "\n *modinfo indicates current loaded kernel does not"
            " support zoned scsi_debug")
    else:
        pass
    if check_null_blk_reslut == 0:
        print(
            "\n *modinfo indicates current loaded kernel does not support"
            " zoned null_blk")
    else:
        pass


def evaluate_kernel_config_features():
    """ Gather the kernel features available.

    Then evaluate the statues and display the result to the user
    """
    # get the results from  the function that reads the config file
    search_kernel_config = dict(helpers.get_kernel_config_info())
    config_data_values = {
        "=m": "",
        "=y": "",
        "=n": "not ",
        " is not set": "not "
    }

    # Core support
    core_support = config_data_values.get(
              search_kernel_config.get('CONFIG_BLK_DEV_ZONED'),
              "not ")
    print("- Zoned block devices: " + core_support + "supported")
    if core_support == "not ":
        print("This system does not support zoned block devices.")
        print("Only applications using passthrough direct access")
        print("devices will work.")
        sys.exit()

    # Device types
    print("- Devices types:")
    print("    - SAS and SATA SMR hard-disks: supported")
    print("    - NVMe ZNS devices: " +
          config_data_values.get(
              search_kernel_config.get('CONFIG_BLK_DEV_NVME'),
              "not ") + "supported")
    print("    - SCSI debug device ZBC emulation: " +
          config_data_values.get(
              search_kernel_config.get('CONFIG_SCSI_DEBUG'),
              "not ") + "supported")
    print("    - null_blk device zoned mode: " +
          config_data_values.get(
              search_kernel_config.get('CONFIG_BLK_DEV_NULL_BLK'),
              "not ") + "supported")

    # File systems
    print("- file systems:")
    print("    - zonefs: " +
          config_data_values.get(
              search_kernel_config.get('CONFIG_ZONEFS_FS'),
              "not ") + "supported")
    print("    - f2fs zoned mode: " +
          config_data_values.get(
              search_kernel_config.get('CONFIG_F2FS_FS'),
              "not ") + "supported")
    print("    - btrfs zoned mode: " +
          config_data_values.get(
              search_kernel_config.get('CONFIG_BTRFS_FS'),
              "not ") + "supported")

    # Device mapper targets
    print("- Device mapper targets:")
    print("    - dm-linear: " +
          config_data_values.get(
              search_kernel_config.get('CONFIG_BLK_DEV_DM'),
              "not ") + "supported")
    print("    - dm-flakey: " +
          config_data_values.get(
              search_kernel_config.get('CONFIG_DM_FLAKEY'),
              "not ") + "supported")
    print("    - dm-crypt: " +
          config_data_values.get(
              search_kernel_config.get('CONFIG_DM_CRYPT'),
              "not ") + "supported")
    print("    - dm-zoned: " +
          config_data_values.get(
              search_kernel_config.get('CONFIG_DM_ZONED'),
              "not ") + "supported")


def evaluate_kernel_api():
    """blkzoned.h"""
    if os.path.exists('/usr/include/linux/blkzoned.h'):
        print("- Zone management kernel API header file: installed")
    else:
        print("- Zone management kernel API header: not installed")
        print("  WARNING: the kernel zone management API header file")
        print("           /usr/include/linux/blkzoned.h was not found."
              " User libraries")
        print("           and applications using the kernel zone management"
              " API will")
        print("           not compile correctly or will be compiled without"
              " zoned")
        print("           block device support.")


def evaluate_fio():
    """Determine if fio is installed"""
    if shutil.which("fio") is None:
        print("- fio: not installed")
        return

    ver = os.popen('fio --version | head -n 1')
    ver_text = str(ver.read())
    print("- fio: installed, version " + ver_text.rstrip())


def evaluate_nvme():
    """Determine if nvme-cli is installed"""
    if shutil.which("nvme") is None:
        print("- nvme-cli: not installed")
        return

    ver = os.popen('nvme --version | head -n 1 | cut -f3 -d" "')
    ver_text = str(ver.read())
    print("- nvme-cli: installed, version " + ver_text.rstrip())


def evaluate_dm_zoned_tools():
    """Determine if dm-zoned-tools is installed"""
    if shutil.which("dmzadm") is None:
        print("- dm-zoned-tools: not installed")
        return

    ver = os.popen('dmzadm --version')
    ver_text = str(ver.read())
    print("- dm-zoned-tools: installed, version " + ver_text.rstrip())


def evaluate_zonefs_tools():
    """Determine if zonefs-tools is installed"""
    if shutil.which("mkzonefs") is None:
        print("- zonefs-tools: not installed")
        return

    ver = os.popen('mkzonefs --version | head -n 1 | cut -f3 -d" "')
    ver_text = str(ver.read())
    print("- zonefs-tools: installed, version " + ver_text.rstrip())


def evaluate_packages():
    """Determine what packages are installed"""
    evaluate_fio()
    evaluate_nvme()
    evaluate_dm_zoned_tools()
    evaluate_zonefs_tools()


def evaluate_library_dynamic(lib):
    """Determine if a dynamic library is installed"""
    libso = lib + ".so"
    lib64path = r'/usr/lib64/' + libso + '.*'
    libpath = r'/usr/lib/' + libso + '.*'
    if os.path.exists("/usr/lib64/" + libso) or os.path.exists(
                      "/usr/lib/" + libso):
        ver = os.popen("pkg-config --modversion " + lib)
        ver_text = str(ver.read())
        print("    - Dynamic library installed, version " + ver_text.rstrip())
    elif glob.glob(lib64path) or glob.glob(libpath):
        print("    - Dynamic library installed")
    else:
        print("    - Dynamic library not installed")


def evaluate_library_static(lib):
    """Determine if a static library is installed"""
    liba = lib + ".a"
    if os.path.exists("/usr/lib64/" + liba) or os.path.exists(
                      "/usr/lib/" + liba):
        print("    - Static library installed")
    else:
        print("    - Static library not installed")


def evaluate_library_header(header):
    """Determine if a library development header files are installed"""
    if os.path.exists("/usr/include/" + header):
        print("    - Development header files installed")
    else:
        print("    - Development header files not installed")


def evaluate_libraries():
    """ Determine if libraries are installed """
    print("- libzbc:")
    evaluate_library_dynamic("libzbc")
    evaluate_library_static("libzbc")
    evaluate_library_header("libzbc/zbc.h")

    print("- libzbd:")
    evaluate_library_dynamic("libzbd")
    evaluate_library_static("libzbd")
    evaluate_library_header("libzbd/zbd.h")

    print("- libnvme:")
    evaluate_library_dynamic("libnvme")
    evaluate_library_static("libnvme")
    evaluate_library_header("libnvme.h")


def main():
    """Main Script execution"""
    # Get General Information about the host OS
    helpers.header("System Information:")
    os_release = dict(helpers.get_distro_general_information())
    pretty_name = os_release.get('PRETTY_NAME')
    print(f'- Distribution: {pretty_name}')
    helpers.get_kernel_general_information()
    print()

    # Get the kernel configuration information
    helpers.header("Kernel features:")
    evaluate_kernel_config_features()
    evaluate_using_modinfo()
    print()

    # User kernel API
    helpers.header("User Kernel zone management API:")
    evaluate_kernel_api()
    print()

    # Check to see what libraries exists
    helpers.header("User Libraries:")
    evaluate_libraries()
    print()

    # Check to see what packages exists
    helpers.header("User Applications:")
    evaluate_packages()
    print()


def version_information():
    """ Show the Version of the script"""
    print("1.0.1")


# CLI Arguments
cli_parser = argparse.ArgumentParser()
cli_parser.add_argument("--version", help="show the version of zbd-check",
                        action="store_true")
args = cli_parser.parse_args()
if args.version:
    version_information()
if len(sys.argv) == 1:
    main()
