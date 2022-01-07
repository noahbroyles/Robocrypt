#!/usr/bin/env python3

import os
import sys
import base64
import getpass

from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# This is the version of the programn ;)
__version__ = '4Pro'


def get_salt(salt_file='/var/secure/robocrypt.salt'):
    with open(salt_file, 'rb') as sf:
        salt = sf.read()
    return salt


def get_kdf():
    return PBKDF2HMAC(
        algorithm=hashes.SHA512_256(),
        length=32,
        salt=get_salt(),
        iterations=140000,
        backend=default_backend()
    )


def encrypt(message: bytes, password: bytes):
    f = Fernet(base64.urlsafe_b64encode(get_kdf().derive(password)))
    encrypted_bytes = f.encrypt(message)
    return encrypted_bytes


class DecryptionError(Exception):
    def __init__(self):
        super(DecryptionError, self).__init__()


def decrypt(message: bytes, password: bytes):
    f = Fernet(base64.urlsafe_b64encode(get_kdf().derive(password)))

    try:
        return f.decrypt(message)
    except InvalidToken:
        raise DecryptionError


def encrypt_file(filepath: str, password: str):
    chunks = filepath.split('/')
    path = '/'.join(chunks[:-1])
    filename, ext = chunks[-1].split('.')

    with open(filepath, 'rb') as f:
        content = f.read()

    encrypted_content = encrypt(content, password.encode())

    with open(f"{path}/{filename}.{ext}.robo", 'wb') as enc_f:
        enc_f.write(encrypted_content)

    os.remove(filepath)


def decrypt_file(filepath: str, password: str):
    chunks = filepath.split('/')
    path = '/'.join(chunks[:-1])
    filename, ext, _ = chunks[-1].split('.')

    with open(filepath, 'rb') as f:
        encrypted_content = f.read()

    try:
        decrypted_content = decrypt(encrypted_content, password=password.encode())
    except AttributeError:
        raise DecryptionError

    with open(f"{path}/{filename}.{ext}", 'wb') as dcrp_f:
        dcrp_f.write(decrypted_content)

    os.remove(filepath)


def read_encrypted_file(filepath: str, password: str) -> bytes:
    with open(filepath, 'rb') as f:
        encrypted_content = f.read()

    try:
        decrypted_content = decrypt(encrypted_content, password=password.encode())
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
    args = parser.parse_args()

    cryption = args.action.lower()[0:2]
    file_obj = Path(args.file)
    if not file_obj.exists():
        sys.exit(f"{args.file}: no such file or directory")
    else:
        file_path = file_obj.absolute().as_posix()
        pw = getpass.getpass(f"Enter password to {cryption}crypt: ")
        if cryption == 'en':  # 'en'cryption baby!
            encrypt_file(file_path, password=pw)
        elif cryption == 'de':  # 'de'cryption baby!
            decrypt_file(file_path, password=pw)
