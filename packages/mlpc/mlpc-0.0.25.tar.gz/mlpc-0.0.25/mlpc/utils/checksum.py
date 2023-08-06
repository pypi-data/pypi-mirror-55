import hashlib
import os
from shutil import copyfile
import base64

MLPC_CHECKSUM_FILENAME = "mlpc_checksum.txt"
MLPC_CHECKSUM_CHECKSCRIPT = "mlpc_verify_folder_is_unchanged.py"


def _generate_checksum(folder_path):
    sha = hashlib.sha256()
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if not file_name == MLPC_CHECKSUM_FILENAME and not file_name == MLPC_CHECKSUM_CHECKSCRIPT and not file_name == "output.log":
                file_paths.append(os.path.abspath(os.path.join(root, file_name)))
    # File names
    for file_path in file_paths:
        sha.update(str.encode(file_path))
    # File content
    for file_path in file_paths:
        with open(file_path, 'rb') as f:
            while 1:
                buf = f.read(4096)
                if not buf:
                    break
                buf_base64 = base64.b64encode(buf)
                buf_sha = hashlib.sha256(buf_base64).digest()
                sha.update(buf_sha)
    checksum = sha.hexdigest()
    return checksum


def generate_and_write_checksum_file(folder_path):
    checksum = _generate_checksum(folder_path)
    with open(os.path.join(folder_path, MLPC_CHECKSUM_FILENAME), "x") as checksum_file:
        checksum_file.writelines(checksum)


def place_checkscript(folder_path):
    src = os.path.abspath(__file__)
    dst = os.path.join(folder_path, MLPC_CHECKSUM_CHECKSCRIPT)
    copyfile(src, dst)


if __name__ == "__main__":
    mlpc_metadata_file = "mlpc_metadata.json"
    if not os.path.isfile(mlpc_metadata_file):
        print("Script must be run from mlpc run folder, where " + mlpc_metadata_file + " is located.")
        exit()
    with open(MLPC_CHECKSUM_FILENAME) as cf:
        existing_checksum = cf.read()
        print("Existing checksum: " + existing_checksum)
    new_checksum = _generate_checksum(".")
    print("New checksum: " + new_checksum)
    if existing_checksum == new_checksum:
        print('')
        print('OK - Everything looks fine.')
    else:
        print('Checksum mismatch, has anything been altered, added or removed?')
