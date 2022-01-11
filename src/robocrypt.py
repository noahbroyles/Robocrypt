#!/usr/bin/env python3

import os
import sys
import base64
import shutil
import getpass
import platform

from pathlib import Path
from functools import wraps
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# This is the version of the programme ;)
__version__ = '4.2Pro'


SPECIAL_SALT = False


def get_salt(salt_file: str = None):
    # Support for Linux and Windows
    if not salt_file and not SPECIAL_SALT:
        if os.path.exists('/var/secure/robocrypt.salt'):
            salt_file = '/var/secure/robocrypt.salt'
        elif os.path.exists('C:/secure/robocrypt.salt'):
            salt_file = 'C:/secure/robocrypt.salt'
        else:
            salt = b"Youngblood thinks there's always tomorrow I miss your touch some nights when I'm hollow I know you crossed a bridge that I can't follow Since the love that you left is all that I get, I want you to knowThat if I can't be close to you, I'll settle for the ghost of you I miss you more than life (More than life) And if you can't be next to me, your memory is ecstasy I miss you more than life, I miss you more than life"

    if SPECIAL_SALT:
        salt_file = SPECIAL_SALT

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

    return base64.urlsafe_b64decode(encrypted_bytes)


class DecryptionError(Exception):
    def __init__(self):
        super(DecryptionError, self).__init__()


def decrypt(message: bytes, password: bytes):
    f = Fernet(base64.urlsafe_b64encode(get_kdf().derive(password)))

    try:
        return f.decrypt(base64.urlsafe_b64encode(message))
    except InvalidToken:
        raise DecryptionError


def encrypt_file(filepath: str, password: str):
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
    with open(filepath, 'rb') as f:
        encrypted_content = f.read()

    try:
        decrypted_content = decrypt(encrypted_content, password=password.encode())
    except AttributeError:
        raise DecryptionError

    return decrypted_content


def map_subparser_to_func(func, subparser):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(subparser, *args, **kwargs)
    return wrapper


def generate_salt(length: int):
    if platform.platform() == 'Windows':
        salt_file = 'C:/secure/robocrypt.salt'
    else:
        salt_file = '/var/secure/robocrypt.salt'

    path = '/'.join(salt_file.split('/')[:-1])
    if not os.path.exists(path):
        os.mkdir(path)

    with open(salt_file, 'wb') as sf:
        sf.write(os.urandom(length))
    
    return salt_file

    

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
    subparsers = parser.add_subparsers(dest='action')
    salt_parser = subparsers.add_parser('generate-salt', aliases=['gs'], help='generate and save a new random salt of a given length')
    salt_parser.add_argument('x', type=int, help='number of bytes in the salt')
    # salt_parser.set_defaults(func=map_subparser_to_func(generate_salt, salt_parser))
    
    encryption_parser = subparsers.add_parser('encrypt', aliases=['en'], help='encrypt a file or directory')
    encryption_parser.add_argument('file', help='the file or directory to encrypt')
    encryption_parser.add_argument('-s', '--salt-file', dest='salt', help='specify a salt file to use', default=False)

    decryption_parser = subparsers.add_parser('decrypt', aliases=['de'], help='decrypt a file or directory')
    decryption_parser.add_argument('file', help='the file or directory to decrypt')
    decryption_parser.add_argument('-s', '--salt-file', dest='salt', help='specify a salt file to use', default=False)

    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()

    action = args.action.lower()[0:2]

    # Start parsing commands
    if action in ['ge', 'gs']:
        like_for_real = input('Overwriting your old salt will render anything encrypted with it absolutely un-readable, unless you back it up.\nAre you sure you want to do this? ').lower()[0] == 'y'
        if like_for_real:
            salt_location = generate_salt(args.x)
            print(f"Successfully saved a salt of length {args.x} to {salt_location}")
        else:
            print('Your salt file was not altered.')
            sys.exit()
    else:
        # We're encrypting or decrypting something
        file_obj = Path(args.file)
        if not file_obj.exists():
            sys.exit(f"{args.file}: no such file or directory")
        file_path = file_obj.absolute().as_posix()

        # Set the salt if there was a custom one
        SPECIAL_SALT = args.salt

        pw = getpass.getpass(f"Enter password to {action}crypt: ")
        if action == 'en':  # 'en'cryption baby!
            encrypt_file(file_path, password=pw)
            print(f"Successfully encrypted {file_path}!")
        elif action == 'de':  # 'de'cryption baby!
            try:
                decrypt_file(file_path, password=pw)
                print(f"Successfully decrypted {file_path}!")
            except DecryptionError:
                sys.exit('Invalid password or salt.')
