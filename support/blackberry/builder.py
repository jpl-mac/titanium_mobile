#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Appcelerator Titanium Mobile
# Copyright (c) 2012 by Appcelerator, Inc. All Rights Reserved.
# Licensed under the terms of the Apache Public License
# Please see the LICENSE included with this distribution for details.
#
# General builder script for staging, packaging, deploying,
# and debugging Titanium Mobile applications on Blackberry
#
import os, sys, traceback, argparse

from tilogger import *
from compiler.ast import Sub

class Builder(object):

	def __init__(self, name, project_dir, ndk):
		# TODO Mac: Should be under build/blackberry from titanium side.
		# Should be converted to os.path.join(project_dir,'build','blackberry')
		self.project_dir = project_dir
		# TODO Mac: This ndk path need to run environment setup if necessary 
		self.ndk = ndk 
		self.name = name
		# TODO Mac: Need to figure out when we need to rebuild and when not. 
		# From initial investigation it could be done based on tiapp.xml.
		self.force_rebuild = False
		
	def run(self):
		# TODO Mac: Reconfigure function upon blackberry needs
		# TODO Mac: V8 runtime should be added and possibly a lot of other stuff
		
		print 'Building & Running'
		self.build()
		
		# Change current directory to do a relative operations 
		os.chdir(self.project_dir)
		# TODO Mac: Add corresponding parameters (ip, icon, bar_descriptor, etc...) to script in order to support:
		# blackberry-nativepackager script. Could be created a wrapper script package.py
		# blackberry-deploy script. Could be created a wrapper script deploy.py
		# For now used HelloWorldDisplay hardcoded project name, simulator ip address, etc...
		# For now used only for simulator
		barPath = os.path.join(self.project_dir, 'Simulator-Debug', '%s.bar' % self.name)
		savePath = os.path.join(self.project_dir, 'Simulator-Debug', self.name)
		os.system("blackberry-nativepackager -package %s bar-descriptor.xml -e %s %s icon.png" % (barPath, savePath, self.name))
		os.system("blackberry-deploy -installApp -launchApp -device 192.168.127.128 -package %s" % barPath)
#		sys.exit(0)
	
	def build(self):
		# TODO Mac: Add corresponding parameters (ip, icon, bar_descriptor, etc...) to script in order to support:
		# blackberry-nativepackager script. Could be created a wrapper script package.py
		# blackberry-deploy script. Could be created a wrapper script deploy.py
		# For now used HelloWorldDisplay hardcoded project name, simulator ip address, etc...
		# For now used only for simulator
		print 'Building'
		os.system("mkbuild %s" % self.project_dir)
#		sys.exit(0)

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
	
def build_project(args):
	# TODO Mac: Remove. For testing only
	print args.type
	print args.ndk_path
	print args.project_path
	
	# TODO Mac: Should be available from tiapp.xml
	# Used hardcoded HelloWorldDisplay for now
	project_name = 'HelloWorldDisplay'
	builder = Builder(project_name, args.project_path, args.ndk_path)
	builder.build()
	
def run_project(args):
	# TODO Mac: Remove. For testing only
	print args.type
	print args.ndk_path
	print args.project_path
	
	# TODO Mac: Should be available from tiapp.xml
	# Used hardcoded HelloWorldDisplay for now
	project_name = 'HelloWorldDisplay'
	builder = Builder(project_name, args.project_path, args.ndk_path)
	builder.run()
	
if __name__ == "__main__":

	# Setup script usage 
	parser = argparse.ArgumentParser(prog='builder')
	subparsers = parser.add_subparsers(help='commands')
	
	# Added parsers for each available command
	parser_build = subparsers.add_parser('build', help='build the project')
	parser_run = subparsers.add_parser('run', help='run the project on device or simulator')
	
	# Setup arguments parser for 'builder build' command
	parser_build.set_defaults(func=build_project)
	parser_build.add_argument('type', help='simulator/device')
	parser_build.add_argument('project_path', help='project directory path')
	parser_build.add_argument('ndk_path', help='blackberry ndk path')
	
	# Setup arguments parser for 'builder run' command	
	parser_run.set_defaults(func=run_project)
	parser_run.add_argument('type', help='simulator/device')
	parser_run.add_argument('project_path', help='blackberry ndk path')
	parser_run.add_argument('ndk_path', help='project directory path')

	# Parse input and call apropriate function
	args = parser.parse_args()
	args.func(args)

	# TODO: Move tilogger to 'common' directory to not duplicate. Could require additional changes in other files.
	#	log = TiLogger(os.path.join(os.path.abspath(os.path.expanduser(dequote(project_dir))), 'build.log'))
	debug(" ".join(sys.argv))
	#	log.debug(" ".join(sys.argv))
