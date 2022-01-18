import os
import robocrypt

from pathlib import Path


pw = 'all that wolfin on the net'

src_path = Path('tests/data/src')


def get_all_sub_objects_of(path: Path):
    sub_objects = []
    c_objects = [Path(f.path) for f in os.scandir(path)]
    for obj in c_objects:
        if obj.is_dir():
            sub_objects += get_all_sub_objects_of(obj)
        else:
            sub_objects.append(obj)
    return sub_objects


pre_existing_files = get_all_sub_objects_of(src_path)


def test_folder_encryption():
    robocrypt.encrypt_file(src_path.as_posix(), pw)

    assert not src_path.exists()
    assert Path('tests/data/src.robodir').exists()


def test_folder_decryption():
    robocrypt.decrypt_file('tests/data/src.robodir', pw)

    assert not Path('tests/data/src.robodir').exists()
    assert src_path.exists()
    for path in pre_existing_files:
        assert path.exists()
