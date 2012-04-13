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
		
		# Configuration for the bar-descriptor.xml file
		self.configDescriptor = {
			'id':self.id,
			'appname':self.name,
			'platformversion':self.ndk.version,
			'description':None,
			'version':'1.0',
			'author':'Appcelerator Titanium Mobile', # TODO MAC: Find out how validate the author
			'category':'core.games'
		}
		
		# Configuration for the project file
		self.configProject = {
			'appname':self.name,
			'buildlocation':None # TODO MAC: Find out how specify the build location
		}
		
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
		
		# TODO Mac: For now used temporarily created directory where exist source files
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
				
		# add replaced templates: bar-descriptor.xml, .project files
		templates = os.path.join(template_dir,'templates')
		# copy bar-descriptor.xml
		shutil.copy2(os.path.join(templates,'bar-descriptor.xml'), build_dir)
		render(os.path.join(build_dir,'bar-descriptor.xml'), self.configDescriptor)
		# copy project file
		shutil.copy2(os.path.join(templates,'project'), os.path.join(build_dir, '.project'))
		render(os.path.join(build_dir,'.project'), self.configProject)		

		# import project into workspace so it can be built with mkbuild
		self.ndk.importProject(build_dir)

		# TODO Mac: not sure what this is trying to accomplish
		# create the blackberry resources
		#blackberry_resources_dir = os.path.join(build_dir,'Resources')
		#if not os.path.exists(blackberry_resources_dir):
		#	os.makedirs(blackberry_resources_dir)

def render(template, config):
	baseDir = os.path.abspath(os.path.dirname(sys.argv[0]))
	baseDir = os.path.dirname(baseDir)
	sys.path.append(os.path.join(baseDir, 'common'))
	from mako.template import Template
	tmpl = load_template(template)
	f = None
	try:
		f = open(template, "w")
		f.write(tmpl.render(config = config))
	except Exception, e:
		print >>sys.stderr, e
		sys.exit(1)
	finally:
		if f!=None: f.close

def load_template(template):
	from mako.template import Template
	return Template(filename=template, output_encoding='utf-8', encoding_errors='replace')

def __runTemplatingDescriptorTest():
	baseDir = os.path.abspath(os.path.dirname(sys.argv[0]))
	baseDir = os.path.dirname(baseDir)
	sys.path.append(os.path.join(baseDir, 'common'))
	from mako.template import Template
	barFile = os.path.join(template_dir, 'templates', 'bar-descriptor.xml')
	tmpl = load_template(barFile)
	print tmpl.render(config = bb.configDescriptor)
	
def __runTemplatingProjectTest():
	baseDir = os.path.abspath(os.path.dirname(sys.argv[0]))
	baseDir = os.path.dirname(baseDir)
	sys.path.append(os.path.join(baseDir, 'common'))
	from mako.template import Template
	projectFile = os.path.join(template_dir, 'templates', 'project')
	tmpl = load_template(projectFile)
	print tmpl.render(config = bb.configProject)

if __name__ == '__main__':
	# Running unit test for -t parameter
	if len(sys.argv) == 2 and sys.argv[1]=='-t':
		baseDir = os.path.abspath(os.path.dirname(sys.argv[0]))
		baseDir = os.path.dirname(baseDir)
		sys.path.append(os.path.join(baseDir, 'common'))
		from tiunittest import UnitTest
		
		bbndk = BlackberryNDK('c:\\bbndk-2.0.0')
		bb = Blackberry('TemplateTest', 'com.macadamian.template', bbndk)
		
		with UnitTest('Test template replacing on bar-descriptor.xml file..'):
			__runTemplatingDescriptorTest()
			
		with UnitTest('Test template replacing on .project file..'):
			__runTemplatingProjectTest()
		
		sys.exit(1)
		
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
	bb.create(sys.argv[3].decode("utf-8"))
