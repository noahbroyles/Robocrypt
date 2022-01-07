#!/usr/bin/env python3

import os
import sys
import base64
import getpass
import threading

from pathlib import Path
from struct import unpack
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# This is the version of the programn ;)
__version__ = '2.0.ProV7.69G'


CIPHER_WHEEL_N = {0: b'A', 1: b'B', 2: b'C', 3: b'D', 4: b'E', 5: b'F', 6: b'G', 7: b'H', 8: b'I', 9: b'J', 10: b'K', 11: b'L', 12: b'M', 13: b'N', 14: b'O', 15: b'P', 16: b'Q', 17: b'R', 18: b'S', 19: b'T', 20: b'U', 21: b'V', 22: b'W', 23: b'X', 24: b'Y', 25: b'Z', 26: b'a', 27: b'b', 28: b'c', 29: b'd', 30: b'e', 31: b'f', 32: b'g', 33: b'h', 34: b'i', 35: b'j', 36: b'k', 37: b'l', 38: b'm', 39: b'n', 40: b'o', 41: b'p', 42: b'q', 43: b'r', 44: b's', 45: b't', 46: b'u', 47: b'v', 48: b'w', 49: b'x', 50: b'y', 51: b'z', 52: b'0', 53: b'1', 54: b'2', 55: b'3', 56: b'4', 57: b'5', 58: b'6', 59: b'7', 60: b'8', 61: b'9', 62: b'+', 63: b'/', 64: b'=', 65: b'_', 66: b'-'}
CIPHER_WHEEL_L = {b'A': 0, b'B': 1, b'C': 2, b'D': 3, b'E': 4, b'F': 5, b'G': 6, b'H': 7, b'I': 8, b'J': 9, b'K': 10, b'L': 11, b'M': 12, b'N': 13, b'O': 14, b'P': 15, b'Q': 16, b'R': 17, b'S': 18, b'T': 19, b'U': 20, b'V': 21, b'W': 22, b'X': 23, b'Y': 24, b'Z': 25, b'a': 26, b'b': 27, b'c': 28, b'd': 29, b'e': 30, b'f': 31, b'g': 32, b'h': 33, b'i': 34, b'j': 35, b'k': 36, b'l': 37, b'm': 38, b'n': 39, b'o': 40, b'p': 41, b'q': 42, b'r': 43, b's': 44, b't': 45, b'u': 46, b'v': 47, b'w': 48, b'x': 49, b'y': 50, b'z': 51, b'0': 52, b'1': 53, b'2': 54, b'3': 55, b'4': 56, b'5': 57, b'6': 58, b'7': 59, b'8': 60, b'9': 61, b'+': 62, b'/': 63, b'=': 64, b'_': 65, b'-': 66}


def get_salt(salt_file='/var/secure/robocrypt.salt'):
    with open(salt_file, 'rb') as sf:
        salt = sf.read()
    return salt


class CipherWorker(threading.Thread):
    def __init__(self, chunk: bytes, shift: int, action='cipher'):
        super().__init__()
        self.chunk = chunk
        self.chunk_length = len(chunk)
        self.shift = shift if action == 'cipher' else -shift
        self.result: bytes = b''

    def run(self):
        # print(f"crunching on a byte chunk with the length of {self.chunk_length}...")
        cipher_string = b''
        for byte in unpack(f'{self.chunk_length}c', self.chunk):
            cipher_string += CIPHER_WHEEL_N[(CIPHER_WHEEL_L[byte] + self.shift) % 67]

        self.result = cipher_string


def _chunker(obj, size: int):
    return (obj[pos:pos + size] for pos in range(0, len(obj), size))


def cipher_decipher(message: bytes, shift: int, action='cipher', threads: int = 1):
    cipher_threads = []
    # spin up as many threads as we're asked too
    for byte_chunk in _chunker(message, int(len(message)/threads)):
        c_processor = CipherWorker(byte_chunk, shift, action=action)
        c_processor.start()
        cipher_threads.append(c_processor)
    # Get the results from the threads
    cipher_string = b''
    for t in cipher_threads:
        t.join()
        cipher_string += t.result

    return cipher_string


