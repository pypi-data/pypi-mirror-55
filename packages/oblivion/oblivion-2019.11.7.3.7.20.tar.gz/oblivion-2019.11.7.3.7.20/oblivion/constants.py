# Standard imports
import hashlib
import textwrap
from typing import Any, Tuple
from inspect import getouterframes, currentframe

# Types
RSAModulus = int
RSAPublicExponent = int
RSAPrivateExponent = int
RSAPublicKey = Tuple[RSAModulus, RSAPublicExponent]
RSAPrivateKey = Tuple[RSAModulus, RSAPrivateExponent]
RSAMsg = bytes
RSALabel = bytes
RSACyphertext = bytes
RSAMsgRepresentative = int
RSACyphertextRepresentative = int

# Crypto constants
HashBase = hashlib.sha3_512
HASH_LENGTH = HashBase().digest_size


def callback(msg: str) -> Any:
    """Callback function to notify progress."""
    return msg


def suggested_callback(msg):
    """Suggested callback function."""
    current_depth: int = len(getouterframes(currentframe()))
    print(textwrap.indent(msg, prefix='-' * current_depth))


#
# Exceptions
#


class RSAException(Exception):
    """Base exceptions for this package."""


class RSAEncryptionException(RSAException):
    """An error ocurred while encrypting."""


class RSADecryptionException(RSAException):
    """An error ocurred while decrypting."""
