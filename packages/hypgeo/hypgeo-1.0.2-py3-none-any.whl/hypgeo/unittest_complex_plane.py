import unittest
import sys
import numpy as np
from hypgeo.complex_plane import _i, ComplexNumber, RootOfUnity
from hypgeo.helpers.field import *

NUMBER_TESTS = 1000
ZERO = ComplexNumber(.0, .0)
ONE = ComplexNumber(1.0, .0)

class TestComplexNumber(unittest.TestCase):
    def test_field_laws(self):
        A = ComplexNumber.rnd(-50, +50, NUMBER_TESTS)
        B = ComplexNumber.rnd(-50, +50, NUMBER_TESTS)
        C = ComplexNumber.rnd(-50, +50, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            a, b, c = A[i], B[i], C[i]
    
            self.assertEqual(associative_property_add(a, b, c), ZERO)
            self.assertEqual(commutative_portperty_add(a, b, c), ZERO)
            self.assertEqual(associative_property_mul(a, b, c), ZERO)
            self.assertEqual(commutative_portperty_mul(a, b, c), ZERO)
            self.assertEqual(right_distributive(a, b, c), ZERO)
            self.assertEqual(left_distributive(a, b, c), ZERO)

    def test_identity(self):
        self.assertEqual(_i * _i, - ONE)

    def test_inverse(self):
        Z = ComplexNumber.rnd(-50, +50, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(Z[i].inv(), Z[i].conj() / (Z[i].norm_sq()))

    def test_inverse_mul(self):
        Z = ComplexNumber.rnd(-50, +50, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(inv_element_mul(Z[i], Z[i].inv(), ONE), ZERO)

    def test_inverse_add(self):
        Z = ComplexNumber.rnd(-50, +50, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(inv_element_add(Z[i], - Z[i], ZERO), ZERO)

    def test_neutral_add(self):
        Z = ComplexNumber.rnd(-50, +50, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(neutral_element_add(Z[i], ZERO), ZERO)

    def test_neutral_mul(self):
        Z = ComplexNumber.rnd(-50, +50, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(neutral_element_mul(Z[i], ONE), ZERO)

    def test_real_im_conj1(self):
        Z = ComplexNumber.rnd(-50, +50, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(Z[i], ComplexNumber(Z[i].re, Z[i].im))
            self.assertEqual((Z[i] + Z[i].conj()) * .5, Z[i].re)
            self.assertEqual((Z[i] - Z[i].conj()) / (_i * 2.0), Z[i].im)
            self.assertEqual(Z[i], Z[i].conj().conj())
            self.assertEqual(Z[i].conj().re, Z[i].re)
            self.assertEqual(Z[i].conj().im, - Z[i].im)

    def test_real_im_conj2(self):
        A = ComplexNumber.rnd(-50, +50, NUMBER_TESTS)
        B = ComplexNumber.rnd(-50, +50, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual((A[i] + B[i]).conj(), A[i].conj() + B[i].conj())
            self.assertEqual((A[i] * B[i]).conj(), A[i].conj() * B[i].conj())
            self.assertEqual((A[i] / B[i]).conj(), A[i].conj() / B[i].conj())

    def test_root_of_unity(self):
        for n in range(0, 100):
            for k in range(0, n):
                self.assertEqual(RootOfUnity(k, n) ** n, ONE)

if __name__ == '__main__':
    unittest.main()