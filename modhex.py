#!/usr/bin/python3

"""
Conversions between hexadecimal strings, integers and ASCII strings to/from
modhex format. See https://demo.yubico.com/modhex.php.

    >>> hex2mod('0')
    'c'
    >>> hex2mod('41')
    'fb'
    >>> hex2mod('Fff')
    'vvv'
    >>> hex2mod('fedcba9876543210')
    'vutrnlkjihgfedbc'
    >>> int2mod(0)
    'cc'
    >>> int2mod(4095)
    'vvv'
    >>> ascii2mod('A')
    'fb'
    >>> ascii2mod('Az')
    'fbil'
    >>> ascii2mod('test')
    'ifhgieif'

    >>> mod2hex('c')
    '0'
    >>> mod2hex('FB')
    '41'
    >>> mod2hex('FC')
    '40'
    >>> mod2hex('FZ')
    '40'
    >>> mod2hex('GA')
    '50'
    >>> mod2hex('GAA')
    '500'
    >>> mod2hex('vVv')
    'fff'
    >>> mod2int('c')
    0
    >>> mod2int('vvv')
    4095
    >>> mod2ascii('fb')
    'A'
    >>> mod2ascii('Ga')
    'P'
    >>> mod2ascii('c') == chr(0)
    True
    >>> mod2ascii('cc') == chr(0)
    True
    >>> mod2ascii('FBIL')
    'Az'
    >>> mod2ascii('iFhGiEiF')
    'test'

"""


import string

MODHEX_DIGITS = 'cbdefghijklnrtuv'

TO_MODHEX = str.maketrans(string.hexdigits[:16], MODHEX_DIGITS)
TO_HEX = str.maketrans(MODHEX_DIGITS, string.hexdigits[:16])


def hex2mod(hex_str):
    return hex_str.lower().translate(TO_MODHEX)


def int2mod(i):
    return hex2mod('%02x' % i)


def ascii2mod(text):
    return ''.join(int2mod(byte) for byte in text.encode('ASCII'))


def mod2hex(mod_str):
    mod_str = mod_str.lower()
    non_mod_digits = {c for c in mod_str if c not in MODHEX_DIGITS}
    for d in non_mod_digits:
        mod_str = mod_str.replace(d, 'c')
    return mod_str.translate(TO_HEX)


def mod2int(mod_str):
    return int(mod2hex(mod_str), 16)


def mod2ascii(mod_str):
    if len(mod_str) % 2:
        mod_str = 'c' + mod_str
    return ''.join(chr(mod2int(a+b)) for a, b
                   in zip(mod_str[:-1:2], mod_str[1::2]))


def help():
    print('usage: %s [-d] <data>' % sys.argv[0])
    sys.exit(-1)


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if len(args) not in (1, 2):
        help()
    if '-d' in args:
        args.remove('-d')
        if not args:
            help()
        print(mod2ascii(args[-1]))
    else:
        print(ascii2mod(args[-1]))
