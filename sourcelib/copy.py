import os
import time
from pathlib import Path
from shutil import copy2, copytree


class NonExistingSourceFileError(Exception):
    ...


def copy(source_path: Path, destination_folder: Path) -> Path:

    if not _exists_with_retries(source_path):
        raise NonExistingSourceFileError(
            f"Can not copy {source_path} because it does not exists"
        )

    destination_path = _initialize_destination_path(source_path, destination_folder)

    if not destination_path.exists():
            
        _transfer_with_retries(source_path, destination_path)
        print(f"| Copied '{source_path}' | To: '{destination_path}'\n.")
    return destination_path


def _initialize_destination_path(source: Path, destination_folder: Path) -> Path:
    destination_folder = Path(destination_folder).resolve()
    destination_folder.mkdir(parents=True, exist_ok=True)
    return destination_folder / source.name


def _transfer(source: Path, destination_path: Path) -> None:
    transfer_function = copytree if os.path.isdir(source) else copy2
    transfer_function(str(source), str(destination_path))


def _transfer_with_retries(source: Path, destination_path: Path, retries: int = 5, delay: int = 5) -> None:
    transfer_function = copytree if os.path.isdir(source) else copy2
    attempt = 0
    while attempt < retries:
        try:
            transfer_function(str(source), str(destination_path))
            return
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
    raise Exception(f"Failed to copy {source} to {destination_path} after {retries} attempts")


def _exists_with_retries(path, retries=5, delay=5):
    for _ in range(retries):
        if path.exists():
            return True
        time.sleep(delay)
    print(f"File {path} does not exist, attempted {retries} retries")
    return False