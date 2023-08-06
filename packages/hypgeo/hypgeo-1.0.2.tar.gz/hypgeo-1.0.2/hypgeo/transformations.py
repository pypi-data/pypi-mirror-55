import math
from hypgeo.complex_plane import _i, ComplexNumber
from hypgeo.moebius import Moeb, MoebConj
from hypgeo.geometry import Vertical, HalfCircle, unit_circle

def moeb_to(z0, z1):
    """Returns the Moebius transformation mapping the complex number z0 to z1.

    Parameters
    ----------
    z0 : ComplexNumber
        Complex number to be mapped to
    z1 : ComplexNumber
        Target complex number

    Returns
    -------
    Moeb
        Moebius transformation mapping the complex number z0 to z1
    """ 

    re_z0 = z0.re
    im_z0 = z0.im
    re_z1 = z1.re
    im_z1 = z1.im

    a = math.sqrt(im_z1 / im_z0)
    b = - re_z0 * math.sqrt(im_z1 / im_z0) + re_z1 * math.sqrt(im_z0 / im_z1)
    c = .0
    d = math.sqrt(im_z0 / im_z1)

    return Moeb(a, b, c, d)

def ellip_0(t):
    """Returns an element of the one parameter group of Moebius rotations (element of elliptic transformations) 
       around imaginary unit.

    Parameters
    ----------
    t : Float
        Flow parameter

    Returns
    -------
    Moeb
        The element of the one parameter group of Moebius rotations around the imaginary unit for time t
    """ 
    return Moeb(math.cos(t), math.sin(t), - math.sin(t), math.cos(t))

def ellip(t, u):
    """Returns an element of the one parameter group of Moebius rotations (element of elliptic transformations) 
       around the complex number u.

    Parameters
    ----------
    t : Float
        Flow parameter
    u : ComplexNumber
        Center of rotation

    Returns
    -------
    Moeb
        the element of the one parameter group of Moebius rotations aroutnd the complex number u
    """
    return ellip_0(t).conj(moeb_to(u, _i))
      
def loxod(t):
    """Returns an element of the one parameter group of Moebius loxodromic transformations (dilatation in y-direction). 

    Parameters
    ----------
    t : Float
        Flow parameter

    Returns
    -------
    Moeb
        The element of the one parameter group of Moebius loxodromic dilatation evaluated for time t
    """
    return Moeb(math.exp(.5 * t), .0, .0, math.exp(- .5 * t))

def parab(t):
    """Returns an element of the one parameter group of Moebius translations in x-direction.

    Parameters
    ----------
    t : Float
        Flow parameter

    Returns
    -------
    Moeb
        The Moebius translation in y-direction by an offset of t
    """
    return Moeb(1.0, t, .0, 1.0) 

def refl_0(R):
    """Returns the Moebius reflection along the half circle centered at (0,0) of radius R.

    Parameters
    ----------
    R : Float
        Radius of circle of reflection

    Returns
    -------
    Moeb
        Moebius reflection along the half circle centered at (0,0) of radius R
    """
    return MoebConj(.0, R, 1.0 / R, .0)  

def refl_circ(u, R):
    """Returns the Moebius reflection along the half circle centered at (u,0) of radius R.

    Parameters
    ----------
    u : Float
        Abscissa of reflection center
    R : Float
        Radius of circle of reflection

    Returns
    -------
    Moeb
        Moebius reflection along the half circle centered at (u,0) of radius R
    """
    return MoebConj(u / (R * R), R * R - u * u / (R * R), 1 / (R * R), - u / (R * R))  

def refl_line(x):
    """Returns the Moebius reflection along the geodesic line x.

    Parameters
    ----------
    x : Line
        Reflection center

    Returns
    -------
    Moeb
        The Moebius reflection along the geodesic line x
    """
    return MoebConj()

