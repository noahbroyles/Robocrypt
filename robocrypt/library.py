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
    'DecryptionError',
    'SaltNotFoundError',
    'generate_salt',
    'get_salt_file',
    'get_salt',
    'get_kdf',
    'encrypt',
    'decrypt',
    'encrypt_file',
    'decrypt_file',
    'read_encrypted_file'
]


class DecryptionError(Exception):
    """This occurs when an invalid password is used to try to decrypt something, or the wrong salt is used.
    """
    def __init__(self):
        super(DecryptionError, self).__init__()


class SaltNotFoundError(FileNotFoundError):
    """This occurs when you attempt to use a salt location that does not exist.
    """
    def __init__(self, salt_location):
        super(FileNotFoundError, self).__init__(f'No salt found at {salt_location}. Try specifying a different salt or generating a new one.')


def get_salt_file() -> str:
    """Returns the location of the salt file used for cryptography.

    On Unix systems the salt file is at `/var/secure/robocrypt.salt`, and on Windows the salt is at `C:/secure/robocrypt.salt`. If a custom salt is specified in the environment variable `ROBO_SALT_FILE`, it will be used instead of the OS default.

    Returns:
        str: the path the to salt file
    """
    if os.environ.get("ROBO_SALT_FILE", False):
        return os.environ['ROBO_SALT_FILE']

    if platform.system() == 'Windows':
        sf = 'C:/secure/robocrypt.salt'
    else:   # It could be Darwin >3 or Linux :)
        sf = '/var/secure/robocrypt.salt'
    
    return sf


os.environ["ROBO_SALT_FILE"] = get_salt_file()


def get_salt(salt_file: str = None) -> bytes:
    """Gets the salt bytes used to encrypt and decrypt things.

    If a salt file is not specified and the env var `ROBO_SALT_FILE` is not set, a default salt location for your OS will be used. If there is not a salt at that location, robocrypt will raise an error.

    Args:
        salt_file (str): a custom file to read the salt from.

    Returns:
        str: the salt bytes
    """
    # Support for Linux and Windows
    if not salt_file:
        salt_file = os.environ.get("ROBO_SALT_FILE", get_salt_file())

    if not Path(salt_file).exists():
        raise SaltNotFoundError(salt_file)

    with open(salt_file, 'rb') as sf:
        salt = sf.read()

    return salt


def get_kdf():
    """Gets a KDF object to perform cryptography with.

    Returns:
        PBKDF2HMAC: the KDF to perform encryption/decryption with
    """
    return PBKDF2HMAC(
        algorithm=hashes.SHA512_256(),
        length=32,
        salt=get_salt(),
        iterations=140000,
        backend=default_backend()
    )


def encrypt(message: bytes, password: bytes) -> bytes:
    """Encrypts a bytes message using the specified bytes password.

    Args:
        message (bytes): the message to encrypt
        password (bytes): the password to encrypt the message with

    Returns:
        bytes: the encrypted bytes
    """
    f = Fernet(base64.urlsafe_b64encode(get_kdf().derive(password)))
    encrypted_bytes = f.encrypt(message)

    return base64.urlsafe_b64decode(encrypted_bytes)


def decrypt(message: bytes, password: bytes) -> bytes:
    """Decrypt a chunk of bytes with a password.

    Args:
        message (bytes): The bytes to decrypt
        password (bytes): The password to decrypt the message with

    Returns:
        bytes: the decrypted bytes
    """
    f = Fernet(base64.urlsafe_b64encode(get_kdf().derive(password)))

    try:
        return f.decrypt(base64.urlsafe_b64encode(message))
    except InvalidToken:
        raise DecryptionError


def encrypt_file(filepath: str, password: str):
    """Encrypts a file and saves it with a .robo for file or .robodir extension for directories.

    Args:
        filepath (str): The file or directory to encrypt
        password (str): the password to encrypt the file with

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
    """Decrypts a file and saves it without its robo extension.

    Args:
        filepath (str): The encrypted file to decrypt
        password (str): The password to decrypt the file with

    """
    filepath = Path(filepath)
    parent_dir = filepath.parent
    fn = filepath.name
    directory = True if fn.endswith('.robodir') else False
    original_filename = fn[:-5] if fn.endswith('.robo') else fn[:-8]

    with open(filepath, 'rb') as f:
        encrypted_content = f.read()

    try:
        decrypted_content = decrypt(encrypted_content, password=password.encode())
    except AttributeError:
        raise DecryptionError

    if directory:
        # This was a robodir
        output = f"{parent_dir}/{original_filename}.zip"
    else:
        output = f"{parent_dir}/{original_filename}"

    with open(output, 'wb') as dcrp_f:
        dcrp_f.write(decrypted_content)

    if directory:
        # Unzip the zip
        new_dir = f"{parent_dir}/{original_filename}"
        os.mkdir(new_dir)
        shutil.unpack_archive(output, new_dir)
        os.remove(output)  # This is the temporary zip file

    os.remove(filepath)


def read_encrypted_file(filepath: str, password: str) -> bytes:
    """Returns the decrypted content of an encrypted file without decrypting the file itself.

    Args:
        filepath (str): the encrypted file to read
        password (str): the password to use to read the file

    Returns:
        bytes: the file's decrypted content in bytes

    """
    with open(filepath, 'rb') as f:
        encrypted_content = f.read()

    try:
        decrypted_content = decrypt(encrypted_content, password=password.encode())
    except AttributeError:
        raise DecryptionError

    return decrypted_content


def generate_salt(length: int):
    """Generates a salt and stores it in the file indicated by the ENV var 'ROBO_SALT_FILE'

    Args:
        length (int): the number of bytes to contain in the salt

    Returns:
        str: the location of the new salt file
    """
    salt_file = get_salt_file()
    try:
        path = '/'.join(salt_file.split('/')[:-1])
        if not os.path.exists(path):
            os.mkdir(path)

        with open(salt_file, 'wb') as sf:
            sf.write(os.urandom(length))
    except PermissionError:
        who_let_the_salt_out = 'administrator' if platform.system() == 'Windows' else 'sudo'
        sys.exit(f'Permission Denied: You may need to run as {who_let_the_salt_out}')

    return salt_file
