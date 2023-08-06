def associative_property_add(a, b, c):
    return (a + (b + c)) - ((a + b) + c)

def commutative_portperty_add(a, b, c):
    return (a + b) - (b + a)

def neutral_element_add(a, neutral):
    return (a + neutral) - a

def inv_element_add(a, a_inv, neutral):
    return (a + a_inv) - neutral


def associative_property_mul(a, b, c):
    return (a * (b * c)) - ((a * b) * c)

def commutative_portperty_mul(a, b, c):
    return (a * b) - (b * a)

def neutral_element_mul(a, neutral):
    return (a * neutral) - a

def inv_element_mul(a, a_inv, neutral):
    return (a * a_inv) - neutral


def right_distributive(a, b, c):
    return (a * (b + c)) - (a * b + a * c)

def left_distributive(a, b, c):
    return ((b + c) * a) - (b * a + c * a)