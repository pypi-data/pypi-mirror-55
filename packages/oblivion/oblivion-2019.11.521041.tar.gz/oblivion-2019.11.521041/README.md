# Inspiration

There are many encryption frameworks out there.

However, after researching a while I found they lack four things
that I (and you should too) care about:

1. Encryption with very large encryption keys:

    ![openssl-warning-with-large-keys.png][openssl-warning-with-large-keys.png]

    ![openssl-modulus-too-large-error.png][openssl-modulus-too-large-error.png]

    As a rule of thumb:

    > The **larger** the **key**, the **strongest** the **encryption**

1. Secure key generation algorithms, focused in **security**, and not in *speed*:

    ```
    There are a lot of things a good RSA key pair **must** have,
    and they are not fast to compute.

    I'm willing to spend more time in the key generation process,
    and ensure that my encryption keys comply with the entire set of health
    checks and regulations.
    ```

1. Configured in the **strongest** mode out-of-the-box

    If using *RSA* without **Optimal Asymmetric Encryption Padding** is a **vulnerability**
    (See: [CWE 780][CWE 780]):

    Then:

    > Why it is not the default and **must to have** padding out there?

1. With support for state of the art technologies:

    Yes, I'm taking about **OAEP** with a
    [Mask Generation Function][Mask Generation Function]
    based on [Keccak][Keccak]

    According with:

    > [RFC 8017][RFC 8017], [FIPS 186-4][FIPS 186-4] and the
    > [Original RSA Paper][Original RSA Paper]

---

# A secure encryption client

This is how **Oblivion** was born.

Define 'Oblivion':

> A state marked by lack of awareness or consciousness

Consciousness about privacy, encryption, and data protection,

This client allows you to:

1. Encrypt with **infinitely large encryption keys** <sup>1</sup>:

    Everything is based around Python's int (which have no lower/upper bounds)

1. Implements all the encryption key **health checks** during key generation,
    and discard potential keys if any verification is not met.

    > **100% strictness**

1. Goes directly with the **RSA-OAEP** crypto scheme based on a **MGF-Keccak** (SHA3-512)

# Use example

1. Install the package:

    ```bash
    $ pip3 install oblivion
    ```

1. Generate your Encryption keys:

    Let's go with 1040 bits keys just for the sake of the example:

    ```bash
    $ oblivion gen 1040
    ```

1. Keys are saved as JSON files,
   one for the public key, one for the private key:

    ```bash
    $ cat rsa.public.json
    ```

    ```json
    {
        "kind": "public",
        "modulus": 122522690358965537792682708496824124112262516942132270155501584497485322645552293207409120914152523672605862836449972168943300350829966930587889728961421830123882224038187427821244472786287020940427834796994555925821321328140925177025426255093656109825645197375135836137545187613283966690578037338843812108868700393269379,
        "exponent": 35942361192094851710022089032047440816217736531893477998580655180307086515540097708615281696760898540432857654468794697590336239623818004644814428847025504745226162859136221296553159608597485457284425658071305244131548998023576152565239915417891151324846782444935361414016601888473188847748509131097620357395575845669301,
        "modulus_bits": 1064,
        "exponent_bits": 1062
    }
    ```

    ```bash
    $ cat rsa.public.json
    ```

    ```json
    {
        "kind": "private",
        "modulus": 122522690358965537792682708496824124112262516942132270155501584497485322645552293207409120914152523672605862836449972168943300350829966930587889728961421830123882224038187427821244472786287020940427834796994555925821321328140925177025426255093656109825645197375135836137545187613283966690578037338843812108868700393269379,
        "exponent": 22373809461484105322724446741777972869163173908614201128738551454257167774768120493233929040210994088302694160927045096319261912202540606801276593998571894092502684928664270800051840286074304365636683965688529464305214291964596762384957282965696803909429672410797771786447911861012359269843584424638990157133366301,
        "modulus_bits": 1064,
        "exponent_bits": 1041
    }
    ```

1. Encrypting is easy:

    ```bash
    $ cat your-file | oblivion encrypt > encrypted-file
    ```

    oblivion will take by default encryption key any **rsa.public.json** located
    in the current directory

1. Decrypting is even easier:

    ```bash
    $ cat encrypted-file | oblivion decrypt > your-original-file
    ```

    similarly, any **rsa.private.json** located
    in the current directory will be used for decryption

    you can specify a different one passing `--key-name` flag
    to oblivion on the command line

1. Below you'll find a little gif with the process:

![how-to-use.gif][how-to-use.gif]

---

**1**: Sure thing generating and encrypting data with large encryption keys take time.

    If it takes time to you, it takes even more time to an attacker to break the encryption.

    That feels good :)

[openssl-warning-with-large-keys.png]: ./static/readme/openssl-warning-with-large-keys.png
[openssl-modulus-too-large-error.png]: ./static/readme/openssl-modulus-too-large-error.png
[how-to-use.gif]: ./static/how-to-use.gif
[Mask Generation Function]: https://tools.ietf.org/html/rfc8017#appendix-B.2.1
[Keccak]: https://csrc.nist.gov/publications/detail/fips/202/final
[CWE 780]: https://cwe.mitre.org/data/definitions/780.html
[RFC 8017]: https://tools.ietf.org/html/rfc8017
[FIPS 186-4]: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf
[Original RSA Paper]: https://people.csail.mit.edu/rivest/Rsapaper.pdf
