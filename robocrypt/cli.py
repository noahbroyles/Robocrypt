import os
import sys
import getpass
import argparse

from pathlib import Path
from .info import version as prog_version
from .library import get_salt_file, generate_salt, encrypt_file, decrypt_file, DecryptionError


def command_line():
    """
    This is the command line entry point of robocrypt.
    """
    # Let's goooooooooo! (https://genius.com/Chris-brown-look-at-me-now-lyrics xpath-> /html/body/div[1]/main/div[2]/div[2]/div[2]/div/div[4]/text()[5])

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
    subparsers = parser.add_subparsers(dest='action', required=True)
    salt_parser = subparsers.add_parser('generate-salt', aliases=['gs'], help='generate and save a new random salt of a given length')
    salt_parser.add_argument('length', type=int, help='number of bytes in the salt')

    encryption_parser = subparsers.add_parser('encrypt', aliases=['en'], help='encrypt a file or directory')
    encryption_parser.add_argument('file', help='the file or directory to encrypt')

    decryption_parser = subparsers.add_parser('decrypt', aliases=['de'], help='decrypt a file or directory')
    decryption_parser.add_argument('file', help='the file or directory to decrypt')

    parser.add_argument('-s', '--salt-file', dest='salt_file', help='specify a salt file to use', default=False)
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {prog_version}')
    args = parser.parse_args()

    action = args.action.lower()[0:2]

    # Set the salt if there was a custom one
    if args.salt_file:
        os.environ["ROBO_SALT_FILE"] = args.salt_file

    # Start parsing commands
    if action in ['ge', 'gs']:
        if os.path.exists(get_salt_file()):
            like_for_real = input('Overwriting your old salt will render anything encrypted with it absolutely un-readable, unless you back it up.\nAre you sure you want to do this? ').lower()[0] == 'y'
        else:
            like_for_real = True
        if like_for_real:
            salt_location = generate_salt(args.length)
            print(f"Successfully saved a salt of length {args.length} to {salt_location}")
        else:
            print('Your salt file was not altered.')
            sys.exit()
    else:
        # We're encrypting or decrypting something
        file_obj = Path(args.file)
        if not file_obj.exists():
            sys.exit(f"{args.file}: no such file or directory")
        file_path = file_obj.absolute().as_posix()

        pw = getpass.getpass(f"Enter password to {action}crypt: ")
        if action == 'en':  # 'en'cryption baby!
            encrypt_file(file_path, password=pw)
            print(f"Successfully encrypted {file_path}!")
        elif action == 'de':  # 'de'cryption baby!
            try:
                decrypt_file(file_path, password=pw)
                print(f"Successfully decrypted {file_path}!")
            except DecryptionError:
                sys.exit('Invalid password or salt. Check your password and salt settings and try again.')


def robocrypt_main():
    try:
        command_line()
    except KeyboardInterrupt:
        sys.exit()
