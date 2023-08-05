import unittest
from unittest import TestCase

import sys
from itertools import product

from inclusive import range as new_range
from inclusive import slice as new_slice

from builtins import range as old_range
from builtins import slice as old_slice

from builtins import range as RANGE

range = None
slice = None


class TestInclusiveRange(TestCase):
	def test_renamed_builtins_in_tests(self):
		self.assertTrue(range is None)

	def test_one_argument_exclusive(self):
		for n in RANGE(-5, 6):
			a = new_range(n)
			b = old_range(n)
			self.assertEqual(a, b)

	def test_one_argument_inclusive(self):
		for n in RANGE(-5, 6):
			a = new_range[n]
			b = old_range(1, 1 + n)
			self.assertEqual(a, b)

	def test_one_argument_float_exclusive(self):
		try:
			old_range(1.0)
			assert False
		except AssertionError:
			raise
		except Exception as ex:
			with self.assertRaises(type(ex)):
				new_range(1.0)

	def test_one_argument_float_inclusive(self):
		try:
			old_range(0, 1 + 1.0)
			assert False
		except AssertionError:
			raise
		except Exception as ex:
			with self.assertRaises(type(ex)):
				new_range[1.0]

	def test_two_argument_exclusive(self):
		for (m, n) in product(RANGE(-5, 6), repeat=2):
			a = new_range(m, n)
			b = old_range(m, n)
			self.assertEqual(a, b)

	def test_two_argument_inclusive(self):
		for (m, n) in product(RANGE(-5, 6), repeat=2):
			a = new_range[m, n]
			b = old_range(m, 1 + n)
			self.assertEqual(a, b)

	def test_three_argument_exclusive(self):
		for (m, n) in product(RANGE(-5, 6), repeat=2):
			for s in [-2, -1, 1, 2]:
				a = new_range(m, n, s)
				b = old_range(m, n, s)
				self.assertEqual(a, b)

	def test_three_argument_inclusive(self):
		for (m, n) in product(RANGE(-5, 6), repeat=2):
			for s in [-2, -1, 1, 2]:
				a = new_range[m, n, s]
				b = old_range(m, 1 + n, s)
				self.assertEqual(a, b)

	def test_zero_argument_exclusive(self):
		try:
			# Deliberate error
			old_range()
			assert False
		except AssertionError:
			raise
		except Exception as ex:
			# Same error?
			with self.assertRaises(type(ex)):
				new_range()


class TestInclusiveSlice(TestCase):
	def test_renamed_builtins_in_tests(self):
		self.assertTrue(slice is None)

	def test_one_argument_exclusive(self):
		for n in old_range(-5, 6):
			a = new_slice(n)
			b = old_slice(n)
			self.assertEqual(a, b)

	def test_one_argument_inclusive(self):
		for n in old_range(-5, 6):
			a = new_slice[n]
			b = old_slice(1, 1 + n)
			self.assertEqual(a, b)

	def test_one_argument_float_exclusive(self):
		for x in [-1.0, 0.0, 1.0]:
			a = new_slice(x)
			b = old_slice(x)
			self.assertEqual(a, b)

	def test_one_argument_float_inclusive(self):
		for x in [-1.0, 0.0, 1.0]:
			a = new_slice[x]
			b = old_slice(1, 1 + x)
			self.assertEqual(a, b)

	def test_two_argument_exclusive(self):
		for (m, n) in product(RANGE(-5, 6), repeat=2):
			a = new_slice(m, n)
			b = old_slice(m, n)
			self.assertEqual(a, b)

	def test_two_argument_inclusive(self):
		for (m, n) in product(RANGE(-5, 6), repeat=2):
			a = new_slice[m, n]
			b = old_slice(m, 1 + n)
			self.assertEqual(a, b)

	def test_three_argument_exclusive(self):
		for (m, n) in product(RANGE(-5, 6), repeat=2):
			for s in [-2, -1, 1, 2]:
				a = new_slice(m, n, s)
				b = old_slice(m, n, s)
				self.assertEqual(a, b)

	def test_three_argument_inclusive(self):
		for (m, n) in product(RANGE(-5, 6), repeat=2):
			for s in [-2, -1, 1, 2]:
				a = new_slice[m, n, s]
				b = old_slice(m, 1 + n, s)
				self.assertEqual(a, b)


if __name__ == "__main__":
	# https://stackoverflow.com/questions/5360833/how-to-run-multiple-classes-in-single-test-suite-in-python-unit-testing
	suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
	unittest.TextTestRunner(verbosity=3).run(suite)
