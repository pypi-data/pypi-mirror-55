# Standard imports
import hashlib
import textwrap
from typing import Any
from inspect import getouterframes, currentframe

# Types
RSAModulus = int
RSAExponent = int
RSAPublicExponent = int
RSAPrivateExponent = int
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
    current_depth: int = len(getouterframes(currentframe()))
    print(textwrap.indent(msg, prefix='-' * current_depth))
