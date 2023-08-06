import unittest
import numpy as np

from hypgeo.complex_plane import _i, ComplexNumber, RootOfUnity
from hypgeo.transformations import line_to_line, moeb_to, refl_0, vert_to_circ, circ_to_vert
from hypgeo.moebius import moeb_id
from hypgeo.geometry import Line

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
        C0 = Line.rnd_c(10.0, - 10.0, + 10.0, NUMBER_TESTS)
        C1 = Line.rnd_c(10.0, - 10.0, + 10.0, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(line_to_line(C0[i], C1[i])(C0[i]), C1[i])

    def test_vert_to_vert(self):
        V0 = Line.rnd_v(- 10.0, + 10.0, NUMBER_TESTS)
        V1 = Line.rnd_v(- 10.0, + 10.0, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(line_to_line(V0[i], V1[i])(V0[i]), V1[i])

    """
    def test_vert_to_circ(self):
        V = Line.rnd_v(- 10.0, + 10.0, NUMBER_TESTS)
        C = Line.rnd_c(10.0, - 10.0, + 10.0, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(vert_to_circ(V[i], C[i])(V[i]), C[i])

    def test_circ_to_vert(self):
        V = Line.rnd_v(- 10.0, + 10.0, NUMBER_TESTS)
        C = Line.rnd_c(10.0, - 10.0, + 10.0, NUMBER_TESTS)

        for i in range(0, NUMBER_TESTS):
            self.assertEqual(circ_to_vert(C[i], V[i])(C[i]), V[i])
            """


       
   
if __name__ == '__main__':
    unittest.main()