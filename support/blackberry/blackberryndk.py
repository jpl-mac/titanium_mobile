#!/usr/bin/python
#
# An autodetection utility for the Blackberry NDK
#
# WARNING: the paths to qde, project and project name must not contain any
#          spaces for the tools to work correctly

import os, sys, platform, subprocess
from argparse import ArgumentParser

class Device:
	''' TODO Mac: Look at how qde works with sim for this class '''
	pass
#	def __init__(self, name, port=-1, emulator=False, offline=False):
#		self.name = name
#		self.port = port
#		self.emulator = emulator
#		self.offline = offline
#
#	def get_name(self):
#		return self.name
#
#	def get_port(self):
#		return self.port
#
#	def is_emulator(self):
#		return self.emulator
#
#	def is_device(self):
#		return not self.emulator
#
#	def is_offline(self):
#		return self.offline

class BlackberryNDK:
	def __init__(self, blackberryNdk):
		self.blackberryNdk = self._findNdk(blackberryNdk)
		if self.blackberryNdk is None:
			raise Exception('No Blackberry NDK directory found')
		self.version = self._findVersion()
		self.qde = self._findQde()
		self._sourceEnvironment()

	def getVersion(self):
		return self.version

	def getBlackberryNdk(self):
		return self.blackberryNdk

	def _findNdk(self, supplied):
		if supplied is not None:
			if os.path.exists(supplied):
				return supplied
			else:
				return None

		if platform.system() == 'Windows':
			# TODO Mac: find out where the NDK installs on windows
			default_dirs = ['C:\\bbndk-2.0.0']
		else:
			default_dirs = ['/Developer/SDKs/bbndk-2.0.0', '/opt/bbndk-2.0.0', '~/bbndk-2.0.0', '~/opt/bbndk-2.0.0']

		for default_dir in default_dirs:
			if os.path.exists(default_dir):
				return default_dir
		return None

	def _findVersion(self):
		infoPath = os.path.join(self.blackberryNdk, 'install', 'info.txt')
		if os.path.exists(infoPath):
			try:
				f = open(infoPath, 'rU')
				for line in f:
					(key, val) = line.split('=', 1)
					if key == 'host':
						f.close()
						return val.strip()
			except IOError, e:
				print >>sys.stderr, e
		return None

	def _sourceEnvironment(self):
		# TODO Mac: Validate the following on windows
		if platform.system() == 'Windows':
			envFile = os.path.join(self.blackberryNdk, 'bbndk-env.bat')
			command = '%s ' % envFile + '&& env'
		else:
			envFile = os.path.join(self.blackberryNdk, 'bbndk-env.sh')
			command = ['bash', '-c', 'source %s && env' % envFile]

		try:
			proc = subprocess.Popen(command, stdout = subprocess.PIPE)
		except OSError, e:
			print >>sys.stderr, e
			return

		for line in proc.stdout:
			# This leaks memory on mac osx, see man putenv
			(key, _, value) = line.partition("=")
			os.environ[key] = value.strip()
		proc.communicate()

	def _findQde(self):
		cmd = 'qde'
		try:
			qnx_host = os.environ.get('QNX_HOST')
		except KeyError:
			print >>sys.stderr, e
			return None

		if platform.system() == 'Windows':
			dir = os.path.join(qnx_host, 'usr', 'qde', 'eclipse')	# TODO Mac: validate actual value
			cmd += '.exe'
		elif platform.system() == 'Darwin':
			dir = os.path.join(qnx_host, 'usr', 'qde', 'eclipse', 'qde.app', 'Contents', 'MacOS')
		elif platform.system() == 'Linux':
			dir = os.path.join(qnx_host, 'usr', 'bin')
		qde = os.path.join(dir, cmd)
		if os.path.exists(qde):
			return qde
		return None

	def _run(self, command):
		assert type(command) is list
		try:
			subprocess.check_output(command, stderr = subprocess.STDOUT)
		except subprocess.CalledProcessError, cpe:
			print >>sys.stderr, cpe, cpe.output
			return
		except OSError, e:
			print >>sys.stderr, e
			return

	def importProject(self, project, workspace = None):
		assert os.path.exists(project)
		if workspace is None:
			workspace = os.path.dirname(project)
		command = [self.qde, '-nosplash', '-application', 'org.eclipse.cdt.managedbuilder.core.headlessbuild', '-consoleLog', '-data', workspace, '-import', project]
		self._run(command)

	def build(self, project, variant):
		assert os.path.exists(project)
		command = ['mkbuild', project, '-variant', variant]
		self._run(command)

	def package(self, package, savePath, projectName):
		command = ['blackberry-nativepackager', '-package', package, 'bar-descriptor.xml', '-e', savePath, projectName, 'icon.png']
		self._run(command)

	def deploy(self, deviceIP, package):
		command = ['blackberry-deploy', '-installApp', '-launchApp', '-device', deviceIP, '-package', package]
		self._run(command)

