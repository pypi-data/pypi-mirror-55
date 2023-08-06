"""Setup package."""

import distutils
from datetime import datetime

distutils.core.setup(
    name='oblivion',
    version=datetime.utcnow().strftime('%Y.%m.%d.%H.%M.%S'),
    packages=[
        'oblivion',
        'oblivion.cli'
    ],

    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'oblivion=oblivion.cli:cli',
        ],
    },
)
