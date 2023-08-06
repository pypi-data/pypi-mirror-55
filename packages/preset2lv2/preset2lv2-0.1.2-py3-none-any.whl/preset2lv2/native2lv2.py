# -*- coding: utf-8 -*-
#******************************************************************************
# ZYNTHIAN PROJECT: Zynthian LV2 Preset Converters
# 
# native2lv2 base class: Implements LV2 Bundle and TTL generation
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
import random
import string
import logging
from tornado import template
from subprocess import check_output
from pkg_resources import resource_filename


class p2lv2Exception(Exception):
	pass
	

# Implements LV2 Bundle & TTL generation
# Implements V1 native format parser (XML)
class native2lv2:

	templates_dpath = "./templates"
	manifest_tpl = "manifest.ttl.tpl"
	preset_tpl = "preset.ttl.tpl"

	def __init__(self, args, bank_per_file=False):
		#self.plugin_name = None
		#self.plugin_uri = None
		#self.preset_ext = None

		self.banks = []
		self.presets = []
		self.preset_data = []
		self.bank_per_file = bank_per_file

		if args.bank:
			self.bundle_name = args.bank
		else:
			self.bundle_name = None

		self.get_preset_data(args.path)
		self.generate_lv2_bundle()


	def sanitize_text(self, text):
		# Remove bad chars
		bad_chars = ['.', ',', ';', ':', '!', '*', '?', '@', '+', '%', '=', '"', '\'', '`', '/', '\\', '^', '<', '>', '[', ']', '(', ')', '{', '}']
		for i in bad_chars: 
			text = text.replace(i, ' ')  

		# Strip and replace (multi)spaces by single underscore
		text = '_'.join(text.split())
		text = '_'.join(filter(None,text.split('_')))

		# If resulting string is empty, generate random string
		if not text:
			text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

		return text


	def get_preset_list(self, path):

		# Remove last dash
		if path[-1]=='/':
			path = path[:-1]

		# Extract Bundle Name and file extension
		fdir, fname = os.path.split(path)
		bname, fext = os.path.splitext(fname)
		if not self.bundle_name:
			self.bundle_name = self.sanitize_text(bname)

		# Search for preset files ...
		self.banks = []
		self.presets = []
		if os.path.isdir(path):
			for f in check_output("find \"{}\" -type f -iname *{}".format(path,self.preset_ext), shell=True).decode("utf-8").split("\n"):
				if f.strip():
					bank = self.bundle_name

					# Extract banks => subdirs
					if self.bank_per_file:
						head, sbank = os.path.split(f[len(path)+1:])
						sbank, fext = os.path.splitext(sbank)
					else:
						sbank, prfile = os.path.split(f[len(path)+1:])

					if sbank:
						bank += '_' + self.sanitize_text(sbank.replace('/','_'))

					#Append preset/bank to list
					if bank not in self.banks:
						self.banks.append(bank)

					self.presets.append({
						'fpath': f,
						'bank': bank
					})

		elif fext.lower()==self.preset_ext:
			self.banks.append(self.bundle_name)
			self.presets.append({
						'fpath': args.path,
						'bank': self.bundle_name
					})

		else:
			raise p2lv2Exception("Preset file extension '{}' is not correct!".format(fext))

		if len(self.presets)==0:
			raise p2lv2Exception("No native presets found!")


	def get_preset_data(self, path):
		self.preset_data = []
		self.get_preset_list(path)
		for preset in self.presets:
			try:
				res = self.parse_preset(preset)
			except Exception as e:
				logging.error("Can't parse '{}': {}".format(preset['fpath'], e))
				continue

			if isinstance(res, dict):
				self.preset_data.append(res)
			else:
				self.preset_data += res


	def generate_lv2_bundle(self):
		# Check data
		if len(self.preset_data)==0:
			raise p2lv2Exception("No preset data to generate LV2 bundle!")

		# Generate data structure with the presets data
		self.data = {
			'plugin_name': self.plugin_name,
			'plugin_url': self.plugin_uri,
			'banks': self.banks,
			'presets': self.preset_data
		}

		# Configure template loader
		template_dir = resource_filename(__name__, "templates")
		loader = template.Loader(template_dir)

		# Generate manifest TTL
		manifest_ttl = loader.load(self.manifest_tpl).generate(**self.data)
		logging.debug("manifest.ttl =>\n{}".format(manifest_ttl))

		# Generate presets TTL
		preset_template = loader.load(self.preset_tpl)
		presets_ttl = {}
		for p in self.preset_data:
			p['plugin_url'] = self.plugin_uri
			ttl = preset_template.generate(**p)
			pn = "{}_{}".format(p['bank'],p['name'])
			presets_ttl[pn] = ttl
			logging.debug("{}.ttl =>\n{}".format(pn, ttl))

		# Create LV2 Bundle directory
		bundle_dir = "{}_{}.presets.lv2".format(self.plugin_name, self.bundle_name)
		os.mkdir(bundle_dir)
		logging.info("Generating LV2 bundle '{}' ...".format(bundle_dir))

		# Save TTL files
		fpath = "{}/manifest.ttl".format(bundle_dir)
		with open(fpath, 'wb') as f:
			logging.info("... writing '{}'".format(fpath))
			f.write(manifest_ttl)
			f.close()

		n = 0
		for pn in presets_ttl:
			fpath = "{}/{}.ttl".format(bundle_dir, pn)
			with open(fpath, 'wb') as f:
				logging.info("... writing '{}'".format(fpath))
				f.write(presets_ttl[pn])
				f.close()
				n += 1

		logging.info("Bundle '{}' generated with {} presets in {} banks.".format(bundle_dir, n, len(self.banks)))
		if n>640:
			logging.warning("There are too many presets. You could experiment timeouts when loading the plugin!")


#******************************************************************************
