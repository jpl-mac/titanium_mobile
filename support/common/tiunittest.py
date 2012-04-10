#!/usr/bin/python
#
# A context manager class to help writing unit tests, failure is determined if
# an exception is raised within the with statement
#
# EXAMPLE:
#
# with UnitTest(<Test description>):
#     foo()
#     assert(bar)
#
# # Print the number of passed and failed tests
# UnitTest.printDetails()
#

from traceback import format_exception

class UnitTest:
	passed = failed = 0

	def __init__(self, desc):
		self.desc = desc

	def __enter__(self):
		print self.desc,

	def __exit__(self, exc_type, exc_val, exc_tb):
		if exc_type:
			UnitTest._fail()
			# Uncomment the following lines to debug failing unit tests
			for line in format_exception(exc_type, exc_val, exc_tb):
				print '\t', line,
		else:
			UnitTest._pass()
		return True	# Return true so exceptions are dropped

	@staticmethod
	def _pass():
		UnitTest.passed += 1
		print 'OK'

	@staticmethod
	def _fail():
		UnitTest.failed += 1
		print 'FAILED'

	@staticmethod
	def printDetails():
		print '\t%s Test%s Passed ' % (UnitTest.passed, 's' if UnitTest.passed > 1 else '')
		print '\t%s Test%s Failed ' % (UnitTest.failed, 's' if UnitTest.failed > 1 else '')
