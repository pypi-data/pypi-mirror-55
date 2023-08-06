# Standard imports
from typing import Tuple

# Local imports
from oblivion.constants import (
    RSAMsgRepresentative,
    RSACyphertextRepresentative,
)
from oblivion.entities import (
    RSAPublicKey,
    RSAPrivateKey,
)


def octet_string_to_integer_primitive(octet_string: bytes) -> Tuple[int, int]:
    """Convert an octet string to a nonnegative integer."""
    # https://tools.ietf.org/html/rfc8017#section-4.2
    integer = \
        sum(value * (256 ** index)
            for index, value in enumerate(reversed(octet_string)))
    return len(octet_string), integer


def integer_to_octet_string_primitive(length: int, integer: int) -> bytes:
    """Convert a nonnegative integer to an octet string."""
    # https://tools.ietf.org/html/rfc8017#section-4.1
    if integer >= 256 ** length:
        raise ValueError(f"{integer} >= 256 ** {length}")
    index = 0
    digits = [0] * length
    while integer:
        digits[index] = integer % 256
        integer //= 256
        index += 1
    return bytes(reversed(digits))


def rsa_encryption_primitive(public_key: RSAPublicKey,
                             message: RSAMsgRepresentative,
                             ) -> RSACyphertextRepresentative:
    # https://tools.ietf.org/html/rfc8017#section-5.1.1
    if not 0 <= message <= public_key.modulus:
        raise ValueError(f'not 0 <= {message} <= {public_key.modulus}')
    return pow(message, public_key.exponent, public_key.modulus)


def rsa_decryption_primitive(private_key: RSAPrivateKey,
                             ciphertext: RSACyphertextRepresentative,
                             ) -> RSACyphertextRepresentative:
    # https://tools.ietf.org/html/rfc8017#section-5.1.2
    if not 0 <= ciphertext <= private_key.modulus:
        raise ValueError(f'not 0 <= {ciphertext} <= {private_key.modulus}')
    return pow(ciphertext, private_key.exponent, private_key.modulus)
