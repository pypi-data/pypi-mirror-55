# Standard imports
import io
import os
import sys

# Local imports
from oblivion.constants import (
    callback,
    HASH_LENGTH,
)
from oblivion.entities import (
    RSAPublicKey,
)
from oblivion.schemes import (
    rsa_encryption_scheme_with_oaep_padding,
)


def put_subparser(subparsers):
    parser = subparsers.add_parser(
        'encrypt',
        help='Encrypt a file read from standard input (/dev/stdin)',
    )
    parser.add_argument(
        '-k', '--key-name',
        help='file name of the key, defaults to "rsa"',
        required=False,
        default='rsa',
    )
    parser.set_defaults(subparser_handler=handler)


def handler(args):
    key = RSAPublicKey(modulus=0, exponent=0)

    path: str = \
        os.path.abspath(
            os.path.join(
                os.getcwd(),
                f'{args.key_name}.{key.kind}.{key.extension}'))

    callback(f'reading {key.kind} key from: {path}')
    if not os.path.exists(path):
        callback(f'error: no such key')
        sys.exit(1)

    key.load_from_file(path)

    # We can encrypt at much this data octets per round
    block_size = key.modulus_octets - 2 * (HASH_LENGTH + 1)
    # Adjust the last octet
    block_size -= 1

    with io.BufferedReader(sys.stdin.buffer) as buffer:
        block = buffer.read(block_size)
        while block:
            encrypted_block = rsa_encryption_scheme_with_oaep_padding(
                public_key=key,
                message=block,
                label=b'oblivion',
            )
            print(encrypted_block.hex())
            block = buffer.read(block_size)
