#!/usr/bin/python3
# -*- coding: utf-8 -*-
#******************************************************************************
# ZYNTHIAN PROJECT: Zynthian LV2 Preset Converters
# 
# preset2lv2.py: Convert several native preset formats to LV2
# 
# Copyright (C) 2015-2019 Fernando Moyano <jofemodo@zynthian.org>
#
#******************************************************************************
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For a full copy of the GNU General Public License see the LICENSE.txt file.
# 
#******************************************************************************

import os
import sys
import logging
import argparse
from . import native2lv2

#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

def main(args=None):
	# Command-line options setup
	parser = argparse.ArgumentParser(description='Convert native presets to LV2.')
	parser.add_argument('format', help='Source preset format: synthv1, padthv1, dx7syx')
	parser.add_argument('path', help='Source preset dir or filepath')
	parser.add_argument('-b', '--bank', help='LV2 bank name')
	
	if args is None:
		args = parser.parse_args()

	try:
		# Import parser & Convert presets
		if args.format in ('synthv1', 'padthv1'):
			from . import v12lv2
			v12lv2.v12lv2(args)
		elif args.format=='dx7syx':
			from . import dx7syx2lv2
			dx7syx2lv2.dx7syx2lv2(args)
		else:
			raise native2lv2.p2lv2Exception("Source preset format must be one of the supported ones: synthv1, padthv1, dx7sysex")

	except native2lv2.p2lv2Exception as e:
		logging.error(e)
		exit(1)


if __name__ == '__main__':
	main()

#******************************************************************************
