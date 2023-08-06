# Standard imports
import os

# Local imports
from oblivion.constants import (
    callback,
    MINIMUM_MODULUS_BIT_SIZE,
)
from oblivion.functions import (
    rsa_generate_keys,
)


def put_subparser(subparsers):
    parser = subparsers.add_parser(
        'gen',
        help='Generates a new RSA Key Pair',
    )
    parser.add_argument(
        '-n', '--name',
        help='file name where the key will be stored, defaults to "rsa"',
        required=False,
        default='rsa',
    )
    parser.add_argument(
        'bits',
        help='minimum bits on the RSA modulus, (4196, 16384, 65536, etc)',
        type=int,
    )
    parser.set_defaults(subparser_handler=handler)


def handler(args):
    callback('generating a new secure RSA key pair')
    if args.bits < MINIMUM_MODULUS_BIT_SIZE:
        callback(f'minimum bit size is {MINIMUM_MODULUS_BIT_SIZE}, adjusting')
        args.bits = MINIMUM_MODULUS_BIT_SIZE
    public_key, private_key = rsa_generate_keys(args.bits)

    for key in (public_key, private_key):
        path: str = \
            os.path.abspath(
                os.path.join(
                    os.getcwd(),
                    f'{args.name}.{key.kind}.{key.extension}'))

        callback(f'saving {key.kind} key to: {path}')

        key.save_to_file(path)