def __runUnitTests():
	# on windows the double dirname need to be done on 2 lines
	baseDir = os.path.abspath(os.path.dirname(sys.argv[0]))
	baseDir = os.path.dirname(baseDir)
	sys.path.append(os.path.join(baseDir, 'common'))
	from tiunittest import UnitTest
	from tempfile import mkdtemp
	import shutil

	print '\nRunning Unit Tests...\n'

	with UnitTest('Test source environement..'):
		ndk._sourceEnvironment()
		for key in ['QNX_TARGET', 'QNX_HOST', 'QNX_CONFIGURATION', 'MAKEFLAGS', 'PATH']:
			assert key in os.environ

	with UnitTest('Test find qde..'):
		qde = ndk._findQde()
		assert os.path.exists(qde)

	with UnitTest('Test import project with workspace..'):
		workspace = mkdtemp()
		projectSrc = os.path.join(ndk.blackberryNdk, 'target', 'qnx6', 'usr', 'share', 'samples', 'ndk', 'HelloWorldDisplay')
		projectName = 'HelloWorldDisplayMakefile'
		project = os.path.join(workspace, projectName)
		shutil.copytree(projectSrc, project)
		ndk.importProject(project, workspace)
		passed = os.path.exists(os.path.join(workspace, '.metadata'))
		shutil.rmtree(workspace)
		assert passed

	with UnitTest('Test import project no workspace..'):
		workspace = mkdtemp()
		projectSrc = os.path.join(ndk.blackberryNdk, 'target', 'qnx6', 'usr', 'share', 'samples', 'ndk', 'HelloWorldDisplay')
		project = os.path.join(workspace, projectName)
		shutil.copytree(projectSrc, project)
		ndk.importProject(project)
		passed = os.path.exists(os.path.join(workspace, '.metadata'))
		assert passed

	with UnitTest('Test build project (Simulator)..'):
		variant = 'Simulator-Debug'
		ndk.build(project, variant)
		assert os.path.exists(os.path.join(project, 'x86', 'o-g', projectName))

	# TODO Mac: Complete the following unit tests
	# These tests don't work at the moment, we need to figure out how to generate the bar file fisrt
#	with UnitTest('Test package project..'):
#		barPath = os.path.join(project, variant, '%s.bar' % projectName)
#		savePath = os.path.join(project, variant, projectName)
#		ndk.package(barPath, savePath, os.path.basename(project))
#
#	with UnitTest('Test deploy project to simulator (hard-coded ip)..'):
#		ndk.deploy('192.168.135.129', )
#
	with UnitTest('Test build project (Device-Debug)..'):
		variant = 'Device-Debug'
		ndk.build(project, variant)
		assert os.path.exists(os.path.join(project, 'arm', 'o.le-v7-g', projectName))

	with UnitTest('Test build project (Device-Release)..'):
		variant = 'Device-Release'
		ndk.build(project, variant)
		assert os.path.exists(os.path.join(project, 'arm', 'o.le-v7', projectName))

	shutil.rmtree(workspace)

	print '\nFinished Running Unit Tests'
	UnitTest.printDetails()


if __name__ == "__main__":
	parser = ArgumentParser(description = 'Prints the NDK directory and version')
	parser.add_argument('ndk_path', help = 'path to the blackberry ndk', nargs='?')
	parser.add_argument('-t', '--test', help = 'run unit tests', action = 'store_true')
	args = parser.parse_args()

	try:
		ndk = BlackberryNDK(args.ndk_path)
		print "BLACKBERRY_NDK=%s" % ndk.getBlackberryNdk()
		print "BLACKBERRY_NDK_VERSION=%s" % ndk.getVersion()
	except Exception, e:
		print >>sys.stderr, e

	if args.test:
		__runUnitTests()
