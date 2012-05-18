#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Appcelerator Titanium Mobile
# Copyright (c) 2012 by Appcelerator, Inc. All Rights Reserved.
# Licensed under the terms of the Apache Public License
# Please see the LICENSE included with this distribution for details.
#
# General script for interacting with a Blackberry device
#
import os, platform, subprocess, sys, argparse

template_dir = os.path.abspath(os.path.dirname(sys._getframe(0).f_code.co_filename))
top_support_dir = os.path.dirname(template_dir)
sys.path.append(top_support_dir)
sys.path.append(os.path.join(top_support_dir, 'common'))

from tilogger import TiLogger
from tiapp import TiAppXML
from blackberryndk import BlackberryNDK
from builder import Builder

class DeviceManagement(object):
	def __init__(self, project_dir, type, ndk):
		self.top_dir = project_dir.rstrip(os.sep)
		(self.variant, self.cpu) = Builder._type2variantCpu[type]
		self.ndk = ndk
		project_tiappxml = os.path.join(self.top_dir, 'tiapp.xml')

		# hide property output
		with open(os.devnull, 'w') as nul:
			sys.stdout = nul
			tiappxml = TiAppXML(project_tiappxml, True)
			sys.stdout = sys.__stdout__
		self.name = tiappxml.properties['name']
		self.buildDir = os.path.join(self.top_dir, 'build', 'blackberry', self.name)

	def _run(self, command):
		assert type(command) is list
		try:
			print 'Command: ' + ' '.join(command)
			subprocess.check_call(command)
			return 0
		except subprocess.CalledProcessError, cpe:
			print >>sys.stderr, cpe, cpe.output
			return cpe.returncode
		except OSError, e:
			print >>sys.stderr, e
			return e.errno

	def getDevice(self):
		# TODO Mac: either get this through a passed argument or try to detect
		return '192.168.226.132'

	def getPackage(self):
		return os.path.join(self.buildDir, self.cpu, self.variant, '%s.bar' % self.name)

	def terminateApp(self):
		if platform.system() == 'Windows':
			deploy = 'blackberry-deploy.bat'
		else:
			deploy = 'blackberry-deploy'
		command = [deploy, '-terminateApp', '-device', self.getDevice(), '-package', self.getPackage()]
		return self._run(command)

	def isAppRunning(self):
		if platform.system() == 'Windows':
			deploy = 'blackberry-deploy.bat'
		else:
			deploy = 'blackberry-deploy'
		command = [deploy, '-isAppRunning', '-device', self.getDevice(), '-package', self.getPackage()]
		return self._run(command)

	def getFile(self, hostFile, deviceFile):
		if platform.system() == 'Windows':
			deploy = 'blackberry-deploy.bat'
		else:
			deploy = 'blackberry-deploy'
		command = [deploy, '-getFile', deviceFile, hostFile, '-device', self.getDevice(), '-package', self.getPackage()]
		return self._run(command)

	def putFile(self, hostFile, deviceFile):
		if platform.system() == 'Windows':
			deploy = 'blackberry-deploy.bat'
		else:
			deploy = 'blackberry-deploy'
		command = [deploy, '-putFile', hostFile, deviceFile, '-device', self.getDevice(), '-package', self.getPackage()]
		return self._run(command)

if __name__ == "__main__":

	# Setup script usage
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--type', choices=['simulator', 'device', 'deploy'], required=True)
	parser.add_argument('-d', '--project_path', help='project directory path', required=True)
	parser.add_argument('-p', '--ndk_path', help='blackberry ndk path')

	subparser = parser.add_subparsers(dest='subparser_name')
	subparser.add_parser('getDevice')
	subparser.add_parser('terminateApp')
	subparser.add_parser('isAppRunning')
	putFileParser = subparser.add_parser('getFile')
	putFileParser.add_argument('hostFile')
	putFileParser.add_argument('deviceFile')
	putFileParser = subparser.add_parser('putFile')
	putFileParser.add_argument('hostFile')
	putFileParser.add_argument('deviceFile')

	# Parse input and call apropriate function
	args = parser.parse_args()

	log = TiLogger(None, level = TiLogger.INFO)
	try:
		bbndk = BlackberryNDK(args.ndk_path and args.ndk_path.decode('utf-8'), log = log)
	except Exception, e:
		print >>sys.stderr, e
		sys.exit(1)
	deviceManagement = DeviceManagement(args.project_path.decode('utf-8'), args.type.decode('utf-8'), bbndk)

	try:
		retCode = 0
		if (args.subparser_name == 'getDevice'):
			print deviceManagement.getDevice()
		elif (args.subparser_name == 'terminateApp'):
			retCode = deviceManagement.terminateApp()
		elif (args.subparser_name == 'isAppRunning'):
			retCode = deviceManagement.isAppRunning()
		elif (args.subparser_name == 'getFile'):
			retCode = deviceManagement.getFile(args.hostFile.decode('utf-8'), args.deviceFile.decode('utf-8'))
		elif (args.subparser_name == 'putFile'):
			retCode = deviceManagement.putFile(args.hostFile.decode('utf-8'), args.deviceFile.decode('utf-8'))
		sys.exit(retCode)
	except Exception, e:
		print >>sys.stderr, e
		sys.exit(1)
