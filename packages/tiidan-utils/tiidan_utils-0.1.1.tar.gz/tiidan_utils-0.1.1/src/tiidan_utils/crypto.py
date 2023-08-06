from hashlib import sha256
from base64 import b64encode


def sha256_base64(value):
    m = sha256()
    m.update(value.encode())
    bytes = m.digest()
    return str(b64encode(bytes), "utf-8")


def base36encode(integer):
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sign = "-" if integer < 0 else ""
    integer = abs(integer)
    result = ""
    while integer > 0:
        integer, remainder = divmod(integer, 36)
        result = chars[remainder] + result

    return sign + result
