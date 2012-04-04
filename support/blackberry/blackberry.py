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
from blackberryndk import BlackberryNDK

template_dir = os.path.abspath(os.path.dirname(sys._getframe(0).f_code.co_filename))
# TODO Mac: don't think we need this just yet
#sys.path.append(os.path.join(template_dir,'..'))

class Blackberry(object):

	def __init__(self, name, appid, bbndk):
		self.name = name
		self.id = appid
		self.ndk = bbndk

	def create(self, dir): 
		project_dir = os.path.join(dir, self.name)

		# Creates directory named as project name.
		# mkbuild utility uses path's last component as project name. So, project directory should be named as project
		build_dir = os.path.join(project_dir, 'build', 'blackberry', self.name)

		if not os.path.exists(build_dir):
			os.makedirs(build_dir)

		# TODO Mac: figure out if we need to do something with version in this script
		#version = os.path.basename(os.path.abspath(os.path.join(template_dir, '..')))

		blackberry_project_resources = os.path.join(project_dir,'Resources','blackberry')
		if os.path.exists(blackberry_project_resources):
			shutil.rmtree(blackberry_project_resources)
		shutil.copytree(os.path.join(template_dir,'resources'),blackberry_project_resources)
		# TODO Mac: For now used temporarily created directory where exist files as:
		# bar-descriptor.xml, project files and sources.
		sourcePath = os.path.join(template_dir,'HelloWorldDisplay')
		for file in os.listdir(sourcePath):
			path = os.path.join(sourcePath, file)
			try:
				if os.path.isdir(path):
					dstDir = os.path.join(build_dir, file)
					if (os.path.exists(dstDir)):
						shutil.rmtree(dstDir)
					shutil.copytree(path, dstDir)
				else:
					shutil.copy2(path, build_dir)
			except Exception, e:
				print >> sys.stderr, e
				sys.exit(1)

		# import project into workspace so it can be built with mkbuild
		print build_dir
		self.ndk.importProject(build_dir)

		# TODO Mac: not sure what this is trying to accomplish
		# create the blackberry resources
		#blackberry_resources_dir = os.path.join(build_dir,'Resources')
		#if not os.path.exists(blackberry_resources_dir):
		#	os.makedirs(blackberry_resources_dir)

if __name__ == '__main__':
	# This script is only meant to be invoked from project.py
	if len(sys.argv) != 5 or sys.argv[1]=='--help':
		print "Usage: %s <name> <id> <directory> <blackberry_ndk>" % os.path.basename(sys.argv[0])
		sys.exit(1)

	try:
		bbndk = BlackberryNDK(sys.argv[4].decode("utf-8"))
	except Exception, e:
		print >>sys.stderr, e
		sys.exit(1)

	bb = Blackberry(sys.argv[1].decode("utf-8"), sys.argv[2].decode("utf-8"), bbndk)
	bb.create(sys.argv[3]).decode("utf-8")
