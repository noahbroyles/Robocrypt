# Robocrypt
## Super strong python3 encryption program with file and folder support

With Robocrypt you can encrpyt/decrypt messages, files, or folders using a password.
Don't look at the code too hard... It's messy. I modifed an old program to use stronger encryption.

_TO DO_: Clean up and modularize code, possibly add encryption support for drive partions

### To get started:
`python3 -m pip install -r requirements.txt`
Before you can start encrypting stuff, you first need to generate a salt using `python3 generateSalt.py <salt length>`. Make sure whatever user you run as can access `/var/secure` and *ONLY* that user.
#### Warning! If you change your salt you will no longer be able to decrypt anything encrypted with the previous salt!!! Be careful!

### To Encrypt / Decrypt a message:
Run `python3 Robocrypt.py`. Follow the prompts for Encryption / Decryption.

### To Encrypt / Decrypt a file or folder:
Run `python3 Robocrypt.py <path/to/thing>`. Follow the prompts.
