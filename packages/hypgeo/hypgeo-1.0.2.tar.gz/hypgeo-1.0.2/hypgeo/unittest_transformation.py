import unittest
import numpy as np

from hypgeo.complex_plane import _i, ComplexNumber, RootOfUnity
from hypgeo.transformations import *
from hypgeo.moebius import moeb_id
from hypgeo.geometry import *

NUMBER_TESTS = 1000
ZERO = ComplexNumber(.0, .0)

class TestTransfomations(unittest.TestCase):
    def test_moeb_to(self):
        U = ComplexNumber.rnd(.0, +50, NUMBER_TESTS)
        V = ComplexNumber.rnd(.0, +50, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            u, v = U[i], V[i]
            self.assertEqual(moeb_to(u, v)(u) - v, ZERO)

    def test_refl_0(self):
        R = np.random.uniform(.0, 20.0, NUMBER_TESTS)

        for r in R:
            self.assertEqual(refl_0(r) * refl_0(r), moeb_id)
            self.assertEqual(refl_0(r) * refl_0(r), moeb_id)

    def test_circ_to_circ(self):
        C0 = HalfCircle.rnd(10.0, - 10.0, + 10.0, NUMBER_TESTS)
        C1 = HalfCircle.rnd(10.0, - 10.0, + 10.0, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(line_to_line(C0[i], C1[i])(C0[i]), C1[i])

    def test_vert_to_vert(self):
        V0 = Vertical.rnd(- 10.0, + 10.0, NUMBER_TESTS)
        V1 = Vertical.rnd(- 10.0, + 10.0, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(line_to_line(V0[i], V1[i])(V0[i]), V1[i])

    def test_vert_to_circ(self):
        V = Vertical.rnd(- 10.0, + 10.0, NUMBER_TESTS)
        C = HalfCircle.rnd(10.0, - 10.0, + 10.0, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(vert_to_circ(V[i], C[i])(V[i]), C[i])

    def test_circ_to_vert(self):
        C = HalfCircle.rnd(10.0, - 10.0, + 10.0, NUMBER_TESTS)
        V = Vertical.rnd(- 10.0, + 10.0, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(circ_to_vert(C[i], V[i])(C[i]), V[i])
    
    def test_refl_circ(self):
        C = HalfCircle.rnd(7.5, - 7.5, + 7.5, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(refl(C[i])(C[i]), C[i])
            self.assertEqual(refl(C[i]) * refl(C[i]), moeb_id)

            for n in np.random.randint(-5, 5, 50):
                self.assertEqual(refl(C[i]) ** n, refl(C[i]) ** (n % 2))
    
    def test_refl_0(self):
        for r in np.random.uniform(.0 , + 10.0, NUMBER_TESTS):
            self.assertEqual(refl_0(r)(unit_circle_r(r)), unit_circle_r(r))
            self.assertEqual(refl_0(r) * refl_0(r), moeb_id)

            for n in np.random.randint(-5, 5, 50):
                self.assertEqual(refl_0(r) ** n, refl_0(r) ** (n % 2))

    def test_ellip(self):
        S = np.random.uniform(- 10.0, + 10.0, NUMBER_TESTS)
        T = np.random.uniform(- 10.0, + 10.0, NUMBER_TESTS)
        Z = HalfSpace.rnd(- 10.0, + 10.0, 10.0, NUMBER_TESTS)
        
        for i in range(0, NUMBER_TESTS):
            self.assertEqual(ellip(S[i], Z[i]) * ellip(T[i], Z[i]), ellip(S[i] + T[i], Z[i]))
            self.assertEqual(ellip(S[i], Z[i]) * ellip(- S[i], Z[i]), moeb_id)

    def test_loxod(self):
        S = np.random.uniform(- 10.0, + 10.0, NUMBER_TESTS)
        T = np.random.uniform(- 10.0, + 10.0, NUMBER_TESTS)
        
        for i in range(0, NUMBER_TESTS):
            self.assertEqual(loxod(S[i]) * loxod(T[i]), loxod(S[i] + T[i]))
            self.assertEqual(loxod(S[i]) * loxod(- S[i]), moeb_id)

    def test_parab(self):
        S = np.random.uniform(- 10.0, + 10.0, NUMBER_TESTS)
        T = np.random.uniform(- 10.0, + 10.0, NUMBER_TESTS)
        
        for i in range(0, NUMBER_TESTS):
            self.assertEqual(parab(S[i]) * parab(T[i]), parab(S[i] + T[i]))
            self.assertEqual(parab(S[i]) * parab(- S[i]), moeb_id)
          
if __name__ == '__main__':
    unittest.main()