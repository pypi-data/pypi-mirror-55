# Local imports
from oblivion.constants import (
    RSAMsg,
    RSALabel,
    RSACyphertext,
    HASH_LENGTH,
)
from oblivion.entities import (
    RSAPublicKey,
    RSAPrivateKey,
)
from oblivion.exceptions import (
    RSAEncryptionException,
    RSADecryptionException,
)
from oblivion.primitives import (
    octet_string_to_integer_primitive,
    integer_to_octet_string_primitive,
    rsa_encryption_primitive,
    rsa_decryption_primitive,
)
from oblivion.functions import (
    hash_func,
    random_bytes,
    bytes_xor,
    mask_generation_function,
)


def rsa_encryption_scheme_with_oaep_padding(public_key: RSAPublicKey,
                                            message: RSAMsg,
                                            label: RSALabel = b'',
                                            ) -> bytes:
    """Perform RSAES-OAEP-ENCRYPT as per RFC-8017."""
    # https://tools.ietf.org/html/rfc8017#section-7.1.1
    # pylint: disable=too-many-locals
    message_length = len(message)
    if message_length > (public_key.modulus_octets - 2 * (HASH_LENGTH + 1)):
        raise RSAEncryptionException()

    label_hash = hash_func(label)
    padding_string = b'\x00' * (
        public_key.modulus_octets
        - message_length
        - 2 * (HASH_LENGTH + 1))
    data_block = label_hash + padding_string + b'\x01' + message
    seed = random_bytes(HASH_LENGTH)
    data_block_mask = mask_generation_function(
        seed, public_key.modulus_octets - HASH_LENGTH - 1)
    masked_data_block = bytes_xor(data_block, data_block_mask)
    seed_mask = mask_generation_function(masked_data_block, HASH_LENGTH)
    masked_seed = bytes_xor(seed, seed_mask)
    encoded_message = b'\x00' + masked_seed + masked_data_block
    _, encoded_message_representative = \
        octet_string_to_integer_primitive(encoded_message)
    ciphertext_representative = rsa_encryption_primitive(
        public_key=public_key,
        message=encoded_message_representative)
    ciphertext = integer_to_octet_string_primitive(
        length=public_key.modulus_octets,
        integer=ciphertext_representative)
    return ciphertext


def rsa_decryption_scheme_with_optimal_asymmetric_encryption_padding(
        private_key: RSAPrivateKey,
        ciphertext: RSACyphertext,
        label: RSALabel = b'') -> bytes:
    """Perform RSAES-OAEP-DECRYPT as per RFC-8017."""
    # https://tools.ietf.org/html/rfc8017#section-7.1.2
    # pylint: disable=too-many-locals
    ciphertext_length = len(ciphertext)

    if ciphertext_length != private_key.modulus_octets \
            or private_key.modulus_octets < 2 * (HASH_LENGTH + 1):
        raise RSADecryptionException()

    _, ciphertext_representative = \
        octet_string_to_integer_primitive(ciphertext)
    message_representative = rsa_decryption_primitive(
        private_key=private_key,
        ciphertext=ciphertext_representative)
    encoded_message = integer_to_octet_string_primitive(
        length=private_key.modulus_octets,
        integer=message_representative)
    label_hash = hash_func(label)
    masked_byte = encoded_message[0]
    masked_seed = encoded_message[1:1 + HASH_LENGTH]
    masked_data_block = encoded_message[1 + HASH_LENGTH:]
    seed_mask = mask_generation_function(masked_data_block, HASH_LENGTH)
    seed = bytes_xor(masked_seed, seed_mask)
    data_block_mask = mask_generation_function(
        mgf_seed=seed,
        mask_length=private_key.modulus_octets - HASH_LENGTH - 1)
    data_block = bytes_xor(masked_data_block, data_block_mask)
    expected_label_hash = data_block[:HASH_LENGTH]
    index = data_block[HASH_LENGTH:].find(b'\x01')
    if index == -1 \
            or masked_byte != 0x00 \
            or label_hash != expected_label_hash:
        raise RSADecryptionException()
    message = data_block[HASH_LENGTH + index + 1:]
    return message
