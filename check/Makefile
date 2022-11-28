# SPDX-License-Identifier: GPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022 Western Digital Corporation or its affiliates.

BINDIR = /usr/sbin

install:
	@echo "Installing zbd-check"
	@python3 -c 'from setup import install_checker; install_checker()' 
	@install --mode=755 -d ${BINDIR}
	@install --mode=755 zbd-check ${BINDIR}

uninstall:
	@echo "Uninstalling zbd-check"
	@python3 -c 'from setup import remove_checker; remove_checker()' 
