# -*- coding: utf-8 -*-
#******************************************************************************
# ZYNTHIAN PROJECT: Zynthian LV2 Preset Converters
# 
# dx7syx12lv2 class: Convert native DX7 SysEx presets to LV2
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
import copy
from subprocess import check_output

from . import native2lv2

class dx7syx2lv2(native2lv2.native2lv2):

	dxsyx_command = "/usr/local/bin/dxsyx -y"

	default_ports = {
		"cutoff": "1.0",
		"resonance": "0.0",
		"output": "1.0",
		"engine": "0",
		"number_of_voices": "16",
		"polymono": "0",
		"pitch_bend_range": "1",
		"pitch_bend_step": "0",
		"mod_wheel_range": "99",
		"mod_wheel_assign": "0",
		"foot_ctrl_range": "99",
		"foot_ctrl_assign": "0",
		"breath_ctrl_range": "99",
		"breath_ctrl_assign": "0",
		"aftertouch_range": "99",
		"aftertouch_assign": "0",
		"master_tune": "0.0",
		"op1_enable": "1.0",
		"op2_enable": "1.0",
		"op3_enable": "1.0",
		"op4_enable": "1.0",
		"op5_enable": "1.0",
		"op6_enable": "1.0"
	}

	def __init__(self, args):
		self.plugin_name = 'dexed'
		self.plugin_uri = 'https://github.com/dcoredump/dexed.lv2'
		self.preset_ext = '.syx'

		super().__init__(args, True)


	def parse_preset(self, preset):
		# Parse SysEx file with dxsyx
		rows = check_output("{} \"{}\"".format(self.dxsyx_command, preset['fpath']), shell=True).decode("utf-8").split("\n")
		#logging.debug("DxSyx Output:\n{}".format(rows))

		# Some checks ...
		if rows[0].strip()!='---':
			raise native2lv2.p2lv2Exception("SysEx parse error. Bad format or corrupted file!")

		if not rows[1].startswith('filename: '):
			raise native2lv2.p2lv2Exception("SysEx parse error. Bad format or corrupted file!")

		# Parse data
		preset_data = []
		ports = None
		voice = None
		for row in rows[2:]:
			if row.startswith('  voice_name: '):
				if ports:
					preset_data.append({
						'name': voice,
						'bank': preset['bank'],
						'ports': ports
					})
				voice = self.sanitize_text(row[14:])
				ports = copy.copy(self.default_ports)
			elif row.startswith('    '):
				 sym, val= row[4:].split(':')
				 ports[sym] = val.strip()

		return preset_data


#******************************************************************************
