# Copyright (c) 2012-2019 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib/

import unittest
import array
import binascii
import contextlib
import mmap
import sys

import numpy

#from cybuffer import cybuffer
from memorybuffer import Py_buffer


try:
    buffer
except NameError:
    buffer = memoryview


Py_UNICODE_SIZE = array.array('u').itemsize


class CybufferTest(unittest.TestCase):

    def test_empty_constructor(self):

        with self.assertRaises(TypeError):
            b = Py_buffer()

    def validate_against_memoryview(self, v, b, m, suboffsets=tuple()):

        # Test view properties' data relationships
        self.assertIs(b.obj, v)
        self.assertEqual(b.nbytes, len(m.tobytes()))
        self.assertEqual(b.itemsize, (len(m.tobytes()) // len(v)))
        self.assertEqual(b.ndim, m.ndim)
        self.assertEqual(b.suboffsets, suboffsets)
        self.assertEqual(b.shape, (len(v),))
        self.assertEqual(b.strides, (len(m.tobytes()) // len(v),))

        # Test Python 3+ properties
        self.assertIs(b.obj, m.obj)
        self.assertEqual(b.c_contiguous, m.c_contiguous)
        self.assertEqual(b.f_contiguous, m.f_contiguous)
        self.assertEqual(b.contiguous, m.contiguous)
        self.assertEqual(b.nbytes, m.nbytes)

        # Test methods
        self.assertEqual(b.tobytes(), m.tobytes())
        self.assertEqual(b.hex(), m.hex())

    def test_bytes(self):
        for v in [b"abcdefghi", bytearray(b"abcdefghi")]:
            self._test_bytes(v)
    def _test_bytes(self, v):

        # Initialize buffers
        b = Py_buffer(v)
        m = memoryview(v)

        # Validate format
        self.assertEqual(b.format, m.format)
        self.assertEqual(b.itemsize, m.itemsize)

        # Validate contiguity
        self.assertTrue(b.c_contiguous)
        self.assertTrue(b.f_contiguous)
        self.assertTrue(b.contiguous)

        # Validate permissions
        self.assertEqual(b.readonly, m.readonly)

        # Test methods
        self.assertEqual(b.tolist(), m.tolist())

        self.validate_against_memoryview(v, b, m)

    def test_1d_arrays(self):
        for f in ["b", "B", "h", "H", "i", "I", "l", "L", "q", "Q", "f", "d"]:
            self._test_1d_arrays(f)
    def _test_1d_arrays(self, f):

        # Initialize buffers
        v = array.array(f, [0, 1, 2, 3, 4])
        b = Py_buffer(v)
        m = memoryview(buffer(v))

        # Validate format
        self.assertEqual(b.format, v.typecode)
        self.assertEqual(b.itemsize, v.itemsize)

        # Validate contiguity
        self.assertTrue(b.c_contiguous)
        self.assertTrue(b.f_contiguous)
        self.assertTrue(b.contiguous)

        # Validate permissions
        if isinstance(b, memoryview):
            self.assertTrue(b.readonly)
        else:
            self.assertFalse(b.readonly)

        # Test methods
        self.assertEqual(b.tolist(), v.tolist())

        self.validate_against_memoryview(v, b, m)

    def test_1d_text_arrays(self):
        for f, s in [("c", b"Hello World!"), ("u", u"Hello World!")]:
            self._test_1d_text_arrays(f, s)
    def _test_1d_text_arrays(self, f, s):

        # Skip some newer types
        if f is "c":
            self.skipTest("Format `%s` not available on Python 3" % f)

        # Initialize buffers
        v = array.array(f, s)
        b = Py_buffer(v)
        m = memoryview(buffer(v))

        # Validate format
        self.assertEqual(b.itemsize, v.itemsize)
        if f is "u" and Py_UNICODE_SIZE == 2:
            self.assertEqual(b.format, "H")
        elif f is "u" and Py_UNICODE_SIZE == 4:
            self.assertEqual(b.format, "I")
        elif f is "c":
            self.assertEqual(b.format, "B")

        # Validate contiguity
        self.assertTrue(b.c_contiguous)
        self.assertTrue(b.f_contiguous)
        self.assertTrue(b.contiguous)

        # Validate permissions
        if isinstance(b, memoryview):
            self.assertTrue(b.readonly)
        else:
            self.assertFalse(b.readonly)

        # Test methods
        self.assertEqual(b.tolist(), list(map(ord, v)))

        self.validate_against_memoryview(v, b, m)

    def test_mmap(self):

        with contextlib.closing(mmap.mmap(-1, 10, access=mmap.ACCESS_WRITE)) as v:
            # Initialize buffers
            b = Py_buffer(v)
            m = memoryview(buffer(v))

            # Validate format
            self.assertEqual(b.format, m.format)
            self.assertEqual(b.itemsize, m.itemsize)

            # Validate contiguity
            self.assertTrue(b.c_contiguous)
            self.assertTrue(b.f_contiguous)
            self.assertTrue(b.contiguous)

            # Validate permissions
            self.assertFalse(b.readonly)

            # Test methods
            self.assertEqual(b.tolist(), m.tolist())

            self.validate_against_memoryview(v, b, m)

            # Cleanup to close memory
            del b
            del m

    def test_nd_numpy_arrays(self):
        for s in [(10,), (10, 11), (10, 11, 12)]:
            for o in ["C", "F"]:
                self._test_nd_numpy_arrays(s, o)
    def _test_nd_numpy_arrays(self, s, o):

        # Initialize buffers
        numpy.random.seed(42)
        a = numpy.random.random(s).astype(float, order=o)
        b = Py_buffer(a)

        # Validate identity
        self.assertIs(b.obj, a)

        # Validate shape, size, etc.
        self.assertEqual(b.nbytes, a.nbytes)
        self.assertEqual(b.ndim, a.ndim)
        self.assertEqual(b.suboffsets, tuple())
        self.assertEqual(b.shape, a.shape)
        self.assertEqual(b.strides, a.strides)

        # Validate format
        self.assertEqual(b.format, a.dtype.char)
        self.assertEqual(b.itemsize, a.itemsize)

        # Validate contiguity
        self.assertEqual(b.c_contiguous, a.flags.c_contiguous)
        self.assertEqual(b.f_contiguous, a.flags.f_contiguous)
        self.assertEqual(b.contiguous, (a.flags.c_contiguous or a.flags.f_contiguous))

        # Validate permissions
        self.assertNotEqual(b.readonly, a.flags.writeable)

        # Test methods
        self.assertEqual(b.tobytes(), a.tobytes())
        self.assertEqual(b.tolist(), a.tolist())
        self.assertEqual(b.hex(), a.tobytes().hex())
