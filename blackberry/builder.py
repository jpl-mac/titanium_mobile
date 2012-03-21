#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Appcelerator Titanium Mobile
# Copyright (c) 2011 by Appcelerator, Inc. All Rights Reserved.
# Licensed under the terms of the Apache Public License
# Please see the LICENSE included with this distribution for details.
#
# General builder script for staging, packaging, deploying,
# and debugging Titanium Mobile applications on Blackberry
#
import os, sys, subprocess, shutil, time, signal, string, platform, re, glob, hashlib, imp, inspect
import traceback
from tilogger import *

class Builder(object):

	def __init__(self, name, ndk, project_dir):
		self.top_dir = project_dir
		# TODO Mac: expand path os.path.join(project_dir,'build','blackberry')
		self.project_dir = project_dir 
		self.res_dir = os.path.join(self.project_dir,'res')
		# TODO Mac: expand path os.path.join(project_dir, 'platform', 'blackberry')
		self.platform_dir = ndk 
		self.project_src_dir = os.path.join(self.project_dir, 'src')
		self.project_gen_dir = os.path.join(self.project_dir, 'gen')
		self.name = name
		self.compiled_files = []
		self.force_rebuild = False
		self.debugger_host = None
		self.debugger_port = -1
		self.compile_js = False
		
		# TODO Mac: Add custom initialization for Builder class upon blackberry needs 

	def build_and_run(self, build_only=False):
		# TODO Mac: Reconfigure function upon blackberry needs
		# TODO Mac: V8 runtime should be added and possibly a lot of other stuff
		if build_only:
			os.system("mkbuild %s" % self.project_dir)
			sys.exit(1)
		
		print 'Executing'
		os.system("mkbuild %s" % self.project_dir)
		os.chdir(self.project_dir)
		# TODO Mac: Add corresponding parameters (ip, icon, bar_descriptor, etc...) to script in order to support:
		# blackberry-nativepackager script. Could be created a wrapper script package.py
		# blackberry-deploy script. Could be created a wrapper script deploy.py
		# For now used HelloWorldDisplay hardcoded project name, simulator ip address, etc...
		# For now used only for simulator
		os.system("blackberry-nativepackager -package Simulator-Debug\%s.bar bar-descriptor.xml -e Simulator-Debug\%s %s icon.png" % (self.name, self.name, self.name))
		os.system("blackberry-deploy -installApp -launchApp -device 192.168.127.128 -package Simulator-Debug\%s.bar" % self.name)
		sys.exit(1)

def dequote(s):
	if s[0:1] == '"':
		return s[1:-1]
	return s

def info(msg):
	log.info(msg)

def debug(msg):
	log.debug(msg)

def warn(msg):
	log.warn(msg)

def trace(msg):
	log.trace(msg)
	
def error(msg):
	log.error(msg)
	
if __name__ == "__main__":
	def usage():
		print "%s <command> <ndk_dir> <project_dir>" % os.path.basename(sys.argv[0])
		print
		print "available commands: "
		print
		print "  build         build project"
		print "  run           build and run the app on the simulator/device"
		
		sys.exit(1)

	argc = len(sys.argv)
	if argc < 2:
		usage()

	command = sys.argv[1]

	if command == 'run':
		if argc < 4:
			print 'Usage: %s run <project_dir> <blackberry_ndk>' % sys.argv[0]
			sys.exit(1)
		
		project_dir = sys.argv[2]
		print 'Project dir: %s' % project_dir
		ndk_dir = sys.argv[3]
		
	elif command == 'build':
		if argc < 4:
			print 'Usage: %s build <project_dir> <blackberry_ndk>' % sys.argv[0]
			sys.exit(1)

		project_dir = sys.argv[2]
		ndk_dir = sys.argv[3]
	else:
		if argc < 6 or command == '--help':
			usage()
	
	# TODO Mac: Should be available from tiapp.xml
	# Used hardcoded HelloWorldDisplay for now
	project_name = 'HelloWorldDisplay'
	# TODO Mac: Should be converted later to build\blackberry
#	ndk_dir = os.path.abspath(os.path.expanduser(dequote(sys.argv[2])))
#	project_dir = os.path.abspath(os.path.expanduser(dequote(sys.argv[3])))
	log = TiLogger(os.path.join(os.path.abspath(os.path.expanduser(dequote(project_dir))), 'build.log'))
	log.debug(" ".join(sys.argv))
	
	s = Builder(project_name,ndk_dir,project_dir)
	s.command = command

	try:
		if command == 'run':
			s.build_and_run()
		elif command == 'build':
			s.build_and_run(build_only=True)
		else:
			error("Unknown command: %s" % command)
			usage()
	except SystemExit, n:
		sys.exit(n)
	except:
		e = traceback.format_exc()
		error("Exception occured while building Blackberry project:")
		for line in e.splitlines():
			error(line)
		sys.exit(1)
