# -*- coding: utf-8 -*-
#******************************************************************************
# ZYNTHIAN PROJECT: Zynthian LV2 Preset Converters
# 
# v12lv2 class: Convert V1 (synthv1 & padthv1) native presets to LV2
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
import xml.etree.ElementTree as ET

from . import native2lv2

class v12lv2(native2lv2.native2lv2):

	def __init__(self, args):
		if args.format=='synthv1':
			self.plugin_name = 'synthv1'
			self.plugin_uri = 'http://synthv1.sourceforge.net/lv2'
			self.preset_ext = '.synthv1'
		elif args.format=='padthv1':
			self.plugin_name = 'padthv1'
			self.plugin_uri = 'http://padthv1.sourceforge.net/lv2'
			self.preset_ext = '.padthv1'
		else:
			raise p2lv2Exception("Format '{}' is not correct!".format(args.format))

		super().__init__(args, False)


	def parse_preset(self, preset):
		# Parse XML
		tree = ET.parse(preset['fpath'])
		root = tree.getroot()

		# Get preset name
		#preset_name = root.get("name")
		head, fname = os.path.split(preset['fpath'])
		preset_name, fext = os.path.splitext(fname)

		# Get ports data
		ports = {}
		for elem in root:
			for subelem in elem:
				lv2sym = subelem.get("name")
				lv2val = subelem.text
				if lv2sym:
					ports[lv2sym] = lv2val

		preset_data = {
			'name': self.sanitize_text(preset_name),
			'bank': preset['bank'],
			'ports': ports
		}
		return preset_data


#******************************************************************************
