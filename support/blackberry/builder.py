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

	# Setup script usage 
	parser = argparse.ArgumentParser(usage='<command> -t TYPE -d PROJECT_PATH -p NDK_PATH')
	
	parsers = parser.add_subparsers(dest='subparser_name')
	buildParser = parsers.add_parser('build')
	runParser = parsers.add_parser('run')

	buildParser.add_argument('-t', '--type', choices=['simulator', 'device', 'deploy'], help='simulator | device | deploy', required=True)
	buildParser.add_argument('-d', '--project_path', help='project directory path', required=True)
	buildParser.add_argument('-n', '--ndk_path', help='blackberry ndk path')

	runParser.add_argument('-t', '--type', choices=['simulator', 'device', 'deploy'], help='simulator | device | deploy', required=True)
	runParser.add_argument('-i', '--ip_address', help='(simulator | device) ip address', required=True)
	runParser.add_argument('-p', '--device_password', help='(simulator | device) protection password')
	runParser.add_argument('-d', '--project_path', help='project directory path', required=True)
	runParser.add_argument('-n', '--ndk_path', help='blackberry ndk path')
	
	# Parse input and call apropriate function
	args = parser.parse_args()

	log = TiLogger(os.path.join(os.path.abspath(os.path.expanduser(args.project_path)), 'build_blackberry.log'))
	log.debug(" ".join(sys.argv))
	try:
		bbndk = BlackberryNDK(args.ndk_path and args.ndk_path.decode('utf-8'), log = log)
	except Exception, e:
		print >>sys.stderr, e
		sys.exit(1)

	builder = Builder(args.project_path.decode('utf-8'), args.type.decode('utf-8'), bbndk)

	retCode = 1
	if (args.subparser_name == 'build'):
		retCode = builder.build()
	elif (args.subparser_name == 'run'):
		retCode = builder.run(args.ip_address.decode('utf-8'), args.device_password.decode('utf-8') if args.device_password != None else None)
	sys.exit(retCode)
