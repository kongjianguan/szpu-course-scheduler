import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

CHARSET = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678"
KEY = b"arSxEu10mMRZ0gYu"


def _random_string(n: int) -> str:
    return ''.join(secrets.choice(CHARSET) for _ in range(n))


def encrypt_password(password: str) -> str:
    iv = _random_string(16).encode()
    plaintext = (_random_string(64) + password).encode()
    cipher = AES.new(KEY, AES.MODE_CBC, iv=iv)
    ct = cipher.encrypt(pad(plaintext, AES.block_size))
    return base64.b64encode(iv + ct).decode()