def line_to_line(l_0, l_1):
    """Returns the Moebius transformation mapping the geodesic line l_0 to l_1.

    Parameters
    ----------
    l_0 : Line
        Line to be mapped to
    l_1 : Line
        Target line

    Returns
    -------
    Moeb
        Moebius transformation mapping the geodesic line l_0 to l_1
    """
    if type(l_0) == Vertical and type(l_1) == Vertical:
        return vert_to_vert(l_0, l_1)
    elif type(l_0) == Vertical and type(l_1) == HalfCircle:
        return vert_to_circ(l_0, l_1)
    elif type(l_0) == HalfCircle and type(l_1) == Vertical:
        return circ_to_vert(l_0, l_1)
    else:
        return circ_to_circ(l_0, l_1)
    
def vert_to_circ(v, c):
    """Returns the Moebius transformation mapping the geodesic vertical line to the geodesic circle.

    Parameters
    ----------
    v : Line of LineType VERTICAL
        Vertical line to be mapped to
    c : Line of LineType CIRCLE
        Target geodesic circle

    Returns
    -------
    Moeb
        Moebius transformation mapping the geodesic vertical line to the geodesic circle
    """
    return circ_to_vert(c, v).inv()    

def circ_to_vert(c, v):
    """Returns the Moebius transformation mapping the geodesic circle to the geodesic vertical line.

    Parameters
    ----------
    c : Line of LineType CIRCLE
        Geodesic circle to be mapped to
    v : Line of LineType VERTICAL
        Target vertical line

    Returns
    -------
    Moeb
        Moebius transformation mapping the geodesic circle to the geodesic vertical line
    """
    u = v.Absc
    return Moeb(1.0, u, .0, 1.0) * circ_to_Yaxis(c)

def circ_to_Yaxis(circ):
    """Returns the Moebius transformation mapping the geodesic circle to the y-axis.

    Parameters
    ----------
    c : Line of LineType CIRCLE
        Geodesic circle to be mapped to the y-axis

    Returns
    -------
    Moeb
        Moebius transformation mapping the geodesic circle to the y-axis
    """
    c = circ.Center
    r = circ.Radius

    return Moeb(1 / (math.sqrt(2.0 * r)), - c / (math.sqrt(2.0 * r)) + math.sqrt(r / 2.0), 
        - 1 / (math.sqrt(2.0 * r)), c / (math.sqrt(2.0 * r)) + math.sqrt(r / 2.0))

def vert_to_vert(v_0, v_1):
    """Returns the Moebius transformation mapping the geodesic, vertical line v_0 to the vertical line v_1.

    Parameters
    ----------
    v_0 : Line of LineType VERTICAL
        Vertical line to be mapped to
    v_1 : Line of LineType VERTICAL
        Target Vertical line

    Returns
    -------
    Moeb
        Moebius transformation mapping the geodesic, vertical line v_0 to the vertical line v_1
    """
    return Moeb(1.0, v_1.Absc - v_0.Absc, .0, 1.0)

def circ_to_circ(c_0, c_1):
    """Returns the Moebius transformation mapping the geodesic circle c_0 to the circle c_1.

    Parameters
    ----------
    c_0 : Line of LineType CIRCLE
        Geodesic circle to be mapped to
    c_1 : Line of LineType CIRCLE
        Target circle

    Returns
    -------
    Moeb
        Moebius transformation mapping the geodesic circle c_0 to the circle c_1
    """
    c0 = c_0.Center
    r0 = c_0.Radius
    c1 = c_1.Center
    r1 = c_1.Radius
    
    return moeb_to(ComplexNumber(c0, r0), ComplexNumber(c1, r1))

def refl(l):
    """Returns the Moebius reflection along the geodesic line l.

    Parameters
    ----------
    l : Line of LineType either CIRCLE or VERTICAL
        Geodesic line as reflection center

    Returns
    -------
    Moeb
        Moebius reflection along the geodesic line l
    """
    return refl_0(1.0).conj(line_to_line(l, unit_circle))