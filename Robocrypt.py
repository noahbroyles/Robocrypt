try:
    # Caesar Cipher has now become robocrypt and uses super strong Encryption instead of a cipher. Hehe hackers! 
    import posixpath as path
    import base64, os, getpass, sys, pyperclip, contextlib, readline
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
    salt = b"""3=\x07\xb0\xbd\xf1\x0e\x84\xdf}\xecmT+\x83\x93\'\x1fK?\xe9W\xa0\x8c\x88\x98\xf0\xaf\xf9\x8c\xc0\xd8\xbeb\xd2\x99\x95qz\xce\x94\xb3\xc6\xb4\x0e\x0b"\x83|\xd87O$\xf8\x85xg\x85\x0b4\xe5;\x81\xd4\'*\xf7\x14\x8a\x98\xd2\r\x14kb\xa6.\x14L\xcf\xc4\x93\x8f\x99r\x07\xdc\x1d\xc3\x825\xaaF\x98\xb3Z\x00\x98\xdf\xb1\xedfp\x90_\xab\xee+\xf1\x1f\x93\xd2\x1a4\xd8\xed\xd4jN \x94\xbfH\xf6r\xaa*\xe6\xd6\x87S\x83\xc8\xb4\xb9|\x91:}\xc7*=BD\xc6\xefyXh\x94\x0b\x16\xaf\xc9\t-\x1e\xde\xa0\xfc\xa2\xe3\xe3\x99C\x1by\n\x00\x13,6\xed\xec.c\x8c\x18\xbfu\xb3\xb8~H0\xbb$S_\x1f\xd3\xbe\xb6\x19\xde\n0\x10\x9c\x80\xb2\x91&c\x19\xed\\T\x12#\xdeN\xa0\x1di#R\x95\xc2\xd0=\x16g|\x99\xe0j\xfd\xe1v\x8f\xa1\x93<\x88\xba\xaffB\x05\x89\xb1\x01\x14\xb8c\x08\x15\x15\xb7{O\xdb\xf3\xc7C]%\x9a:k\xa4W\xd0~:xXI\xa4\xbbW\x02\xcb\xca\x8a\xceNO!\xd0\'\xc3\x14?\xb5\x9fO\x16\xd8\x88}\xd0\n\x0e\xe8\xb1\x86\xdd\xc2\xbc%\xed7\xbd\x0fj\x0ee\xb7\xce;\rG\xa1NR\x1b\xf7\x86\x1b\x85\x86\xe4$:\xb0\x89\xdf\xd1@\x07\x13\xab%\xd7\xda\xd6\x1b3\x00\xc4\xfb\xb0\xdaZz\xc4\x92y\x81o\xb4\xec\x08\xf8\xaf\x81\tx\xee\x84\xaa\xc2Af\xcb\x90\x1b0\x92*\xe2\xf3\xfb\x06\xe5\x05S\x9b}\x83\xbd\xc7\x0b\xb5f\xa9K\xab\x91|\xcfL\x1f\xe6b\xa2\xf2\x1c\xea\xb3\x89\xed\x16\xdc5w\xcf\xfc%7\x8b\n\x00\xdd\x02\xb9r\x87>\xd90\xcc\x07\x88\x1d\x9e\x00\x86\x8b\xda\xfbC\xa11\xfcI\xb8\xff6\xfb(\xfa\xf4\xa3>\xd1+\x9f\xe7s\xbd\x16\xcbf[X\xba\xcd\xccD\x19,\x18\xe7\xbf\x11+\xb8\xaf\t\x88\x97\xc2\x96\xa2\xdd\xe8(\rf\xc4\xd2\xd0\xb8&\xe9>\xaa\xce5\xfc\x9e\x8c5]\xbe\xcf\\\x9e\\\xe8\x7f\x7f\x07~l\xf3\x92kRe\x9cN\x0c\x85{O\x80\x8e\xdd\x03:\xddI\x05L\xeb&\xe6\x1a\xae\xf2u\x16\x12j4\xda\xad\x1c\x97\xb2\xf1\xcc\x88\x8f\xe2\xb7p\xeb\xb1|2\xb86\xc9k71\xa3\x11\xa2\x7f\xeb\xe4\xcao\x0c\xa7L\x95j\xa2I#\xca\xcac\xf7f\x1f\xbc\x03\x83\xf1\xa3\xc8\x8e+J\xfd\x7f\x07\xec\xf4\xb5\xc5_)\xff\xf2t<L\xc5%\xba\xc9T\xb7\xda\x18K\xb7\xb5\x14\xc5\xda\xf4Cc\xb1\xcf\x1a\x16B6\xca\x18}\xc2\n\xa4j\x8e\xcdPDK\x91\xdcR\xa0\x06\x93\xbb\xce\x0crM\xdc\xc7/\xb6\xef\xd3\x12\xb3\\\xfe\x16\xe4 \x10g5\xbf\xf0\x1f\x83\xa5Q\x8e\x05^\xfa,\xfbd\xc5\xfdhN\x8a\x96\xb1\xdc\xf8\x19w\\\xd3\x9cP)$\xdb\x87a\xae\xa5\x8d6\x88\x11i> \x11\x85`\x15\x8f\x8eZ\xea?\x8eQ\xae\xb8\x15\xde\xb8C\\\xe2\xdb\xda\x88\x9fY\x85\xebK\xf0N\xc5\xb2\x1f\x12\x1b\x84\xa1\xef/\xf5z\xbcb\xf3D\xbe\xd2F\xc0\xe2\xc8\x15\xd9L\xf0+Y"\x81D\xbc\x98\x7f\xae\x1c\x0eRF7\x1fk\xcdK\xe9\xb3\xa0\xb1\xdc[\x82\x1b\xe7\x12\x8b\x8dQZw\x0e\x8aIc\x04\x8f\x0e\xd7\xc6\x1b`9\xa7\xec\x99\xc9`\xa8\xa8a\x8b{\xf0"\xd4S\xca\xd0\x0f/\xac\xa2<2\x93\x93\xe3n\xdaS\xe0\xafh\xd0\xf5\x9f\xc3+\xc9\x8b\x83\xf9z\xcd&Q1W\x85\x9a\xdb\xf6\xbe|\xd2\x06N\x1b$B=\x16\xf9)iM\x80\xa43.\x12^\xfaq\x9f\xeb)\xfb\x14\x8c\xb5\x00\x88\xc9\xce\xa0\x12!1_\xc9\xf8[R\xd2\xf56\xde\xc7\x9f\x044\x14\x0b\x1e\xb6ND\x92 c8}\xcd\xfb\x1e\xbe}x\x19\xf9\xfe\xfd\x1d\x12\x7f8B\xd0\x1f`\x90\xd8Ka=\x82\x05R\xee\xe9\xb4\x0e\x9em\x95\xf8\xbc\x02\x06[x\x93\xbc\xe8)\xf9\xb8Z\x02\x11\x08\x1a\xf8\x88\x92eH\x93\xdf\xb8\x83\x01I\xee\xfc\t\xf82\x03I\xe1\xca}p\xc9\xa1\x7f$\xfe\x13\xc0c-\xddH\x82*g\x04\xff{h\xfbr\x11\xf2\xb4h\xf4\xd7\xb9z!\x108\xf9\xcb>\x03\\w3O\x0ey\xffP\xbe\xed\x99=\x143\x8aO^\xa6\x0bJ\x19\xbb\xf1XS\xad\xa7A\xfbO\xc9h<\xf9\xd7\x16\xe3y\x1c\xd3\xa5\xc3\xfa]\xf9\x00\xb0\x14\xc4\xb4\xc77n\x1bC]\xcc\x07\x00\xe2A\xcek(\xe7\x0eA\x16\x1bR\xb7\xb0.>\xa7\xebDg\xdc\xa1#\xe9\xbc\xb4\x1d\x1f\x86\xedj\x0cO;\xb1"""

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

    def encrpyt(message, password):
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        return f.encrypt(message)
    
    def decrypt(message, password):
        key = base64.urlsafe_b64encode(kdf.derive(password))  
        f = Fernet(key)
        try:
            return f.decrypt(message)
        except:
            return False # wrong password

    #Here comes the code to be run if there is no file involved.
    def noarg():
        print("Do you wish to encrypt or decrypt a message? ")
        mode = input().lower()
        if mode[0] == "e":
            message = getMessage()
            print()
            print("Enter the password to encrpyt this with: ")
            password = getpass.getpass().encode()
            print()
            encodedMessage = message.encode()
            encryptedMessage = encrpyt(encodedMessage, password)
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
       

    #Here comes the code to be run if there is yes a file involved.
    if len(sys.argv) == 1:
        noarg()
    else:
        filename = sys.argv[1]
        path = filename
        if not os.path.exists(filename):
            print(filename, "was not found.")
            sys.exit()
        if os.path.isdir(filename): # This is a folder we need to 
            mode = input('Would you like to encrypt this folder? ').lower()
            if mode[0] in ["y", 'e']:
                if input("Encrypting this folder will first zip it and then encrpyt the zip. The zip must first be decrypted by this program and then unzipped. Is that okay? ").lower()[0] == "y":
                    print("Enter the password to encrpyt this folder with: ")
                    password = getpass.getpass().encode()
                    os.system("zip -rv " + path + ".zip.roboFolder " + filename)
                    os.system("rm -fr " + filename)
                    print()
                    filename = (path + '.zip.roboFolder')
                    file = open(filename, 'rb')
                    encodedMessage = file.read()
                    file.close()
                    encryptedMessage = encrpyt(encodedMessage, password)
                    file = open(filename, 'wb')
                    file.write(encryptedMessage)
                    file.close()
                    print('The folder was encrypted succesfully and stored as an encrpyted zipped folder only readable by this program named "' + filename + '"')
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
                    print("Enter the password to encrpyt this file with: ")
                    password = getpass.getpass().encode()
                    file = open(filename, 'rb')
                    encodedMessage = file.read()
                    file.close()
                    encryptedMessage = encrpyt(encodedMessage, password)
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
