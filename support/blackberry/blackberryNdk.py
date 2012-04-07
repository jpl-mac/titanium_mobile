#!/usr/bin/python
#
# An autodetection utility for the Blackberry NDK
#

import os, sys, platform, subprocess
from argparse import ArgumentParser

class Device:
	''' TODO MAc: Look at how qde works with sim for this class '''
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
			default_dirs = ['/Developer/SDKs/bbndk-2.0.0', '/opt/bbndk-2.0.0', '~/bbndk-2.0.0']

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
		except OSError, e:
			print >>sys.stderr, e
			return

		for line in proc.stdout:
			# This leaks memory on mac osx, see man putenv
			(key, _, value) = line.partition("=")
			os.environ[key] = value

	def _findQde(self):
		if platform.system() == 'Windows':
			hostVal = 'win32'	# TODO Mac: validate actual value
		elif platform.system() == 'Darwin':
			hostVal = 'macosx'
		elif platform.system() == 'Linux':
			hostVal = 'linux'

		qde = os.path.join(self.blackberryNdk, 'host', hostVal, 'x86', 'usr', 'qde', 'eclipse', 'qde.app', 'Contents', 'MacOS', 'qde')
		if os.path.exists(qde):
			return qde
		return None


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


# ------------------------------ UNIT TESTS ------------------------------

	if args.test:
		passed = failed = 0

		def _pass():
			global passed
			passed += 1
			print 'OK'

		def _fail():
			global failed
			failed += 1
			print 'FAILED'

		class UnitTest:
			def __init__(self, desc):
				self.desc = desc
			def __enter__(self):
				print self.desc,
			def __exit__(self, exc_type, exc_val, exc_tb):
				if exc_type:
					_fail()
				else:
					_pass()
				return True	# Return true so exceptions are dropped

		print '\nRunning Unit Tests...\n'

		with UnitTest('Test source environement..'):
			ndk._sourceEnvironment()
			for key in ['QNX_TARGET', 'QNX_HOST', 'QNX_CONFIGURATION', 'MAKEFLAGS', 'DYLD_LIBRARY_PATH', 'PATH']:
				assert key in os.environ

		with UnitTest('Test find qde..'):
			qde = ndk._findQde()
			assert os.path.exists(qde)
			# run -version




		print '\nFinished Running Unit Tests'
		print '\t%s Test%s Passed ' % (passed, 's' if passed > 1 else '')
		print '\t%s Test%s Failed ' % (failed, 's' if failed > 1 else '')
