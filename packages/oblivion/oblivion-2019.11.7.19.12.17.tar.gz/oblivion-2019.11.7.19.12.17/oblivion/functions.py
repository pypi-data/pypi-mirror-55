# Standard imports
import math
import secrets
from typing import Tuple

# Local imports
from oblivion.constants import (
    HashBase,
    HASH_LENGTH,

    callback,
)
from oblivion.entities import (
    RSAPublicKey,
    RSAPrivateKey,
)
from oblivion.primitives import (
    integer_to_octet_string_primitive,
)


def hash_func(msg: bytes) -> bytes:
    """Return the digest of msg."""
    return HashBase(msg).digest()


def random_bytes(size: int) -> bytes:
    """Return a safe random octet string."""
    return secrets.token_bytes(size)


def bytes_xor(bytes_a: bytes, bytes_b: bytes) -> bytes:
    """Return the XOR between A and B."""
    if len(bytes_a) != len(bytes_b):
        raise ValueError('Expected equal length octet strings')
    return bytes(a ^ b for a, b in zip(bytes_a, bytes_b))


def jacobi(numerator: int, denominator: int) -> int:
    """Compute the Jacobi Symbol."""
    if denominator <= 0 or denominator & 1 == 0:
        raise ValueError('Jacobi parameters are out of function domain')
    j_symbol: int = 1
    numerator %= denominator
    while numerator:
        while numerator & 1 == 0:
            numerator = numerator // 2
            if denominator % 8 in (3, 5):
                j_symbol *= -1
        numerator, denominator = denominator, numerator
        if numerator % 4 == denominator % 4 == 3:
            j_symbol *= -1
        numerator %= denominator
    if denominator == 1:
        return j_symbol
    return 0


def is_prime(number, rounds: int = 16) -> bool:
    """Primality test via Solovay-Strassen algorithm."""
    helper: int = (number - 1) // 2
    for _ in range(rounds):
        witness: int = 1 + secrets.randbelow(number - 1)
        if math.gcd(witness, number) != 1:
            return False
        if jacobi(witness, number) % number != pow(witness, helper, number):
            return False
    return True


def generate_prime(bits: int) -> int:
    """Return a prime number of the specified bits."""
    callback('generating prime')
    while True:
        prime = secrets.randbits(bits + 1)
        prime += (1 - prime & 1)
        if (prime).bit_length() < bits:
            continue
        if is_prime(prime):
            return prime


def generate_special_prime(bits: int, depth: int = 2) -> int:
    """
    Return a prime 'p' where 'p - 1' has large prime factors.

    To guarantee that 'p - 1' has a large prime factor we'll generate a random
    base prime number 'u', and then find the first prime 'p' in the sequence:

        i * u + 1, where i = 2, 4, 6, ...

    With this, we ensure that the only prime factor of 'p - 1' is 'u', which is
    large.

    To provide extra security, 'u - 1' will also contain large prime factors,
    and recursively the base prime used to generate 'u', up to the provided
    depth level.
    """
    callback('generating base prime')

    counter: int = 0
    if depth > 1:
        base_prime = generate_special_prime(bits, depth=depth - 1)
    else:
        base_prime = generate_prime(bits)

    callback('incrementing base prime')
    while True:
        counter += 2
        prime = counter * base_prime + 1
        if is_prime(prime):
            return prime


def extended_euclidian_gcd(left: int, right: int) -> Tuple[int, int, int]:
    """Solve left * x + right * y = gcd(left, right) and return r, x, y."""
    new_x, new_y, new_r = 0, 1, right
    old_x, old_y, old_r = 1, 0, left
    while new_r != 0:
        quotient = old_r // new_r
        old_r, new_r = new_r, old_r - quotient * new_r
        old_x, new_x = new_x, old_x - quotient * new_x
        old_y, new_y = new_y, old_y - quotient * new_y
    return old_r, old_x, old_y


def modular_multiplicative_inverse(number: int, modulo: int) -> int:
    """Compute the multiplicative inverse of number under given modulo."""
    # Assumes number and modulo are co-prime
    return extended_euclidian_gcd(number, modulo)[1] % modulo


def rsa_generate_keys(bits: int) -> Tuple[RSAPublicKey, RSAPrivateKey]:
    """Generate public and private keys with (n, d) of the specified bits."""
    public = RSAPublicKey(modulus=0, exponent=0)
    private = RSAPrivateKey(modulus=0, exponent=0)
    reduced_totient_divisor_min_bits: int = bits // 2 ** 4
    while True:
        callback('generating prime number: p')
        # p and q should differ in length by a few digits
        # both (p - 1) and (q - 1) should contain large prime factors
        prime_p = generate_special_prime(bits // 2 - 1)
        callback('generating prime number: q')
        prime_q = generate_special_prime(bits // 2 + 1)
        callback('computing modulus: n')
        public.modulus = prime_p * prime_q
        private.modulus = public.modulus
        callback('computing health check')
        # gcd(p - 1, q - 1) should be small
        reduced_totient_divisor: int = math.gcd(prime_p - 1, prime_q - 1)
        if public.modulus_bits >= bits:
            if reduced_totient_divisor_min_bits:
                if (reduced_totient_divisor.bit_length()
                        < reduced_totient_divisor_min_bits):
                    break
            else:
                break
        callback('health check failed, retrying')
    callback('computing reduced_totient of: n')
    reduced_totient = (prime_p - 1) * (prime_q - 1) // reduced_totient_divisor
    while True:
        callback('computing private exponent: d')
        private.exponent = generate_prime(bits)
        # It's guaranteed that private.exponent < reduced_totient (FIPS 186-4)
        callback('computing public exponent: e')
        public.exponent = \
            modular_multiplicative_inverse(private.exponent, reduced_totient)
        callback('computing health check')
        # Ensure that any message (except for 0 and 1), will be reduced
        #   after performing encryption, this is, M ** e (mod n) will
        #   'wrap around'
        if public.modulus_bits < public.exponent < reduced_totient \
                and math.gcd(public.exponent, reduced_totient) == 1:
            break
        callback('health check failed, retrying')
    return public, private


def mask_generation_function(mgf_seed: bytes, mask_length: int) -> bytes:
    """Mask generation function based on a hash function."""
    # https://tools.ietf.org/html/rfc8017#appendix-B.2.1
    if mask_length > (2 ** 32) * HASH_LENGTH:
        raise ValueError(f'{mask_length} > {(2 ** 32) * HASH_LENGTH}')

    range_length = 1 + mask_length // HASH_LENGTH
    if mask_length % HASH_LENGTH != 0:
        range_length -= 1

    mgf_output = bytes()
    for counter in range(1 + range_length):
        mgf_output += hash_func(
            mgf_seed
            + integer_to_octet_string_primitive(
                length=4,
                integer=counter))
    return mgf_output[:mask_length]
