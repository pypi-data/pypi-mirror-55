import math
import numpy as np

def CheckType(operation):
    def _operation(instance, o):
        assert type(o) is ComplexNumber or type(o) is float or type(o) is np.float64 or type(o) \
            is int or isinstance(o, ComplexNumber), "%s is not of type \"ComplexNumber\" or \"float\" or \"int\"!" % str(o)
        return operation(instance, o)
    return _operation

def MapFloat(operation):
    def _operation(instance, o):
        if type(o) is float or type(o) is np.float64 or type(o) is int:
            o = ComplexNumber(float(o), 0.0)
        return operation(instance, o)
    return _operation

class ComplexNumber:
    """A class representing complex numbers and their algebraic operations."""

    @property
    def re(self):
        return self._re

    @property
    def im(self):
        return self._im

    def __init__(self, re, im):
        """
        Parameters
        ----------
        real_part : float
            The real part of the complex number
        imaginary_part : float
            The imaginary part of the complex number
        """

        self._re = re
        self._im = im

    @CheckType
    @MapFloat
    def __add__(self, o):
        """Adds two complex numbers.

        Parameters
        ----------
        o : ComplexNumber
            Complex number to be added to instance

        Returns
        -------
        ComplexNumber
            Sum of instance and o
        """

        ret = ComplexNumber(self._re + o.re, self._im + o.im)
        return ret

    @CheckType
    @MapFloat
    def __sub__(self, o): 
        """Substracts o from instance.

        Parameters
        ----------
        o : ComplexNumber
            Complex number to be substracted from instance

        Returns
        -------
        ComplexNumber
            Difference between instance and o
        """    
        return ComplexNumber(self._re - o.re, self._im - o.im)

    @CheckType
    @MapFloat
    def __mul__(self, o):
        """Multiplicates two complex numbers.

        Parameters
        ----------
        o : ComplexNumber
            Complex number to be multiplicated with instance

        Returns
        -------
        ComplexNumber
            Product of instance and o
        """ 
        return ComplexNumber(self._re * o.re - self._im * o.im,
            self._re * o.im + o.re * self._im)
    
    @CheckType
    def __pow__(self, n):
        """Returns the n-th power of the instance.

        Parameters
        ----------
        n : int
            Power

        Returns
        -------
        ComplexNumber
            N-th power of instance
        """ 

        ret = self.copy()
        for i in range(1, n):
            ret *= self
        
        return ret

    @CheckType
    @MapFloat
    def __truediv__(self, o):
        """Divides instance by o.

        Parameters
        ----------
        o : ComplexNumber
            Complex number to be used as divisor

        Returns
        -------
        ComplexNumber
            Division between of instance by o
        """ 
        if type(o) is float or type(o) is np.float64:
            return ComplexNumber(self._re / o, self._im / o)

        norm_sq_inv = 1 / o.norm_sq()
        return ComplexNumber(self._re * o.re + self._im * o.im,
            - self._re * o.im + o.re * self._im) * norm_sq_inv

    def __str__(self):
        if self._re == .0 and self._im == .0:
            return "0.0"
        elif self._re == .0:
            return "{} * i".format(str(self._im)) 
        elif self._im == .0:
            return "{}".format(str(self._re)) 
        else:
            return "{} + {} * i".format(str(self._re), str(self._im))

    def __eq__(self, o):
        if type(o) is float or type(o) is np.float64:
            if math.isclose(self._re, o, abs_tol=1e-09) and math.isclose(self._im, .0, abs_tol=1e-09):
                return True 
            else:
                return False
        elif type(o) is not ComplexNumber:
            return False
        elif math.isclose(self._re, o.re, abs_tol=1e-09) and math.isclose(self._im, o.im, abs_tol=1e-09):
            return True
        else:
            return False

    def is_real(self):
        if math.isclose(self._im, .0, abs_tol=1e-09):
            return True, self._re

    def __neg__(self):
        return ComplexNumber(- self._re, - self._im)

    def copy(self):
        """Returns a copy of the instance."""
        return ComplexNumber(self._re, self._im)

    def norm_sq(self):
        """Returns the squared norm of the instance."""
        return self._re * self._re + self._im * self._im

    def norm(self):
        """Returns the norm of the instance."""
        return math.sqrt(self.norm_sq_inv())

    def conj(self):
        """Returns the complex conjugate of instance."""
        return ComplexNumber(self._re, - self._im)

    def inv(self):
        """Returns the inverse of instance."""
        return self.conj() / self.norm_sq()

    def to_vec(self):
        """Returns instance as np.array vector."""
        return np.array([self._re, self._im])
    
    def from_vec(vec):
        """Converts two dimensional float array into Complexnumber.

        Parameters
        ----------
        vector : list, np.array
            input enumerable to be converted to ComplexNumber

        Returns
        -------
        ComplexNumber
            Enumerable converted to ComplexNumber
        """ 
        return ComplexNumber(vec[0], vec[1])

    def rnd(min, max, samples):
        """Returns an array with length n=samples of random complex numbers whose real and imaginary parts
            are bounded by min from below and by max from above.

        Parameters
        ----------
        min : float
            lower boundary for real and imaginary part of randomly generated complex numbers  
        max : float
            upper boundary for real and imaginary part of randomly generated complex numbers 

        Returns
        -------
        ComplexNumber
            Array of size n=samples of bounded, random complex numbers
        """ 
        rnd_z = []
        rnds = np.random.uniform(min, max, 2 * samples)
        for i in range(0, samples):
            rnd_z.append(ComplexNumber(rnds[2 * i], rnds[2 * i + 1]))

        return rnd_z

    def rnd_in_HPlus(min_x, max_x, max_y, samples):
        """Returns an array with length n=samples of random complex numbers in upper half space whose real part 
           is within the range [min_x, max_x] and whose imaginary part is bounded by y_max from above

        Parameters
        ----------
        min_x : float
            lower boundary for real part of randomly generated complex numbers
        max_x : float
            upper boundary for real part of randomly generated complex numbers 
        max_y : float
            upper boundary for imaginary part of randomly generated complex numbers  

        Returns
        -------
        ComplexNumber
            Array of size n=samples of random complex numbers in upper half space bounded by max_x, min_x, max_y
        """ 
        return [ComplexNumber(np.random.uniform(min_x, max_x), np.random.uniform(.0, max_y)) for i in range(0, samples)]

_i = ComplexNumber(0, 1)

class RootOfUnity(ComplexNumber):
    def __init__(self, k, n):
        assert k < n, 'Wrong input parameters k and n! k must be < than n but is {} >= {}'.format(str(k), str(n))
        ComplexNumber.__init__(self, math.cos(2.0 * math.pi * float(k) / float(n)), math.sin(2.0 * math.pi * float(k) / float(n)))
