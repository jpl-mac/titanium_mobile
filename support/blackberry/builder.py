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
import os, sys
from optparse import OptionParser

template_dir = os.path.abspath(os.path.dirname(sys._getframe(0).f_code.co_filename))
top_support_dir = os.path.dirname(template_dir) 
sys.path.append(top_support_dir)
sys.path.append(os.path.join(top_support_dir, 'common'))

from tilogger import TiLogger
from tiapp import TiAppXML
from blackberryndk import BlackberryNDK

class Builder(object):
	type2variantCpu = {'simulator' : ('o-g', 'x86'),
	                 'device' : ('o.le-v7-g', 'arm'),
	                 'deploy' : ('o.le-v7', 'arm')}

	def __init__(self, project_dir, type, ndk):
		self.top_dir = project_dir.rstrip(os.sep)
		self.type = type
		(self.variant, self.cpu) = Builder.type2variantCpu[type]
		self.ndk = ndk 
		project_tiappxml = os.path.join(self.top_dir, 'tiapp.xml')
		tiappxml = TiAppXML(project_tiappxml)
		self.name = tiappxml.properties['name']
		self.buildDir = os.path.join(self.top_dir, 'build', 'blackberry', self.name)
		
	def run(self, ipAddress, password = None):
		# TODO Mac: V8 runtime should be added and possibly a lot of other stuff
		
		retCode = self.build()
		if retCode != 0:
			return retCode
		info('Running')
		
		# Change current directory to do relative operations
		os.chdir("%s" % self.buildDir)
		# TODO Mac: Add corresponding parameters (ip, icon, bar_descriptor, etc...) to script in order to support:
		# For now use simulator ip address, etc...
		# For now use only for simulator
		# TODO Mac: log each command that is executed to the build.log file,
		# output might be interesting as well
		# TODO Mac: See if we can reasonably launch the simulator from here and fetch the ip address
		barPath = os.path.join(self.buildDir, self.cpu, self.variant, '%s.bar' % self.name)
		savePath = os.path.join(self.buildDir, self.cpu, self.variant, self.name)
		retCode = self.ndk.package(barPath, savePath, self.name, self.type)
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

	# Setup script usage using argparse
	parser = OptionParser(usage='<command: build | run> -t TYPE -d PROJECT_PATH -n NDK_PATH -i IP_ADDRESS [-p DEVICE_PASSWORD]')
	
	commonGroup = parser.add_option_group('Common options')
	commonGroup.add_option('-t', '--type', choices=['simulator', 'device', 'deploy'], help='simulator | device | deploy', dest='type')
	commonGroup.add_option('-d', '--project_path', help='project directory path', dest='project_path')
	commonGroup.add_option('-n', '--ndk_path', help='blackberry ndk path', dest='ndk_path')
	
	runGroup = parser.add_option_group('Run/Deploy options')
	runGroup.add_option('-i', '--ip_address', help='(simulator | device) ip address', dest='ip_address')
	runGroup.add_option('-p', '--device_password', help='(simulator | device) protection password', dest='device_password')

	(options, args) = parser.parse_args()
	if len(args) != 1:
		print parser.get_usage()
		sys.exit(1)

	buildUsage = 'Usage: build -t TYPE -d PROJECT_PATH -n NDK_PATH'
	runUsage = 'Usage: run -t TYPE -d PROJECT_PATH -n NDK_PATH -i IP_ADDRESS [-p DEVICE_PASSWORD]'

	if args[0] == 'build':
		if options.type == None or options.project_path == None or options.ndk_path == None:
			parser.error(buildUsage)
			sys.exit(1)
	elif args[0] == 'run':
		if options.type == None or options.project_path == None or options.ndk_path == None or options.ip_address == None:
			parser.error(runUsage)
			sys.exit(1)
	else:
		print parser.get_usage()
		sys.exit(1)

	log = TiLogger(os.path.join(os.path.abspath(os.path.expanduser(options.project_path)), 'build_blackberry.log'))
	log.debug(" ".join(sys.argv))
	try:
		bbndk = BlackberryNDK(options.ndk_path and options.ndk_path.decode('utf-8'), log = log)
	except Exception, e:
		print >>sys.stderr, e
		sys.exit(1)

	builder = Builder(options.project_path.decode('utf-8'), options.type.decode('utf-8'), bbndk)

	retCode = 1
	if (args[0] == 'build'):
		retCode = builder.build()
	elif (args[0] == 'run'):
		retCode = builder.run(options.ip_address.decode('utf-8'), options.device_password.decode('utf-8') if options.device_password != None else None)
	sys.exit(retCode)
