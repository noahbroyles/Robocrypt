#!/usr/bin/python3 

try:
    # Caesar Cipher has now become robocrypt and uses super strong Encryption instead of a cipher. Hehe hackers! 
    import posixpath as path
    import base64, os, getpass, sys, contextlib, readline
    import pyperclip
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.fernet import Fernet

    robo = """
    ____        __             _____
   / __ \____  / /_  ____     |__  /
  / /_/ / __ \/ __ \/ __ \     /_ < 
 / _, _/ /_/ / /_/ / /_/ /   ___/ / 
/_/ |_|\____/_.___/\____/   /____/      

    """
    columns = os.popen('stty size', 'r').read().split()[1]
    if int(columns) >= 40:
        print(robo)

    # Set the salt to a secure random value
    with open('/var/secure/robocrypt.salt', 'rb') as sf:
        salt = sf.read()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=23,
        backend=default_backend()
    )


    def getMessage():
        """Returns a string input from the keyboard"""
        print('Enter your message:\n')
        return input()


    def encrypt(message, password):
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        return f.encrypt(message)


    def decrypt(message, password):
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        try:
            return f.decrypt(message)
        except:
            return False  # wrong password


    # Here comes the code to be run if there is no file involved.
    def noarg():
        print("Do you wish to encrypt or decrypt a message? ")
        mode = input().lower()
        if mode[0] == "e":
            message = getMessage()
            print()
            print("Enter the password to encrypt this with: ")
            password = getpass.getpass().encode()
            print()
            encodedMessage = message.encode()
            encryptedMessage = encrypt(encodedMessage, password)
            # Give it out
            print('Your translated text is:')
            print()
            tran_mess = encryptedMessage.decode()
            print(tran_mess)
            print()
            if input('Would you like to have your message copied? ').lower()[0] == 'y':
                pyperclip.copy(tran_mess)
                print('Your message was copied. All you have to do is paste.')
            sys.exit()
        else:
            message = getMessage().encode()
            print()
            print("Enter the password to decrpyt this with: ")
            password = getpass.getpass().encode()
            decryptedMessage = decrypt(message, password)
            try:
                tran_mess = decryptedMessage.decode()
            except:
                sys.exit("Wrong password.")
            print('Your translated text is:')
            print()
            print(tran_mess)
            print()
            if input('Would you like to have your message copied? ').lower()[0] == 'y':
                pyperclip.copy(tran_mess)
                print('Your message was copied. All you have to do is paste.')
            else:
                pass
            sys.exit()


    # Here comes the code to be run if there is yes a file involved.
    if len(sys.argv) == 1:
        noarg()
    else:
        filename = sys.argv[1]
        path = filename
        if not os.path.exists(filename):
            print(filename, "was not found.")
            sys.exit()
        if os.path.isdir(filename):  # This is a folder we need to
            mode = input('Would you like to encrypt this folder? ').lower()
            if mode[0] in ["y", 'e']:
                if input("Encrypting this folder will first zip it and then encrypt the zip. The zip must first be decrypted by this program and then unzipped. Is that okay? ").lower()[0] == "y":
                    print("Enter the password to encrypt this folder with: ")
                    password = getpass.getpass().encode()
                    os.system(f"zip -rv {path[:-1] if path.endswith('/') else path}.zip.roboFolder {filename}")
                    os.system("rm -fr " + filename)
                    print()
                    filename = f"{path[:-1] if path.endswith('/') else path}.zip.roboFolder"
                    file = open(filename, 'rb')
                    encodedMessage = file.read()
                    file.close()
                    encryptedMessage = encrypt(encodedMessage, password)
                    file = open(filename, 'wb')
                    file.write(encryptedMessage)
                    file.close()
                    print('The folder was encrypted succesfully and stored as an encrypted zipped folder only readable by this program named "' + filename + '"')
                else:
                    print('Your files weren\'t touched.')
                    sys.exit()

        elif "roboFolder" in filename:
            print("Enter the password to decrpyt this roboFolder with: ")
            password = getpass.getpass().encode()
            file = open(filename, 'rb')
            encodedMessage = file.read()
            file.close()
            decryptedMessage = decrypt(encodedMessage, password)
            if not decryptedMessage:
                print("Wrong Password.")
                sys.exit()
            else:
                print('\nWorking...')
                file = open(filename, 'wb')
                file.write(decryptedMessage)
                file.close()
                filename = filename.replace(".roboFolder", "")
                os.rename(path, filename)
                os.system("unzip -qq " + filename)
                os.system("rm -fr " + filename)
                print("The roboFolder was decrypted succesfully. ")
        elif "roboFile" in filename:
            print("Enter the password to decrpyt this roboFile with: ")
            password = getpass.getpass().encode()
            file = open(filename, 'rb')
            encodedMessage = file.read()
            file.close()
            decryptedMessage = decrypt(encodedMessage, password)
            if not decryptedMessage:
                print("Wrong Password.")
                sys.exit()
            else:
                print('\nWorking...')
                file = open(filename, 'wb')
                file.write(decryptedMessage)
                file.close()
                filename = filename.replace(".roboFile", "")
                os.rename(path, filename)
                print("The roboFile was decrypted succesfully. ")
        else:
            mode = input('Would you like to encrypt this file? ')
            if mode[0] in ["e", "y"]:
                if input("Encrypting this file will make it only readable by this program. Is that okay? ").lower()[0] == "y":
                    print()
                    print("Enter the password to encrypt this file with: ")
                    password = getpass.getpass().encode()
                    file = open(filename, 'rb')
                    encodedMessage = file.read()
                    file.close()
                    encryptedMessage = encrypt(encodedMessage, password)
                    file = open(filename, 'wb')
                    file.write(encryptedMessage)
                    file.close()
                    os.rename(path, (filename + ".roboFile"))
                    print("The file was encrypted succesfully. ")
                else:
                    print("Your file wasn't touched.")
                    sys.exit()



except KeyboardInterrupt:
    print('\nWow! You dare to Ctrl-C me?')
