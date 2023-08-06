from base64 import b64decode, b64encode

import maya
from Cryptodome.Cipher import AES


class TimeMixin:
    @staticmethod
    def now(tzinfo="Asia/Shanghai"):
        return maya.now().datetime(tzinfo)

    @classmethod
    def now_str(cls, tzinfo="Asia/Shanghai"):
        """return string format of now as: '20180705010203123456'"""
        now = cls.now(tzinfo)
        return f"{now:%Y%m%d%H%M%S}{now.microsecond}"

    @classmethod
    def timestamp_str(cls, tzinfo="Asia/Shanghai"):
        """return string format of now as: '20180730115800'"""
        return f"{cls.now(tzinfo):%Y%m%d%H%M%S}"


class EncryptMixin:
    @staticmethod
    def encrypt_key(raw_string, key):
        # https://pycryptodome.readthedocs.io/en/latest/src/examples.html
        key = f"{key[:32]:32}".encode()  # make sure len(key) == 32
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(raw_string.encode())
        return " ".join(
            b64encode(i).decode() for i in (cipher.nonce, tag, ciphertext)
        )

    @staticmethod
    def decrypt_key(encrypted, key):
        if not key:
            return encrypted
        key = f"{key[:32]:32}".encode()  # make sure len(key) == 32
        nonce, tag, ciphertext = [b64decode(i) for i in encrypted.split()]
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()
