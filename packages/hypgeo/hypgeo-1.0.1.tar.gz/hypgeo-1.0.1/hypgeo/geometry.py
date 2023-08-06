import enum
from hypgeo.complex_plane import *
import math

class LineType(enum.Enum):
    CIRCLE = 1
    VERTICAL = 2

class Line:
    """A class representing geodesic lines (perpendicular half circles and perpendicular lines) in upper half plane HPlus."""
    @property
    def Radius(self):       
        return self._radius

    @property
    def Center(self):
        return self._center

    @property
    def Absc(self):
        return self._absc

    @property
    def Type(self):
        return self._type

    @property
    def z0(self):
        return self._z0

    @property
    def z1(self):
        return self._z1

    def __init__(self, z0, z1):
        """
        Parameters
        ----------
        z0 : ComplexNumber
            First complex number defining geodesic line
        z1 : ComplexNumber
            Second complex number defining geodesic line
        """

        assert z0 != z1, "zo and z1 have to be different in order to determine a geodesic line in upper half plane!"
        assert type(z0) is ComplexNumber, "z0 is not of type \"ComplexNumber\"!"
        assert type(z1) is ComplexNumber, "z1 is not of type \"ComplexNumber\"!"
        assert z0 != z1, "A line in HPlus can only be determined by two different complex numbers!"
        assert z0.im > 0, "z0 is not contained in HPlus!"
        assert z1.im > 0, "z1 is not contained in HPlus!"

        self._z0 = z0
        self._z1 = z1

        if self._z0.re == self._z1.re:
            self._type = LineType.VERTICAL
            self._absc = self._z0.re
            self._center = None
            self._radius = float('inf')
        else:
            self._type = LineType.CIRCLE
            self._absc = None
            x0 = self._z0.re
            y0 = self._z0.im
            x1 = self._z1.re
            y1 = self._z1.im
            self._center = 1.0 / 2.0 * (y1 ** 2 - y0 ** 2 - x0 ** 2 + x1 ** 2) / (x1 - x0)
            self._radius = 1.0 / ( 2.0 * (abs(x1 - x0))) * math.sqrt(((x1 - x0) ** 2 + (y1 - y0) ** 2) * ((x1 - x0) ** 2 + (y1 + y0) ** 2))

    def __eq__(self, o):
        if type(o) != Line:
            return False
        elif o.Type != self._type:
            return False
        else:
            if o.Type == LineType.VERTICAL:
                if math.isclose(self._absc, o.Absc, abs_tol=1e-09):
                    return True
                else: 
                    return False
            else:
                if math.isclose(self._radius, o.Radius, abs_tol=1e-09) and math.isclose(self._center, o.Center, abs_tol=1e-09):
                    return True
                else: 
                    return False

    def rnd_c(max_r, min_c, max_c, samples):
        rnd_c = []
        R, C = np.random.uniform(.0, max_r, samples), np.random.uniform(min_c, max_c, samples)

        for i in range(0, samples):
            z_0, z_1 = ComplexNumber(C[i] + R[i] * math.sin(math.pi / 4.0), R[i] * math.cos(math.pi / 4.0)), \
                ComplexNumber(C[i] - R[i] * math.sin(math.pi / 4.0), R[i] * math.cos(math.pi / 4.0))        
            rnd_c.append(Line(z_0, z_1))

        return rnd_c

    def rnd_v(min_absc, max_absc, samples):
        rnd_v = []
        Absc = np.random.uniform(min_absc, max_absc, samples)

        for i in range(0, samples):
            z_0, z_1 = ComplexNumber(Absc[i], 1.0), ComplexNumber(Absc[i], 31.0)        
            rnd_v.append(Line(z_0, z_1))

        return rnd_v

unit_circle = Line(ComplexNumber(- 1.0 / (math.sqrt(2.0)), 1.0 / (math.sqrt(2.0))), ComplexNumber(+ 1.0 / (math.sqrt(2.0)), 1.0 / (math.sqrt(2.0)))) 
