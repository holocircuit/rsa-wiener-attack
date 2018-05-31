import random

# tests if n is prime, using Miller-Rabin with 1000 random moduli
def check_prime(n):
    if n <= 1: raise ValueError

    # check all factors up to 10_000, as a shortcut
    for i in xrange(2, 10000):
        if n == i: return True

        if n % i == 0:
            return False

    # if it returns False, n is definitely not prime
    def miller_rabin_one(n, a):
        r = 0
        m = n - 1

        # early exit - check Fermat's Little Theorem
        z = pow(a, m, n)
        if z != 1: return False

        while m % 2 == 0:
            r += 1
            m /= 2

        z = pow(a, m, n)
        if z == 1 or z == n - 1:
            return True

        for i in xrange(r):
            z *= z
            z %= n

            if z == n - 1:
                return True
            if z == 1:
                # if we reach 1, and haven't hit -1 yet, then n is definitely not prime
                # because we found a square root of 1 that wasn't 1 or -1
                return False
        # we should never be able to reach here, because we checked FLT above, so should have exited in the last iteration of the loop
        assert False

    # test for 1000 random moduli
    for _ in xrange(100):
        a = random.randrange(2, n)
        if not miller_rabin_one(n, a):
            return False
    return True

# generate a prime which is at least 2**n
def gen_prime(n):
    lower_bound = 2**n
    start = random.randrange(lower_bound, 2 * lower_bound)

    while not check_prime(start):
        start += 1
    return start

# floor of square root of an integer, by binary search
def int_sqrt(N):
    if N < 0: return None
    if N == 0: return 0
    if N == 1: return 1

    lower = 0
    upper = N
    while upper - lower > 1:
        mid = (lower + upper) / 2
        if mid ** 2 <= N:
            lower = mid
        else:
            upper = mid

    return lower

# only returns if the number is a square
def int_sqrt_exact(N):
    k = int_sqrt(N)

    if k == None: return None
    if k**2 == N: return k
    return None

# shamelessly stolen from wikibooks
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m
