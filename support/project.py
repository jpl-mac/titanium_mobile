#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Unified Titanium Mobile Project Script
#
import os, sys, subprocess, shutil, codecs, argparse

def run(args):
	return subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()

def main():
	parser = argparse.ArgumentParser(description='Unified Titanium Mobile Project Script')
	parser.add_argument('name', help='project name')
	parser.add_argument('id', help='app id')
	parser.add_argument('directory', help='location')
	parser.add_argument('platforms', help='deployment targets space separated {iphone | android | mobileweb | blackberry}', nargs='+')
	# Added to show up in the usage string as we need to special handle it
	parser.add_argument(metavar='android_sdk', help='android SDK home (if android in platforms)', nargs='?', dest='notUsed')
	# Included for future support as it is not currently used by Ti Studio
	parser.add_argument('--android_sdk', help='android SDK home (if android in platforms)')
	parser.add_argument('--blackberry_ndk', help='blackberry NDK home')
	args = parser.parse_args()

	name = args.name.decode("utf-8")
	appid = args.id.decode("utf-8")
	directory = os.path.abspath(os.path.expanduser(args.directory.decode("utf-8")))
	iphone = 'iphone' in args.platforms
	android = 'android' in args.platforms
	mobileweb = 'mobileweb' in args.platforms
	blackberry = 'blackberry' in args.platforms
	android_sdk = None
	blackberry_ndk = None

	if android:
		sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), "android"))
		from androidsdk import AndroidSDK
		# android_sdk is a special case as it's positional and optional
		# and there can be any number of platforms listed before it, it
		# is parsed alongside the platforms.
		# Added --android_sdk for the future, but as current Studio
		# doesn't use it we need to look at the last item of platforms
		# if --android_sdk is not used.
		android_sdk = args.android_sdk or args.platforms[-1]
		android_sdk = android_sdk.decode("utf-8")
		try:
			AndroidSDK(android_sdk)
		except Exception, e:
			print >>sys.stderr, e
			sys.exit(1)

	if blackberry:
		sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), "blackberry"))
		from blackberryndk import BlackberryNDK
		blackberry_ndk = args.blackberry_ndk and args.blackberry_ndk.decode("utf-8")
		try:
			bbndk = BlackberryNDK(blackberry_ndk)
			if blackberry_ndk is None:
				blackberry_ndk = bbndk.getBlackberryNdk()
		except Exception, e:
			print >>sys.stderr, e
			sys.exit(1)

	project_dir = os.path.join(directory,name)
	
	if not os.path.exists(project_dir):
		os.makedirs(project_dir)

	template_dir = os.path.abspath(os.path.dirname(sys._getframe(0).f_code.co_filename))
	all_dir = os.path.abspath(os.path.join(template_dir,'all'))
	
	if not os.path.exists(all_dir):
		all_dir = template_dir

	tiapp = codecs.open(os.path.join(all_dir,'tiapp.xml'),'r','utf-8','replace').read()
	tiapp = tiapp.replace('__PROJECT_ID__',appid)
	tiapp = tiapp.replace('__PROJECT_NAME__',name)
	tiapp = tiapp.replace('__PROJECT_VERSION__','1.0')

	tiapp_file = codecs.open(os.path.join(project_dir,'tiapp.xml'),'w+','utf-8','replace')
	tiapp_file.write(tiapp)
	tiapp_file.close()

	# create the titanium resources
	resources_dir = os.path.join(project_dir,'Resources')
	if not os.path.exists(resources_dir):
		os.makedirs(resources_dir)

	# write out our gitignore
	gitignore = open(os.path.join(project_dir,'.gitignore'),'w')
	# start in 1.4, we can safely exclude build folder from git
	gitignore.write("tmp\n")
	gitignore.close()

	if iphone:
		iphone_resources = os.path.join(resources_dir,'iphone')
		if not os.path.exists(iphone_resources): os.makedirs(iphone_resources)
		iphone_gen = os.path.join(template_dir,'iphone','iphone.py')
		run([sys.executable, iphone_gen, name, appid, directory])

	if android:
		android_resources = os.path.join(resources_dir,'android')
		if not os.path.exists(android_resources): os.makedirs(android_resources)
		android_gen = os.path.join(template_dir,'android','android.py')
		run([sys.executable, android_gen, name, appid, directory, android_sdk])

	if mobileweb:
		mobileweb_resources = os.path.join(resources_dir,'mobileweb')
		if not os.path.exists(mobileweb_resources): os.makedirs(mobileweb_resources)
		mobileweb_gen = os.path.join(template_dir,'mobileweb','mobileweb.py')
		run([sys.executable, mobileweb_gen, name, appid, directory])

	if blackberry:
		blackberry_gen = os.path.join(template_dir,'blackberry','blackberry.py')
		run([sys.executable, blackberry_gen, name, appid, directory, blackberry_ndk])

	# copy LICENSE and README
	for file in ['LICENSE','README']:
		shutil.copy(os.path.join(all_dir,file),os.path.join(project_dir,file))

	# copy RESOURCES
	for file in ['app.js']:
		shutil.copy(os.path.join(all_dir,file),os.path.join(resources_dir,file))

	# copy IMAGES
	for file in ['KS_nav_ui.png', 'KS_nav_views.png']:
		shutil.copy(os.path.join(all_dir,file),os.path.join(resources_dir,file))

if __name__ == '__main__':
	main()

