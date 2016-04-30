from math import pow

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1]
    
def norm(a):
    return pow(a[0]*a[0] + a[1]*a[1], 0.5)
    
def sub(a, b):
    return a[0] - b[0], a[1] - b[1]
    
def add(a, b):
    return a[0] + b[0], a[1] + b[1]
    
def mult(a, b):
    return a*b[0], a*b[1]
    
def dist(a, b):
    return norm(sub(a, b))

def point_to_line_dist(v, w, p):
    l2 = pow(dist(v, w), 2)
    t = dot(sub(p, v), sub(w, v))/l2
    projection = add(v, mult(t, sub(w, v)))
    return dist(p, projection)
        
    