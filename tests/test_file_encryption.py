import robocrypt

from pathlib import Path


pw = 'dont need security in the clubbbb'
with open('tests/data/Dictionary.java', 'rb') as f:
    og_content = f.read()


def test_file_encryption():
    robocrypt.encrypt_file('tests/data/Dictionary.java', pw)

    assert not Path('tests/data/Dictionary.java').exists()
    assert Path('tests/data/Dictionary.java.robo').exists()


def test_file_decryption():
    robocrypt.decrypt_file('tests/data/Dictionary.java.robo', pw)

    assert not Path('tests/data/Dictionary.java.robo').exists()
    assert Path('tests/data/Dictionary.java').exists()


def test_content():
    with open('tests/data/Dictionary.java', 'rb') as f:
        decrypted_content = f.read()

    assert og_content == decrypted_content
