import os
from pathlib import Path


def ensure_path_exists(path: Path) -> None:
  '''
  Makes sure the folder exists on disk.

  Args:
    :param path: Path string to the folder we want to create.
  '''
  if not path.exists():
    path.mkdir(parents=True)


def ensure_directory_exists(dir_name: str) -> None:
  '''
  Makes sure the folder exists on disk.

  Args:
    dir_name: Path string to the folder we want to create.
  '''
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)
