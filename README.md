Copyright (C) 2022 Western Digital Corporation or its affiliates.

# zbd-tools

*zbd-tools* is a tool set providing functions determining the availability
of zone block device support. These tools will help identify kernel
configurations and whether zone block device software packages are
installed.

## License

*zbd-tools* is distributed under the terms of the GNU General Public
License Version 3 or any later version (SPDX: *GPL-3.0-or-later*). A copy of
this license with *zbd-tools* copyright can be found in the file
[LICENSES/GPL-3.0-or-later.txt](LICENSES/GPL-3.0-or-later.txt).

If *zbd-tools* license files are missing, please see the GPL version 3 text
[here](https://www.gnu.org/licenses/gpl-3.0.html).

All source files in *zbd-tools* contain the GPL v3 license SPDX short
identifiers in place of the full license text.

```
SPDX-License-Identifier: GPL-3.0-or-later
```

Some files such as the `.gitignore` file are public domain specified by the
CC0 1.0 Universal (CC0 1.0) Public Domain Dedication. These files are
identified with the following SPDX header.

```
SPDX-License-Identifier: CC0-1.0
```

See the file [LICENSES/CC0-1.0.txt] for the full text of this license.

*zbd-tools* is distributed "as is," without technical support, and
WITHOUT ANY WARRANTY, without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

## Contributions and Bug Reports

Contributions are accepted as github pull requests or via email (`git
send-email` patches). Any problem may also be reported through github issues
page or by contacting:

* Tommy.McGee (tommy.mcgee@opensource.wdc.com)

PLEASE DO NOT SUBMIT CONFIDENTIAL INFORMATION OR INFORMATION SPECIFIC TO DRIVES
THAT ARE VENDOR SAMPLES OR NOT PUBLICLY AVAILABLE.

## Requirements

*zbd-tools* requires the following for installation and usage:
- make
- Python 3.0 or higher
- Python Package Manager (PIP), *if you have Python 3.4 or later
  PIP is already included*

**NOTE:** PIP is required only if *install from source* is not preferred.

## Installation 

To install and uninstall *zbd-tools* utilities, the project *Makefile* can be
used. Installation from the Python Package Index using the pip package manager
is also possible.

### Installation Using *make*

To install *zbd-tools* utilities execute the following command as root.

```
# make install
Installing zbd-check
```

To uninstall *zbd-tools* utilities execute the following command as root.

```
# make uninstall
Uninstalling zbd-check
```

### Installation Using *pip*

A PIP package for *zbd-tools* is provided by the Python Package Index (pypi).
For users who prefer not to install from the source tree using *make*, the
following command can be executed to fetch and install the
*zbd-tools* package from pypi.

```
$ pip install zbd-tools
Collecting zbd-tools
  Downloading zbd_tools-1.0-py3-none-any.whl (6.3 kB)
Installing collected packages: zbd-tools
Successfully installed zbd-tools-1.0
```

To uninstall *zbd-tools* from the system, use the following command.

```
$ pip uninstall zbd-tools
Found existing installation: zbd-tools 1.0
Uninstalling zbd-tools-1.0:
  Would remove:
    /usr/local/bin/zbd-check
    /usr/local/lib/python3.9/dist-packages/check/*
    /usr/local/lib/python3.9/dist-packages/zbd_tools-1.0.dist-info/*
Proceed (Y/n)? Y
Successfully uninstalled zbd-tools-1.0
```

## Usage

*zbd-tools* provides the *zbd-check* utility to check the zoned block device
features and applications supported by a Linux distribution.

### *zbd-check*

This utility allows checking a Linux distribution for zoned block device
support. Three different class of features are checked:
1. Kernel features: device types, device mapper targets and file systems support
   are checked.
2. User Libraries: *zbd-check* will list the installation status of user
   libraries related to zoned block devices.
3. User Applications: *zbd-check* will list the installation status of user
   applications related to zoned block devices.

*zbd-check* command line usage is displayed using the option "--help".

```
$ zbd-check --help
usage: zbd-check.py [-h] [--version]

options:
  -h, --help  show this help message and exit
  --version   show the version of zbd-check
```

The following shows an example output of the *zbd-check* utility executed on a
system running Fedora Linux 37.

```
$ zbd-check
------------------------------------------------------------------------
System Information:
------------------------------------------------------------------------
- Distribution: Fedora Linux 37 (Workstation Edition)
- Kernel Version: 6.0

------------------------------------------------------------------------
Kernel features:
------------------------------------------------------------------------
- Zoned block devices: supported
- Devices types:
    - SAS and SATA SMR hard-disks: supported
    - NVMe ZNS devices: supported
    - SCSI debug device ZBC emulation: supported
    - null_blk device zoned mode: supported
- file systems:
    - zonefs: supported
    - f2fs zoned mode: supported
    - btrfs zoned mode: supported
- Device mapper targets:
    - dm-linear: supported
    - dm-flakey: supported
    - dm-crypt: supported
    - dm-zoned: supported

------------------------------------------------------------------------
User Kernel zone management API:
------------------------------------------------------------------------
- Zone management kernel API header file: installed

------------------------------------------------------------------------
User Libraries:
------------------------------------------------------------------------
- libzbc:
    - Dynamic library installed, version 5.13.0
    - Static library installed
    - Development header files installed
- libzbd:
    - Dynamic library installed, version 2.0.2
    - Static library installed
    - Development header files installed
- libnvme:
    - Dynamic library installed, version 1.2
    - Static library not installed
    - Development header files installed

------------------------------------------------------------------------
User Applications:
------------------------------------------------------------------------
- fio: installed, version fio-3.29-7-g01686
- nvme-cli: installed, version 2.2.1
- dm-zoned-tools: installed, version 2.2.1
- zonefs-tools: installed, version 1.5.2
```
