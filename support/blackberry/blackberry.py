#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Appcelerator Titanium Mobile
# Copyright (c) 2012 by Appcelerator, Inc. All Rights Reserved.
# Licensed under the terms of the Apache Public License
# Please see the LICENSE included with this distribution for details.
#
# Blackberry Application Script
#

import os, sys, shutil

template_dir = os.path.abspath(os.path.dirname(sys._getframe(0).f_code.co_filename))
# TODO Mac: don't think we need this just yet
#sys.path.append(os.path.join(template_dir,'..'))

class Blackberry(object):

	def __init__(self, name, appid):
		self.name = name
		self.id = appid

	def create(self, dir): 
		project_dir = os.path.join(dir, self.name)

		# Creates directory named as project name.
		# mkbuild utility uses path's last component as project name. So, project directory should be named as project
		blackberry_dir = os.path.join(project_dir, 'build', 'blackberry', self.name)

		if not os.path.exists(blackberry_dir):
			os.makedirs(blackberry_dir)		

		# TODO Mac: figure out if we need to do something with version in this script
		#version = os.path.basename(os.path.abspath(os.path.join(template_dir, '..')))

		blackberry_project_resources = os.path.join(project_dir,'Resources','blackberry')
		if os.path.exists(blackberry_project_resources):
			shutil.rmtree(blackberry_project_resources)
		shutil.copytree(os.path.join(template_dir,'resources'),blackberry_project_resources)
		# TODO Mac: For now used temporarily created directory where exist files as:
		# bar-descriptor.xml, project files and sources.
		sourcePath = os.path.join(template_dir,'HelloWorldDisplay')
		for files in os.listdir(sourcePath):
			file = os.path.join(sourcePath, files)
			try:
				if (os.path.isdir(file)):
					srcDir = os.path.join(blackberry_dir, files)
					if (os.path.exists(srcDir)):
						shutil.rmtree(srcDir)
					shutil.copytree(file, srcDir)
				else :
					shutil.copy2(file, blackberry_dir)
			except Exception, e:
				print >> sys.stderr, e
				sys.exit(1)
		
		# TODO Mac: not sure what this is trying to accomplish
		# create the blackberry resources
		#blackberry_resources_dir = os.path.join(blackberry_dir,'Resources')
		#if not os.path.exists(blackberry_resources_dir):
		#	os.makedirs(blackberry_resources_dir)

if __name__ == '__main__':
	# This script is only meant to be invoked from project.py
	if len(sys.argv) != 5 or sys.argv[1]=='--help':
		print "Usage: %s <name> <id> <directory> <blackberry_ndk>" % os.path.basename(sys.argv[0])
		sys.exit(1)

	bb = Blackberry(sys.argv[1], sys.argv[2])
	# TODO Mac: do something with argv[4], the blackberry ndk folder
	bb.create(sys.argv[3])
