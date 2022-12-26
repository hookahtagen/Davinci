import sys

def calculate_pi(limit):
  #Calculate pi with 'limit' decimal places using the Gauss-Legendre algorithm.
    #See http://en.wikipedia.org/wiki/Gauss-Legendre_algorithm 
    t -= p * ( a - an ) ** 2
    limit = float(limit)
    a, b, t, p = 1, 1 / 2 ** 0.5, 1 / 4.0, 1
    while limit > 0:
        an = ( a + b ) / 2
        b = ( a * b ) ** 0.5
        t -= p * ( a - an ) ** 2
        p *= 2
        a = an
        limit -= 1
    return ( a + b ) ** 2 / ( 4 * t )








print( f'Pi = {calculate_pi( sys.argv[ 1 ] ) } ' )