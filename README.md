# Robocrypt
## Super strong python3 encryption program with file and folder support

Due to the encryption algorithm in use here, large files should not be encrypted with this tool. Robocrypt keeps data in memory while encrypting/decrypting, so depending on the RAM in your system there will be a limit on the size of files you can handle with this tool.

Robocrypt is amazing for encrypting small files and folders with sensitive data. It uses symmetric key encryption, plus a salt of random bytes. I guarantee that ain't nobody gonna break the encryption, unless you use a sub-par password.

# Documentation Index:
- [Installation](#installation)
- [Setup](#setup)
- [Module Documentation](#module)
- [Command Line Docs](#command-line)

## <a id="installation"></a>Installation:
```console
pip3 install robocrypt
```

## <a id="setup"></a>Setup:
You only have to do this if you want to control the permissions and length of your salt. If you do not care about this stuff, skip this step and robocrypt will do it for you.  
<br>  
Create a `secure` directory in `/var` that only your user can read/write too:
```console
$ sudo mkdir /var/secure
$ sudo chmod 740 /var/secure
```
Generate a salt to use when encrypting stuff:
```console
$ robocrypt generate-salt 69173
```  
Make sure that you decrypt anything you've encrypted with your current salt(or back it up) before you change it! Otherwise you will never be able to recover files that you encrypted. 
If you intend to share encrypted files with someone, you also need to share your salt with them, or they will have serious trouble trying to decrypt the files.

# <a id="module"></a>Module `robocrypt`
## Sub-modules

* [robocrypt.cli](#robocrypt.cli)
* [robocrypt.info](#robocrypt.info)
* [robocrypt.library](#robocrypt.library)

    
# <a id="robocrypt.cli"></a>Module `robocrypt.cli`

    
## Functions

### Function `command_line`

>     def command_line()


This is the command line entry point of `robocrypt`.




    
# <a id="robocrypt.info"></a>Module `robocrypt.info`
This contains information about the module such as version and author.


    
# <a id="robocrypt.library"></a>Module `robocrypt.library`
This contains all the core functions used by `robocrypt`.

    
## Functions


    
### Function `decrypt`




>     def decrypt(
>         message: bytes,
>         password: bytes
>     ) ‑> bytes


Decrypt a chunk of bytes with a password.


**Args**  
**```message```** :&ensp;<code>bytes</code>
:   The bytes to decrypt


**```password```** :&ensp;<code>bytes</code>
:   The password to decrypt the message with



**Returns**  
<code>bytes</code>
:   the decrypted bytes



    
### Function `decrypt_file`




>     def decrypt_file(
>         filepath: str,
>         password: str
>     )


Decrypts a file and saves it without its robo extension.


**Args**  
**```filepath```** :&ensp;<code>str</code>
:   The encrypted file to decrypt


**```password```** :&ensp;<code>str</code>
:   The password to decrypt the file with



    
### Function `encrypt`




>     def encrypt(
>         message: bytes,
>         password: bytes
>     ) ‑> bytes


Encrypts a bytes message using the specified bytes password.


**Args**  
**```message```** :&ensp;<code>bytes</code>
:   the message to encrypt


**```password```** :&ensp;<code>bytes</code>
:   the password to encrypt the message with



**Returns**  
<code>bytes</code>
:   the encrypted bytes



    
### Function `encrypt_file`




>     def encrypt_file(
>         filepath: str,
>         password: str
>     )


Encrypts a file and saves it with a `.robo` for file or `.robodir` extension for directories. I strongly advise that you not mess with the extensions if you want to be able to properly decrypt your files.


**Args**  
**```filepath```** :&ensp;<code>str</code>
:   The file or directory to encrypt


**```password```** :&ensp;<code>str</code>
:   the password to encrypt the file with



    
### Function `generate_salt`




>     def generate_salt(
>         length: int
>     )


Generates a salt and stores it in the file indicated by the ENV var `ROBO_SALT_FILE`.


**Args**  
**```length```** :&ensp;<code>int</code>
:   the number of bytes to contain in the salt



**Returns**  
<code>str</code>
:   the location of the new salt file

    
### Function `get_kdf`


>     def get_kdf()


Gets a KDF object to perform cryptography with.


**Returns**  
<code>PBKDF2HMAC</code>
:   the KDF to perform encryption/decryption with



    
### Function `get_salt`




>     def get_salt(
>         salt_file: str = None
>     ) ‑> bytes


Gets the salt bytes used to encrypt and decrypt things.  
If a salt file is not specified and the env var `ROBO_SALT_FILE` is not set, a default salt location for your OS will be used. If there is not a salt at that location, robocrypt will raise an error.  
The salt file location is stored in the environment variable `ROBO_SALT_FILE`. You can modify this environment variable to point to different salt files if desired.


**Args**  
**```salt_file```** :&ensp;<code>str</code>
:   a custom file to read the salt from.



**Returns**  
<code>str</code>
:   the salt bytes



    
### Function `get_salt_file`

>     def get_salt_file() ‑> str


Returns the location of the salt file used for cryptography.  
On Unix systems the salt file is at `/var/secure/robocrypt.salt`, and on Windows the salt is at `C:/secure/robocrypt.salt`. If a custom salt is specified in the environment variable `ROBO_SALT_FILE`, it will be used instead of the OS default.


**Returns**  
<code>str</code>
:   the path the to salt file


### Function `read_encrypted_file`

>     def read_encrypted_file(
>         filepath: str,
>         password: str
>     ) ‑> bytes


Returns the decrypted content of an encrypted file without decrypting the file itself.


**Args**  
**```filepath```** :&ensp;<code>str</code>
:   the encrypted file to read


**```password```** :&ensp;<code>str</code>
:   the password to use to read the file

**Returns**  
<code>bytes</code>
:   the file's decrypted content in bytes


## Classes
### Class `DecryptionError`
>     class DecryptionError


This occurs when an invalid password is used to try to decrypt something, or the wrong salt is used.

-----
<small>Generated by *pdoc* 0.10.0 (<https://pdoc3.github.io>). That's why the documentation looks like crap.</small>


# <a id="command-line"></a>Robocrypt Command Line:
Here is the `help` for the robocrypt CLI:
```console
usage: robocrypt [-h] [-s SALT_FILE] [-v] {generate-salt,gs,encrypt,en,decrypt,de} ...

        ____        __             __ __
       / __ \____  / /_  ____     / // /
      / /_/ / __ \/ __ \/ __ \   / // /_
     / _, _/ /_/ / /_/ / /_/ /  /__  __/
    /_/ |_|\____/_.___/\____/     /_/   
    

positional arguments:
  {generate-salt,gs,encrypt,en,decrypt,de}
    generate-salt (gs)  generate and save a new random salt of a given length
    encrypt (en)        encrypt a file or directory
    decrypt (de)        decrypt a file or directory

optional arguments:
  -h, --help            show this help message and exit
  -s SALT_FILE, --salt-file SALT_FILE
                        specify a salt file to use
  -v, --version         show program's version number and exit
```
The commands you can use are these:  
- `generate-salt` or shortcut `gs`
- `encrypt` or shortcut `en`
- `decrypt` or shortcut `de`

To specify a salt file to generate, encrypt, or decrypt, use the argument `--salt-file /path/to/saltfile`.  
## `generate-salt`:
**Generate a salt in the default location**:
```console
$ sudo robocrypt generate-salt 5829
Overwriting your old salt will render anything encrypted with it absolutely un-readable, unless you back it up.
Are you sure you want to do this? yes
Successfully saved a salt of length 5829 to /var/secure/robocrypt.salt
```
Robocrypt will ask you if you really want to overwrite any existing salt files. Answering `no` at the prompt will exit the program without touching the salt.

**Generate a salt to a specific file**:
```console
$ sudo robocrypt --salt-file /var/secure/myother.salt generate-salt 5829
Successfully saved a salt of length 5829 to /var/secure/myother.salt
```
Here we were not prompted to confirm because there was no previous file at `/var/secure/myother.salt`.

## `encrypt`:  
**Encrypt a file**:
```
$ robocrypt encrypt tests/data/Dictionary.java 
Enter password to encrypt: 🔑
Successfully encrypted /path/tests/data/Dictionary.java!
$ ls tests/data/
Dictionary.java.robo  src
```
You can see that `Dictionary.java` was encrypted and saved as `Dictionary.java.robo`.  

**Encrypt a folder with a specified salt**:
```console
$ robocrypt --salt-file /var/secure/alternate.salt encrypt tests/data/src/
Enter password to encrypt: 🔑
Successfully encrypted /path/tests/data/src!
$ ls tests/data/
Dictionary.java.robo  src.robodir
```
The `src` directory was encrypted and saved as `src.robodir` using the `alternate.salt`.  

## `decrypt`:
**Decrypt a file**:
```console
$ robocrypt decrypt tests/data/Dictionary.java.robo 
Enter password to decrypt: 🔑
Successfully decrypted /path/tests/data/Dictionary.java.robo!
$ ls tests/data/
Dictionary.java  src.robodir
```
`Dictionary.java` was restored to its original state with only the `.java` extension.  

**Decrypt a folder with a specified salt**:
```console
$ robocrypt --salt-file /var/secure/alternate.salt decrypt tests/data/src.robodir
Enter password to decrypt: 🔑
Successfully decrypted /path/tests/data/src.robodir!
$ ls tests/data/
Dictionary.java  src
```
Now the `src` directory is back to normal, with no `.robodir` extension.

## Warning!
When using the tool, don't jack around with the output files' extensions (`.robo` and `.robodir`). Robocrypt uses these extensions to tell what type of file is encrypted and if change them, you will regret it. Also, I would recommend not double-encrypting anything. Because of the way the program works with extensions, you'll end up screwing yourself. Encrypt your shit ***one*** time with a strong password.
<br>