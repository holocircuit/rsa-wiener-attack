from continued_fraction import *
from utils import *
import fractions
import time

# Takes a guess for phi(N) = (p-1)(q-1), and checks if it gives the prime factorisation of N
# returns (p, q) if so, otherwise returns None
def recover_pq_from_phi_n(N, guess_for_phi):
    # let A = p + q, which we can determine from N and phi(N)
    A = N - guess_for_phi + 1

    # let B = (p - q). Then B^2 = A^2 - 4N
    # try and solve to get a square root
    B2 = A*A - 4*N

    B = int_sqrt_exact(B2)
    if B == None: return None

    # Use the values for A and B to recover p and q, and check if gives a valid factorisation
    p = (A + B) / 2
    q = (A - B) / 2

    if p * q == N: return (p, q)
    return None

# Given N, e, where d < (1/3) * N**0.25, recovers d and the factorisation of N using Wiener's attack
# returns (p, q, d), and asserts that e, d are inverses
def wiener_attack(N, e):
    frac = fractions.Fraction(e, N)

    for (k, d) in continued_fraction_rational(frac):
        if k == 0:
            continue
        phi_n_guess = (e * d - 1) / k
        factorisation = recover_pq_from_phi_n(N, phi_n_guess)
        if factorisation != None:
            (p, q) = factorisation
            break
    else:
        print "The attack failed :("
        return None

    phi = (p - 1) * (q - 1)
    assert (e * d) % phi == 1
    return (p, q, d)

if __name__ == "__main__":
    print "[+] Demonstrating Wiener's attack"
    NUMBER_OF_BITS = 10
    p = gen_prime(NUMBER_OF_BITS)
    q = gen_prime(NUMBER_OF_BITS)
    if p < q: p, q = q, p

    N = p * q
    phi = (p-1)*(q-1)

    upper_bound = int_sqrt(int_sqrt(N)) / 3

    # Generate a random "bad" (i.e. small) private key
    bad_d = random.randrange(2, int(upper_bound) + 1)
    e = modinv(bad_d, phi)
    while e == None:
        bad_d = random.randrange(2, int(upper_bound) + 1)
        e = modinv(bad_d, phi)

    print "[+] Generated RSA key with two random %d-bit primes, and a \"small\" d" % NUMBER_OF_BITS
    print "N: %d" % N
    print "e: %d" % e
    print
    print "[+] Running Wiener's attack..."
    start_ = time.time()
    output = wiener_attack(N, e)
    end_ = time.time()
    print "[+] It took %d seconds" % (end_ - start_)
    if output != None:
        (p2, q2, d2) = output
        print "[+] Output from Wiener's attack:"
        print "[+] p: %d" % p2
        print "[+] q: %d" % q2
        print "[+] d: %d" % d2
        print
        print "Actual values used:"
        print "[+] p: %d" % p
        print "[+] q: %d" % q
        print "[+] d: %d" % bad_d
    else:
        print "[-] Wiener's attack failed!"
        print "[-] p: %d" % p
        print "[-] q: %d" % q
        print "[-] d: %d" % bad_d
        print "[-] phi: %d" % phi
        print "[-] k: %d" % ((e * bad_d - 1) / phi)
