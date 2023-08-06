class RSAException(Exception):
    """Base exceptions for this package."""


class RSAEncryptionException(RSAException):
    """An error ocurred while encrypting."""


class RSADecryptionException(RSAException):
    """An error ocurred while decrypting."""
