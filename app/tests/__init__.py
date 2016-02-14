import unittest

from mpos import app


class BaseTest(unittest.TestCase):

	def setUp(self):
		self.client = app.test_client()

	def tearDown(self):
		pass

	def test_base(self):
		print 'base test initialized'
