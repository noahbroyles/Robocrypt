# Robocrypt
## Super strong python3 encryption program with file and folder support

Due to the encryption algorithm in use here, large files should not be encrypted with this tool. Robocrypt keeps data in memory while encrypting/decrypting, so depending on the RAM in your system there will be a limit on the size of files you can encrypt with this tool.

Robocrypt is amazing for encrypting small files and folders with sensitive data. I guarantee that ain't nobody gonna break the encryption, unless you use a shitty password.

## Setup:
Create a `secure` directory with whatever permissions you decide are appropriate:
```console
$ sudo mkdir /var/secure
$ sudo chmod <whatever> /var/secure
```  
Generate a salt to use when encrypting stuff:
```console
$ ./generateSalt 1247
```  
Make sure that you decrypt anything you've encrypted with your current salt before you change it! Otherwise you will never recover files that you encrypted. 

## Docs:
```console
$ ./robocrypt.py --help
usage: robocrypt [-h] {encrypt,decrypt} file

    ____        __             __ __
   / __ \____  / /_  ____     / // /
  / /_/ / __ \/ __ \/ __ \   / // /_
 / _, _/ /_/ / /_/ / /_/ /  /__  __/
/_/ |_|\____/_.___/\____/     /_/

positional arguments:
  {encrypt,decrypt}  encrypt or decrypt
  file               The file or directory to encrypt/decrypt

optional arguments:
  -h, --help         show this help message and exit
```
When using the tool, don't jack around with the output files' extensions (`.robo` and `.robodir`). If you do this, you will regret it. Also I would recommend not to double-encrypt anything. Because of the way the program works with extensions, you'll end up screwing yourself. Encrypt your shit ***one*** time with a strong password.
