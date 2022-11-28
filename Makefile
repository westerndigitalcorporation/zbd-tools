# SPDX-License-Identifier: GPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022 Western Digital Corporation or its affiliates.

TARGET = check

all: help

help:
	@echo "Run \"make install\" as root to install zbd-tools."
	@echo "Run \"make uninstall\" as root to uninstall zbd-tools."

install:
	@list='${TARGET}'; for d in $$list; do \
		cd $$d; make -s -f Makefile install; cd ..; \
	done

uninstall:
	@list='${TARGET}'; for d in $$list; do \
		cd $$d; make -s -f Makefile uninstall; cd ..; \
	done
