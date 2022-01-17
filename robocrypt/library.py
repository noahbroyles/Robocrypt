#!/usr/bin/env python3

import os
import sys
import base64
import shutil
import platform

from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


__all__ = [
    'generate_salt',
    'get_salt_file',
    'get_salt',
    'get_kdf',
    'DecryptionError',
    'encrypt',
    'decrypt',
    'encrypt_file',
    'decrypt_file',
    'read_encrypted_file'
]


def get_salt_file() -> str:
    """
    Returns the location of the salt file used for cryptography
    :return: The path to the salt file
    """
    if platform.system() == 'Windows':
        sf = 'C:/secure/robocrypt.salt'
    else:
        sf = '/var/secure/robocrypt.salt'

    return sf


os.environ["robo-SALT_FILE"] = get_salt_file()


def get_salt(salt_file: str = None) -> bytes:
    """
    Returns the salt bytes used to encrypt and decrypt things.
    :param salt_file: The file to read the salt from. If not specified, a default for your OS will be used.
    :return: the salt bytes
    """
    # Support for Linux and Windows
    if not salt_file and not os.environ.get("robo-SALT_FILE", False):
        return b"Youngblood thinks there's always tomorrow I miss your touch some nights when I'm hollow I know you crossed a bridge that I can't follow Since the love that you left is all that I get, I want you to knowThat if I can't be close to you, I'll settle for the ghost of you I miss you more than life (More than life) And if you can't be next to me, your memory is ecstasy I miss you more than life, I miss you more than life"

    if not salt_file:
        salt_file = os.environ["robo-SALT_FILE"]

    with open(salt_file, 'rb') as sf:
        salt = sf.read()

    return salt


def get_kdf():
    """
    Returns a KDF object to perform cryptography with
    :return: a PBKDF2HMAC
    """
    return PBKDF2HMAC(
        algorithm=hashes.SHA512_256(),
        length=32,
        salt=get_salt(),
        iterations=140000,
        backend=default_backend()
    )


def encrypt(message: bytes, password: bytes) -> bytes:
    """
    Encrypts a bytes message using the specified bytes password
    :param message: the message to encrypt
    :param password: the password to encrypt the message with
    :return: Encrypted bytes
    """
    f = Fernet(base64.urlsafe_b64encode(get_kdf().derive(password)))
    encrypted_bytes = f.encrypt(message)

    return base64.urlsafe_b64decode(encrypted_bytes)


class DecryptionError(Exception):
    """
    This occurs when an invalid password is used to try to decrypt something, or the wrong salt is used.
    """
    def __init__(self):
        super(DecryptionError, self).__init__()


def decrypt(message: bytes, password: bytes) -> bytes:
    """
    Decrypt a chunk of bytes with a bytes password.
    :param message: The bytes to decrypt
    :param password: The password to decrypt the message with
    :return: the decrypted bytes
    """
    f = Fernet(base64.urlsafe_b64encode(get_kdf().derive(password)))

    try:
        return f.decrypt(base64.urlsafe_b64encode(message))
    except InvalidToken:
        raise DecryptionError


def encrypt_file(filepath: str, password: str):
    """
    Encrypts a file and saves it with a .robo for file or .robodir extension for directories.
    :param filepath: The file or directory to encrypt
    :param password: the password to encrypt the file with
    :return: None
    """
    filepath = Path(filepath)
    parent_dir = filepath.parent
    filename = filepath.name

    if filepath.is_dir():
        # This is a directory
        read_path = shutil.make_archive(f'{filepath}.robotmp', 'zip', filepath.as_posix())
        shutil.rmtree(filepath.as_posix())
        output_path = f"{parent_dir}/{filename}.robodir"
    else:
        # This is just a file
        read_path = filepath
        output_path = f"{parent_dir}/{filename}.robo"

    with open(read_path, 'rb') as f:
        content = f.read()

    encrypted_content = encrypt(content, password.encode())
    with open(output_path, 'wb') as enc_f:
        enc_f.write(encrypted_content)

    os.remove(read_path)


def decrypt_file(filepath: str, password: str):
    """
    Decrypts a file and saves it without its robo extension.
    :param filepath: The encrypted file to decrypt
    :param password: The password to decrypt the file with
    :return: None
    """
    filepath = Path(filepath)
    parent_dir = filepath.parent
    filename_parts = filepath.name.split('.')

    with open(filepath, 'rb') as f:
        encrypted_content = f.read()

    try:
        decrypted_content = decrypt(encrypted_content, password=password.encode())
    except AttributeError:
        raise DecryptionError

    if filename_parts[-1] == 'robodir':
        # This was a robodir
        output = f"{parent_dir}/{filename_parts[0]}.zip"
    else:
        output = f"{parent_dir}/{filename_parts[0]}.{filename_parts[1]}"

    with open(output, 'wb') as dcrp_f:
        dcrp_f.write(decrypted_content)

    if filename_parts[-1] == 'robodir':
        # Unzip the zip
        new_dir = f"{parent_dir}/{filename_parts[0]}"
        os.mkdir(new_dir)
        shutil.unpack_archive(output, new_dir)
        os.remove(output)  # This is the temporary zip file

    os.remove(filepath)


def read_encrypted_file(filepath: str, password: str) -> bytes:
    """
    Returns the decrypted content of an encrypted file without decrypting the file itself.
    :param filepath: the encrypted file to read
    :param password: the password(string) to use to read the file
    :return: the file's decrypted content in bytes
    """
    with open(filepath, 'rb') as f:
        encrypted_content = f.read()

    try:
        decrypted_content = decrypt(encrypted_content, password=password.encode())
    except AttributeError:
        raise DecryptionError

    return decrypted_content


def generate_salt(length: int):
    """
    Generates a salt and stores it in the file indicated by the ENV var 'robo-SALT_FILE'
    :param length: the number of bytes to contain in the salt
    :return: the location of the new salt file
    """
    try:
        path = '/'.join(os.environ["robo-SALT_FILE"].split('/')[:-1])
        if not os.path.exists(path):
            os.mkdir(path)

        with open(os.environ["robo-SALT_FILE"], 'wb') as sf:
            sf.write(os.urandom(length))
    except PermissionError:
        sys.exit('Permission Denied: You may need to run as sudo')

    return os.environ["robo-SALT_FILE"]