def get_kdf():
    return PBKDF2HMAC(
        algorithm=hashes.SHA512_224(),
        length=32,
        salt=get_salt(),
        iterations=724,
        backend=default_backend()
    )


def encrypt(message: bytes, password: bytes, shift: int = None, cipher_threads: int = 1):
    f = Fernet(base64.urlsafe_b64encode(get_kdf().derive(password)))
    encrypted_bytes = f.encrypt(message)

    if shift is not None:
        return cipher_decipher(encrypted_bytes, shift, action='cipher', threads=cipher_threads)
    return encrypted_bytes


class DecryptionError(Exception):
    def __init__(self):
        super(DecryptionError, self).__init__()


def decrypt(message: bytes, password: bytes, shift: int = None, cipher_threads: int = 1):
    f = Fernet(base64.urlsafe_b64encode(get_kdf().derive(password)))

    if shift is not None:
        message = cipher_decipher(message, shift, action='decipher', threads=cipher_threads)
    try:
        return f.decrypt(message)
    except InvalidToken:
        raise DecryptionError


def encrypt_file(filepath: str, password: str, shift: int = 17, cipher_threads: int = 1):
    chunks = filepath.split('/')
    path = '/'.join(chunks[:-1])
    filename, ext = chunks[-1].split('.')

    with open(filepath, 'rb') as f:
        content = f.read()

    encrypted_content = encrypt(content, password.encode(), shift=shift, cipher_threads=cipher_threads)

    with open(f"{path}/{filename}.{ext}.robo", 'wb') as enc_f:
        enc_f.write(encrypted_content)

    os.remove(filepath)


def decrypt_file(filepath: str, password: str, shift: int = 17, cipher_threads: int = 1):
    chunks = filepath.split('/')
    path = '/'.join(chunks[:-1])
    filename, ext, _ = chunks[-1].split('.')

    with open(filepath, 'rb') as f:
        encrypted_content = f.read()

    try:
        decrypted_content = decrypt(encrypted_content, password=password.encode(), shift=shift, cipher_threads=cipher_threads)
    except AttributeError:
        raise DecryptionError

    with open(f"{path}/{filename}.{ext}", 'wb') as dcrp_f:
        dcrp_f.write(decrypted_content)

    os.remove(filepath)


def read_encrypted_file(filepath: str, password: str, shift: int = 17) -> bytes:
    with open(filepath, 'rb') as f:
        encrypted_content = f.read()

    try:
        decrypted_content = decrypt(encrypted_content, password=password.encode(), shift=shift)
    except AttributeError:
        raise DecryptionError

    return decrypted_content


if __name__ == '__main__':
    # Let's goooooooooo! (https://genius.com/Chris-brown-look-at-me-now-lyrics xpath-> /html/body/div[1]/main/div[2]/div[2]/div[2]/div/div[4]/text()[5])
    import argparse

    parser = argparse.ArgumentParser(
        allow_abbrev=True,
        prog='robocrypt',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
    ____        __             __ __
   / __ \____  / /_  ____     / // /
  / /_/ / __ \/ __ \/ __ \   / // /_
 / _, _/ /_/ / /_/ / /_/ /  /__  __/
/_/ |_|\____/_.___/\____/     /_/
"""
    )
    parser.add_argument('action', help='encrypt or decrypt', choices=['encrypt', 'decrypt'])
    parser.add_argument('file', help='The file to encrypt/decrypt')
    parser.add_argument('-s', '--shift', type=int, help='The cipher shift to use')
    parser.add_argument('-t', '--threads', type=int, help='number of threads to use when ciphering (only if a shift value is set)', default=1)
    args = parser.parse_args()

    cryption = args.action.lower()[0:2]
    file_obj = Path(args.file)
    if not file_obj.exists():
        sys.exit(f"{args.file}: no such file or directory")
    else:
        file_path = file_obj.absolute().as_posix()
        pw = getpass.getpass(f"Enter password to {cryption}crypt: ")
        if cryption == 'en':  # 'en'cryption baby!
            encrypt_file(file_path, password=pw, shift=args.shift, cipher_threads=args.threads)
        elif cryption == 'de':  # 'de'cryption baby!
            decrypt_file(file_path, password=pw, shift=args.shift, cipher_threads=args.threads)
