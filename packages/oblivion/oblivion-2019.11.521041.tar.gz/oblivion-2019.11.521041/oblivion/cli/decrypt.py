# Standard imports
import io
import os
import sys

# Local imports
from oblivion.constants import (
    callback,
)
from oblivion.entities import (
    RSAPrivateKey,
)
from oblivion.schemes import (
    rsa_decryption_scheme_with_oaep_padding,
)


def put_subparser(subparsers):
    parser = subparsers.add_parser(
        'decrypt',
        help='Decrypt a file read from standard input (/dev/stdin)',
    )
    parser.add_argument(
        '-k', '--key-name',
        help='file name of the key, defaults to "rsa"',
        required=False,
        default='rsa',
    )
    parser.set_defaults(subparser_handler=handler)


def handler(args):
    key = RSAPrivateKey(modulus=0, exponent=0)

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

    with io.BufferedReader(sys.stdin.buffer, 1024) as buffer, \
            io.BufferedWriter(sys.stdout.buffer, 1024) as out_buffer:
        block = bytes.fromhex(buffer.readline().decode()[0:-1])
        while block:
            decrypted_block = rsa_decryption_scheme_with_oaep_padding(
                private_key=key,
                ciphertext=block,
                label=b'oblivion',
            )
            out_buffer.write(decrypted_block)
            block = bytes.fromhex(buffer.readline().decode()[0:-1])
