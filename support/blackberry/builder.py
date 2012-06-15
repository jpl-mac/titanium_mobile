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
import os, sys, shutil
from optparse import OptionParser

template_dir = os.path.abspath(os.path.dirname(sys._getframe(0).f_code.co_filename))
top_support_dir = os.path.dirname(template_dir) 
sys.path.append(top_support_dir)
sys.path.append(os.path.join(top_support_dir, 'common'))

from tilogger import TiLogger
from tiapp import TiAppXML
from blackberryndk import BlackberryNDK
from blackberry import Blackberry
from deltafy import Deltafy, Delta

class Builder(object):
	type2variantCpu = {'simulator' : ('o-g', 'x86'),
	                 'device' : ('o.le-v7-g', 'arm'),
	                 'deploy' : ('o.le-v7', 'arm')}

	def __init__(self, project_dir, type, ndk):
		self.top_dir = project_dir.rstrip(os.sep)
		self.type = type
		(self.variant, self.cpu) = Builder.type2variantCpu[type]
		self.ndk = ndk 
		self.project_tiappxml = os.path.join(self.top_dir, 'tiapp.xml')
		self.tiappxml = TiAppXML(self.project_tiappxml)
		self.name = self.tiappxml.properties['name']
		self.buildDir = os.path.join(self.top_dir, 'build', 'blackberry', self.name)
		self.project_deltafy = Deltafy(self.top_dir)
		
	def run(self, ipAddress, password = None, debugToken = None):
		# TODO Mac: V8 runtime should be added and possibly a lot of other stuff
		
		retCode = self.build()
		if retCode != 0:
			return retCode
		info('Running')
		
		# Check if tiapp.xml changed during last build
		tiapp_delta = self.project_deltafy.scan_single_file(self.project_tiappxml)
		tiapp_changed = tiapp_delta is not None

		if (tiapp_changed):
			# regenerate bar-descriptor.xml
			# TODO MAC: Add blackberry specific properties. Needs update in tiapp.py script
			templates = os.path.join(template_dir,'templates')
			shutil.copy2(os.path.join(templates,'bar-descriptor.xml'), self.buildDir)
			Blackberry.regenerateBarDescriptor(os.path.join(self.buildDir,'bar-descriptor.xml'), self.tiappxml.properties)

		# Change current directory to do relative operations
		os.chdir("%s" % self.buildDir)
		barPath = os.path.join(self.buildDir, self.cpu, self.variant, '%s.bar' % self.name)
		savePath = os.path.join(self.buildDir, self.cpu, self.variant, self.name)
		retCode = self.ndk.package(barPath, savePath, self.name, self.type, debugToken)
		if retCode != 0:
			return retCode

		retCode = self.ndk.deploy(ipAddress, barPath, password)
		return retCode
	
	def build(self):
		info('Building')
		return self.ndk.build(self.buildDir, self.cpu)

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

	# Setup script usage using optparse
	parser = OptionParser(usage='<command: build | run> -t TYPE -d PROJECT_PATH [-p NDK_PATH] [-i IP_ADDRESS] [-s DEVICE_PASSWORD]')
	
	commonGroup = parser.add_option_group('Common options')
	commonGroup.add_option('-t', '--type', choices=['simulator', 'device', 'deploy'], help='simulator | device | deploy', dest='type')
	commonGroup.add_option('-d', '--project_path', help='project directory path', dest='project_path')
	commonGroup.add_option('-p', '--ndk_path', help='blackberry ndk path', dest='ndk_path')
	
	runGroup = parser.add_option_group('Run/Deploy options')
	runGroup.add_option('-i', '--ip_address', help='(simulator | device) ip address', dest='ip_address')
	runGroup.add_option('-s', '--device_password', help='(simulator | device) protection password', dest='device_password')
	runGroup.add_option('--debug_token', help='path to debug token file (required for --type device)')

	(options, args) = parser.parse_args()
	if len(args) != 1:
		print parser.get_usage()
		sys.exit(1)

	buildUsage = 'Usage: %s build -t TYPE -d PROJECT_PATH [-p NDK_PATH]' %os.path.basename(sys.argv[0])
	runUsage = 'Usage: %s run -t TYPE -d PROJECT_PATH [-p NDK_PATH] -i IP_ADDRESS [-s DEVICE_PASSWORD] [--debug_token DEBUG_TOKEN]' %os.path.basename(sys.argv[0])

	type = options.type and options.type.decode('utf-8')
	projectPath = options.project_path and options.project_path.decode('utf-8')
	ndkPath = options.ndk_path and options.ndk_path.decode('utf-8')
	ipAddress = options.ip_address and options.ip_address.decode('utf-8')
	devicePassword = options.device_password and options.device_password.decode('utf-8')
	debugToken = options.debug_token and options.debug_token.decode('utf-8')
	if args[0] == 'build':
		if options.type == None or options.project_path == None:
			parser.error(buildUsage)
			sys.exit(1)
	elif args[0] == 'run':
		if options.type == None or options.project_path == None or options.ip_address == None or (type == 'device' and debugToken == None):
			if type == 'device' and debugToken == None:
				print "--debug_token is required for --type device"
			parser.error(runUsage)
			sys.exit(1)
	else:
		print parser.get_usage()
		sys.exit(1)

	log = TiLogger(os.path.join(os.path.abspath(os.path.expanduser(projectPath)), 'build_blackberry.log'))
	log.debug(" ".join(sys.argv))
	try:
		bbndk = BlackberryNDK(ndkPath, log = log)
	except Exception, e:
		print >>sys.stderr, e
		sys.exit(1)

	builder = Builder(projectPath, type, bbndk)

	retCode = 1
	if (args[0] == 'build'):
		retCode = builder.build()
	elif (args[0] == 'run'):
		retCode = builder.run(ipAddress, devicePassword, debugToken)
	sys.exit(retCode)
