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
import os, sys, argparse

template_dir = os.path.abspath(os.path.dirname(sys._getframe(0).f_code.co_filename))
top_support_dir = os.path.dirname(template_dir) 
sys.path.append(top_support_dir)
sys.path.append(os.path.join(top_support_dir, 'common'))

from tilogger import TiLogger
from tiapp import TiAppXML

class Builder(object):

	def __init__(self, project_dir, ndk):
		self.top_dir = project_dir.rstrip(os.sep)
		# TODO Mac: Should replaced with os.path.join(project_dir,'build','blackberry')
		self.project_dir = self.top_dir
		# TODO Mac: This ndk path need to run environment setup if necessary
		# see http://stackoverflow.com/questions/3503719/emulating-bash-source-in-python 
		self.ndk = ndk 
		# TODO Mac: retrieve name from tiapp file, for now use basename, project don't have tiapp file yet
		# Also consider moving this code to run as that's the only method using it
		#project_tiappxml = os.path.join(self.top_dir,'tiapp.xml')
		#tiappxml = TiAppXML(project_tiappxml)
		#self.name = tiappxml.properties['name']
		self.name = os.path.basename(self.top_dir)
		
	def run(self):
		# TODO Mac: Reconfigure function upon blackberry needs
		# TODO Mac: V8 runtime should be added and possibly a lot of other stuff
		
		self.build()
		print 'Running'
		
		# Change current directory to do relative operations
		os.chdir("%s" % self.project_dir)
		# TODO Mac: Add corresponding parameters (ip, icon, bar_descriptor, etc...) to script in order to support:
		# blackberry-nativepackager script. Could be created a wrapper script package.py
		# blackberry-deploy script. Could be created a wrapper script deploy.py
		# For now used HelloWorldDisplay hardcoded project name, simulator ip address, etc...
		# For now used only for simulator
		barPath = os.path.join(self.project_dir, 'Simulator-Debug', '%s.bar' % self.name)
		savePath = os.path.join(self.project_dir, 'Simulator-Debug', self.name)
		os.system("blackberry-nativepackager -package %s bar-descriptor.xml -e %s %s icon.png" % (barPath, savePath, self.name))
		os.system("blackberry-deploy -installApp -launchApp -device 192.168.135.129 -package %s" % barPath)
	
	def build(self):
		# TODO Mac: Add corresponding parameters (ip, icon, bar_descriptor, etc...) to script in order to support:
		# blackberry-nativepackager script. Could be created a wrapper script package.py
		# blackberry-deploy script. Could be created a wrapper script deploy.py
		# For now used HelloWorldDisplay hardcoded project name, simulator ip address, etc...
		# For now used only for simulator
		print 'Building'

		print 'JP', self.project_dir
		os.system("mkbuild '%s'" % self.project_dir)
		
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

	# Setup script usage 
	parser = argparse.ArgumentParser(usage='<command> -t TYPE -d PROJECT_PATH -p NDK_PATH')
	
	parser.add_argument('command', choices=['build', 'run'], help='commands')
	parser.add_argument('-t', '--type', choices=['simulator', 'device'], help='simulator | device', required=True)
	parser.add_argument('-d', '--project_path', help='project directory path', required=True)
	parser.add_argument('-p', '--ndk_path', help='blackberry ndk path', required=True)
	
	# Parse input and call apropriate function
	args = parser.parse_args()

	log = TiLogger(os.path.join(os.path.abspath(os.path.expanduser(args.project_path)), 'build.log'))
	log.debug(" ".join(sys.argv))
	
	# TODO Mac: Remove. For testing only
	print args.type
	print args.ndk_path
	print args.project_path
	# end Remove

	builder = Builder(args.project_path, args.ndk_path)

	if (args.command == 'build'):
		builder.build()
	elif (args.command == 'run'):
		builder.run()
