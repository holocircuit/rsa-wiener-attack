import math
import fractions

# Using the recursive definition for continued fractions:
# The nth continued fraction is p_n / q_n, where
# p_0 = a_0, q_0 = 1
# p_1 = a_1p_0 + 1, q_1 = a_1
# p_n = a_np_{n-1} + p_{n-2}, q_n = a_nq_{n-1} + q_{n-2} for n >= 2
#
# we can rewrite this slightly as
# p_{-1} = 1, q_{-1} = 0
# p_0 = a_0, q_0 = 1
# p_n = a_np_{n-1} + p_{n-2}, q_n = a_nq_{n-1} + q_{n-2} for n >= 1
#
# which is how I've calculated it here
def continued_fraction_gen(x, reciprocal, floor, of_int):
    count = 0

    prev_p = 1
    prev_q = 0

    a = floor(x)
    x -= of_int(a)
    p = a
    q = 1
    yield((p, q))

    while x != 0:
        x = reciprocal(x)
        a = floor(x)
        x -= of_int(a)

        p, prev_p = a*p + prev_p, p
        q, prev_q = a*q + prev_q, q

        yield((p, q))

def continued_fraction_float(x):
    return continued_fraction_gen(x, lambda x : 1/x, math.floor, lambda x : float(x))

# This won't work correctly for negative rationals because the floor function is incorrect
def continued_fraction_rational(x):
    reciprocal = lambda x : fractions.Fraction(x.denominator, x.numerator)
    floor = lambda x : x.numerator / x.denominator
    of_int = lambda n : fractions.Fraction(n, 1)
    return continued_fraction_gen(x, reciprocal, floor, of_int)

if __name__ == "__main__":
    print "[+] Some examples of calculating continued fractions"
    print "[+] First 10 continued fractions for pi:"
 
    pi = continued_fraction_float(math.pi)
    for i in xrange(10):
        (p, q) = next(pi)
        print "%10d / %10d" % (p, q) 

    print "[+] Successive approximation errors:"
    pi = continued_fraction_float(math.pi)
    for i in xrange(10):
        (p, q) = next(pi)
        approx = p/q
        diff = math.pi - approx
        print "%+.15f" % diff

    print
    print "[+] All continued fractions for 4090249588 / 2899386061"
    print "[+] (these were just two random 32-bit numbers I chose)"
    print "[+] Unlike for pi, this is a rational number, so eventually terminates"
    x = fractions.Fraction(4090249588, 2899386061)
    x = continued_fraction_rational(x)
    for (p, q) in x:
        print "%10d / %10d" % (p, q) 

 
   
