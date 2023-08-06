# Standard imports
import json
from typing import Dict, Union

# Local imports
from oblivion.constants import (
    RSAModulus,
    RSAExponent,
)


class RSAKey():
    """Class to represent a RSA Key."""

    kind: str = 'generic'
    extension: str = 'json'

    def __init__(self, *,
                 modulus: RSAModulus,
                 exponent: RSAExponent):
        """Class constructor."""
        self._modulus: RSAModulus = 0
        self.modulus_octets: int = 0
        self.modulus_bits: int = 0
        self.modulus: RSAModulus = modulus
        self._exponent: RSAExponent = 0
        self.exponent_bits: int = 0
        self.exponent: RSAExponent = exponent

    @property
    def exponent(self) -> RSAExponent:
        return self._exponent

    @exponent.setter
    def exponent(self, exponent: RSAExponent):
        self._exponent = exponent
        self.exponent_bits = exponent.bit_length()

    @property
    def modulus(self) -> RSAModulus:
        return self._modulus

    @modulus.setter
    def modulus(self, modulus: RSAModulus):
        self._modulus = modulus
        self.modulus_bits = modulus.bit_length()
        self.modulus_octets = (
            self.modulus_bits // 8 + (self.modulus_bits % 8 != 0))

    def save_to_file(self, path: str):
        """Save the Key to a location in the file system."""
        with open(path, 'w') as target_handle:
            data: Dict[str, Union[int, str]] = {
                'type': self.kind,
                'modulus': self.modulus,
                'exponent': self.exponent,
                'modulus_bits': self.modulus_bits,
                'exponent_bits': self.exponent_bits,
            }
            target_handle.write(json.dumps(data, indent=4))
            target_handle.write('\n')


class RSAPublicKey(RSAKey):
    """Class to represent a RSA Public Key."""

    kind: str = 'public'


class RSAPrivateKey(RSAKey):
    """Class to represent a RSA Private Key."""

    kind: str = 'private'
