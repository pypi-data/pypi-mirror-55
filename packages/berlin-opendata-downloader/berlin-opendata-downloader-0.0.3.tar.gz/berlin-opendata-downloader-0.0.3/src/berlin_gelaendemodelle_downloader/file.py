
import re
import os

from glob import glob


def write_file_content(download_path: str, file_name: str, file_content: str) ->  None:
    """
    Writes the given ``file_content`` to the given path.

    Args:
        download_path (str): directory
        file_name (str): file name
        file_content (str): file content
    """

    with open(os.path.join(download_path, file_name), mode="w") as file:
        file.writelines("\n".join(file_content))



def fix_file_names(download_path: str) -> None:
    """
    Fix all the not constant named files.

    Args:
        download_path (str): directory of the downloaded files.
    """

    files = glob(os.path.join(download_path, "*"))

    for file in files:
        if not re.match(r".*\d{3}_\d{4}\.", file):
            os.rename(file, file.replace(file[-8:], f"_{file[-8:]}"))

        if not re.match(r".*\.txt", file):
            file_wo_extension, _ = os.path.splitext(file)
            os.rename(file, file_wo_extension + ".txt")
