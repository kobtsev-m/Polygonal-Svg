from numpy import linalg
from math import sqrt
import time


def area(a, b, c):
    return (b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0])


def intersect(a, b, c, d):
    if a > b:
        a, b = b, a
    if c > d:
        c, d = d, c
    return max(a, c) < min(b, d)

         
def is_intersect(a, b, c, d):
    return intersect(a[0], b[0], c[0], d[0]) and \
           intersect(a[1], b[1], c[1], d[1]) and \
           area(a, b, c) * area(a, b, d) < 0 and \
           area(c, d, a) * area(c, d, b) < 0


def normalize(x, y, z):
    length = sqrt(x**2 + y**2 + z**2)
    if length:
        return x/length, y/length, z/length
    else:
        return 0, 0, 0


def is_diagonal(pi, pj, pi_next):
    v1 = normalize(pi_next[0] - pi[0], pi_next[1] - pi[1], 0)
    v2 = normalize(pj[0] - pi[0], pj[1] - pi[1], 0)
    
    return linalg.det([v1, v2, (0, 0, 1)]) >= 0


def is_crossing_side(p1, p2, sides):
    for side in sides:
        if is_intersect(p1, p2, side[0], side[1]):
            return True
    
    return False
        

def get_triangles(circuit, degeneracy_check):

    circuit_length = len(circuit)
    if circuit_length < 3:
        return False
    
    sides = []    
    for i in range(len(circuit)-1):
        sides.append([circuit[i], circuit[i+1]])
    sides.append([circuit[-1], circuit[0]])

    if degeneracy_check:
        for side in sides:
            if is_crossing_side(side[0], side[1], sides):
                return False

    start = time.time()

    triangles = []
    while circuit_length > 3:        
        i = 0
        while i < circuit_length-1:
            pi = circuit[i]
            pj = circuit[i+2] if i < len(circuit)-2 else circuit[0]
            pi_next = circuit[i+1]
            
            if is_diagonal(pi, pj, pi_next) and not \
               is_crossing_side(pi, pj, sides):

                triangles.append([pi, pj, pi_next])
                sides.append([pi, pj])
                circuit.remove(pi_next)
                circuit_length -= 1

            i += 1

        if time.time() - start > 1:
            break

    if circuit_length == 3:
        triangles.append(circuit)

    return triangles
