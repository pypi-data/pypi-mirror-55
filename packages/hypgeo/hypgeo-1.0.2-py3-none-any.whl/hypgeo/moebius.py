import numpy as np
from hypgeo.complex_plane import *
from hypgeo.geometry import *

class MoebGen:
    """A class representing general Moebius transformations (of the connected unit component) and their operation on the upper half plane."""
    
    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def c(self):
        return self._c

    @property
    def d(self):
        return self._d

    @property
    def Det(self):
        return self._det

    def IsGenMoeb(op):
        def _op(inst, o):
            assert isinstance(o, MoebGen), "%s is not of type \"MoebGen\"!" % str(o)
            return op(inst, o)
        return _op

    def __init__(self, a, b, c, d):
        """
        Parameters
        ----------
        a : float or (real) ComplexNumer
            coefficient c_11 in matrix representation of moebius transformation via SL(2, R)
            given by ( (c_11, c_12), (c_21, c_22))
        b : float or (real) ComplexNumerr
            coefficient c_12 in matrix representation
        c : float or (real) ComplexNumerr
            coefficient c_21 in matrix representation
        d : float or ComplexNumer
            coefficient c_22 in matrix representation
        """

        #check whether coefficients are real
        assert type(a) is float or type(a) is np.float64, 'A must be of type float!'
        assert type(b) is float or type(b) is np.float64, 'A must be of type float!'
        assert type(c) is float or type(c) is np.float64, 'A must be of type float!'
        assert type(d) is float or type(d) is np.float64, 'A must be of type float!' 
        
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        self._det = self._a * self._d - self._b * self._c

    def __call__(self, z):
        if type(z) is np.array or type(z) is np.ndarray:
            assert len(z) == 2, "z has wrong dimension!"
            z = ComplexNumber(z[0], z[1])
        if isinstance(z, GeodesicLine):
            return self.map_line(z)
        assert type(z) is ComplexNumber, 'z has to be a complex number!'

        if math.isclose(self._det, - 1.0, abs_tol=1e-09):
            z = z.conj()
        return (z * self._a + self._b) / (z * self._c + self._d)

    def clone(self):
        return MoebGen(self._a, self._b, self._c, self._d)

    def map_line(self, l):  
        z_0, z_1 = l.get_two_points()      
        u_0, u_1 = MoebGen.__call__(self, z_0), MoebGen.__call__(self, z_1)
        return GeodesicLine.line_trough(u_0, u_1)

    def inv(self):
        """Returns the (group) inverse of instance."""
        return MoebGen(self._d / self._det, - self._b / self._det, - self._c / self._det, self._a / self._det)

    @IsGenMoeb
    def __mul__(self, o):
        """Right multiplicates of instance transformation with o.

        Parameters
        ----------
        o : Moeb
            Moebius transformation multiplied with instance from right

        Returns
        -------
        Moeb
            Right multiplication of instance transformation with o
        """ 
        return MoebGen(self._a * o.a + self._b * o.c, self._a * o.b + self._b * o.d, 
            self._c * o.a + self._d * o.c, self._c * o.b + self._d * o.d)

    def conj(self, o):
        """Returns the (group) conjugation of instance transformation with o.

        Parameters
        ----------
        o : Moeb
            Moebius transformation used in conjugation of instance.

        Returns
        -------
        Moeb
            (Group) conjugation of instance transformation by multiplying o from the right and its inverse
            from the left
        """ 
        return (o.inv()) * self * o

    def __truediv__(self, o):
        """Multiplies instance from left with the inverse of o.

        Parameters
        ----------
        o : Moeb
            Moebius transformation to be inverted and multiplied from left with instance o

        Returns
        -------
        ComplexNumber
            Left division of instance by o
        """ 
        return self * o.inv()

    def __pow__(self, n):
        """Returns the n-th power of instance transformation with o.

        Parameters
        ----------
        n : int
            Power

        Returns
        -------
        Moeb
            N-th power of instance transformation with o
        """ 

        if n > 0:
            pow = self.clone()
            for i in range(1, n):
                pow *= self
        elif n == 0:
            return moeb_id
        else:
            pow = self.clone().inv()
            inv = self.inv().clone()
            for i in range(1, - n):
                pow *= inv

        return pow

    def __str__(self):
        """Returns a string representation of of instance."""
        return "((a = {}, b={}), (c = {}, d={}))".format(self._a, self._b, self._c, self._d)

    def __eq__(self, o):
        if type(o) is not MoebGen:
            return False
        elif math.isclose(self._a, o.a, abs_tol=1e-09) and math.isclose(self._b, o.b, abs_tol=1e-09) \
            and math.isclose(self._c, o.c, abs_tol=1e-09) and math.isclose(self._d, o.d, abs_tol=1e-09):
            return True
        else:
            return False

moeb_id = MoebGen(1.0, .0, .0, 1.0)

class Moeb(MoebGen):
    def __init__(self, a, b, c, d):
        #check if a * d - b * c = 1
        assert math.isclose(a * d - b * c, 1.0, abs_tol=1e-09), 'Coefficients do not satisfy determinant condition!'
        MoebGen.__init__(self, a, b, c, d)
    
    def rnd(min, max, samples):
        rnd_moeb = []

        for i in range(0, samples):
            coeffs = np.random.uniform(min, max, 4)
            det = coeffs[0] * coeffs[3] - coeffs[1] * coeffs[2]
            while det == .0:
                coeffs = np.random.uniform(min, max, 4)
            if det < .0:
                coeffs[0] *= - 1.0
                coeffs[1] *= - 1.0
                det = coeffs[0] * coeffs[3] - coeffs[1] * coeffs[2]
            coeffs = coeffs / math.sqrt(det)
            rnd_moeb.append(Moeb(coeffs[0], coeffs[1], coeffs[2], coeffs[3]))

        return rnd_moeb

    def plot(self, rectanlge):
        return None

class MoebConj(MoebGen):
    """A class representing Moebius transformations (of the second connected component) and their operation on the upper half plane."""
    def __init__(self, a, b, c, d):
        #check if a * d - b * c = - 1
        assert math.isclose(a * d - b * c, - 1.0, abs_tol=1e-09), 'Coefficients do not satisfy determinant condition!'
        MoebGen.__init__(self, a, b, c, d)
    
    def rnd(min, max, samples):
        rnd_moeb = []

        for i in range(0, samples):
            coeffs = np.random.uniform(min, max, 4)
            det = coeffs[0] * coeffs[3] - coeffs[1] * coeffs[2]
            while det == .0:
                coeffs = np.random.uniform(min, max, 4)
            if det > .0:
                coeffs[0] *= - 1.0
                coeffs[1] *= - 1.0
                det = coeffs[0] * coeffs[3] - coeffs[1] * coeffs[2]
            coeffs = coeffs / math.sqrt(- det)
            rnd_moeb.append(MoebConj(coeffs[0], coeffs[1], coeffs[2], coeffs[3]))

        return rnd_moeb

class MoebCorr(Moeb):
    def __init__(self, a, b, c, d, rho):
        self._rho = rho
        Moeb.__init__(self, a, b, c, d)

    def __call__(self, z):
        z_x = z.real_part
        z_y = z.imaginary_part
        u = z_x / self._rho + math.sqrt(1.0 - self._rho * self._rho) / self._rho * z_y
        v = z_y
        z = ComplexNumber(u, v)
        w = Moeb.__call__(self, z)
        w_x = w.real_part
        w_y = w.imaginary_part
        u = self._rho * w_x + math.sqrt(1.0 - self._rho * self._rho) * w_y
        v = w_y
        return ComplexNumber(u, v)






