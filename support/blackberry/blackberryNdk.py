#!/usr/bin/python
#
# An autodetection utility for the Blackberry NDK
#

import os, sys, platform, shlex, subprocess
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
			return supplied

		if platform.system() == 'Windows':
			# TODO Mac: find out where the NDK installs on windows
			default_dirs = ['C:\\bbndk', 'C:\\Program Files\\bbndk-2.0.0']
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
		# TODO Mac: Adapt the following for windows
		envFile = os.path.join(self.blackberryNdk, 'bbndk-env.sh')
		command = ['bash', '-c', 'source %s && env' % envFile]
		try:
			proc = subprocess.Popen(command, stdout = subprocess.PIPE)
			#proc.communicate()
			proc.wait()
		except OSError, e:
			print >>sys.stderr, e
			return

		for line in proc.stdout:
			# This leaks memory on mac osx, see man putenv
			(key, _, value) = line.partition("=")
			os.environ[key] = value.strip()
		#pprint.pprint(dict(os.environ))

	def _findQde(self):
		cmd = 'qde'
		if platform.system() == 'Windows':
			subdir = os.path.join('win32', 'x86', 'usr', 'bin')	# TODO Mac: validate actual value
			cmd += '.exe'
		elif platform.system() == 'Darwin':
			subdir = os.path.join('macosx', 'x86', 'usr', 'qde', 'eclipse', 'qde.app', 'Contents', 'MacOS')
		elif platform.system() == 'Linux':
			subdir = os.path.join('linux', 'x86', 'usr', 'bin')

		qde = os.path.join(self.blackberryNdk, 'host', subdir, 'qde')
		if os.path.exists(qde):
			return qde
		return None

	def importProject(self, project, workspace = None):
		print 'jp 1', project
		assert os.path.exists(project)
		print 'jp 2'
		if workspace is None:
			print 'jp 3'
			workspace = os.path.dirname(project)
			print 'jp 4'
		print 'jp 5', workspace
		command_line = '%s -nosplash -application org.eclipse.cdt.managedbuilder.core.headlessbuild -consoleLog -data %s -import %s' % (self.qde, workspace, project)
		print 'jp 6', command_line
		command = shlex.split(command_line)
		print 'jp 7'
		
		try:
			print 'jp 8'
			#subprocess.check_output(command, stderr = subprocess.STDOUT)#.communicate()
			proc = subprocess.Popen(command, stderr = subprocess.STDOUT)#.communicate()
			proc.wait()
			print 'jp 9'
		except OSError, e:
			print 'jp 10'
			print >>sys.stderr, e
			print 'jp 11'
			return
		print 'jp 12'

def __runUnitTests():
	baseDir = os.path.abspath(os.path.dirname(os.path.dirname(sys.argv[0])))
	sys.path.append(os.path.join(baseDir, 'common'))
	from tiunittest import UnitTest
	from tempfile import mkdtemp
	import shutil

	print '\nRunning Unit Tests...\n'

	with UnitTest('Test source environement..'):
		ndk._sourceEnvironment()
		for key in ['QNX_TARGET', 'QNX_HOST', 'QNX_CONFIGURATION', 'MAKEFLAGS', 'DYLD_LIBRARY_PATH', 'PATH']:
			assert key in os.environ

	with UnitTest('Test find qde..'):
		qde = ndk._findQde()
		assert os.path.exists(qde)

	with UnitTest('Test import project with workspace..'):
		workspace = mkdtemp()
		projectSrc = os.path.join(ndk.blackberryNdk, 'target', 'qnx6', 'usr', 'share', 'samples', 'ndk', 'HelloWorldDisplay')
		project = os.path.join(workspace, 'HelloWorldDisplay')
		shutil.copytree(projectSrc, project)
		ndk.importProject(project, workspace)
		passed = os.path.exists(os.path.join(workspace, '.metadata'))
		shutil.rmtree(workspace)
		assert passed

	with UnitTest('Test import project no workspace..'):
		workspace = mkdtemp()
		projectSrc = os.path.join(ndk.blackberryNdk, 'target', 'qnx6', 'usr', 'share', 'samples', 'ndk', 'HelloWorldDisplay')
		project = os.path.join(workspace, 'HelloWorldDisplay')
		shutil.copytree(projectSrc, project)
		ndk.importProject(project)
		passed = os.path.exists(os.path.join(workspace, '.metadata'))
		shutil.rmtree(workspace)
		assert passed


	print '\nFinished Running Unit Tests'
	UnitTest.printDetails()


if __name__ == "__main__":
	parser = ArgumentParser(description = 'Prints the NDK directory and version')
	parser.add_argument('ndk_path', help = 'path to the blackberry ndk', nargs='?')
	parser.add_argument('-t', '--test', help = 'run unit tests', action = 'store_true')
	args = parser.parse_args()
	#print 'JP', args, args.ndk_path

	try:
		ndk = BlackberryNDK(args.ndk_path)
		print "BLACKBERRY_NDK=%s" % ndk.getBlackberryNdk()
		print "BLACKBERRY_NDK_VERSION=%s" % ndk.getVersion()
	except Exception, e:
		print >>sys.stderr, e

	if args.test:
		__runUnitTests()
