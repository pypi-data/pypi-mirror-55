import unittest
from hypgeo.moebius import Moeb, MoebConj, moeb_id
from hypgeo.helpers.group import *

NUMBER_TESTS = 1000

class TestMoebiusTransformation(unittest.TestCase):
    def test_associative_law(self):
        A = Moeb.rnd(-50, +50, NUMBER_TESTS)
        B = Moeb.rnd(-50, +50, NUMBER_TESTS)
        C = Moeb.rnd(-50, +50, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            a, b, c = A[i], B[i], C[i]    
            self.assertEqual(associative_property(a, b, c), moeb_id)

    def test_neutral_element(self):
        M = Moeb.rnd(-50, +50, NUMBER_TESTS)

        for m in M:
            self.assertEqual(neutral_element_r(m, moeb_id), moeb_id)
            self.assertEqual(neutral_element_l(m, moeb_id), moeb_id)

    def test_inv_element(self):
        M = Moeb.rnd(-50, +50, NUMBER_TESTS)

        for m in M:
            self.assertEqual(inv_element_r(m, m.inv()), moeb_id)
            self.assertEqual(inv_element_r(m, m.inv()), moeb_id)

    def test_associative_law_conj(self):
        A = MoebConj.rnd(-50, +50, NUMBER_TESTS)
        B = MoebConj.rnd(-50, +50, NUMBER_TESTS)
        C = MoebConj.rnd(-50, +50, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            a, b, c = A[i], B[i], C[i]   
            self.assertEqual(associative_property(a, b, c), moeb_id)

    def test_neutral_element_conj(self):
        M = MoebConj.rnd(-50, +50, NUMBER_TESTS)

        for m in M:
            self.assertEqual(neutral_element_r(m, moeb_id), moeb_id)
            self.assertEqual(neutral_element_l(m, moeb_id), moeb_id)

    def test_inv_element_conj(self):
        M = MoebConj.rnd(-50, +50, NUMBER_TESTS)

        for m in M:
            self.assertEqual(inv_element_r(m, m.inv()), moeb_id)
            self.assertEqual(inv_element_r(m, m.inv()), moeb_id)


if __name__ == '__main__':
    unittest.main()

