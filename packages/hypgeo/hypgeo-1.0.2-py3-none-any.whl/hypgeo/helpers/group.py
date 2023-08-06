def associative_property(a, b, c):
    return (a * (b * c)) / ((a * b) * c)

def neutral_element_r(a, neutral):
    return (a * neutral) / a

def neutral_element_l(a, neutral):
    return (neutral * a) / a

def inv_element_r(a, a_inv):
    return a * a_inv

def inv_element_l(a, a_inv):
    return a_inv * a