import sys
import os
import re
from datetime import datetime
import shutil
import requests

_BIB_FILE_URL = "https://aclanthology.org/anthology.bib"
_BIB_FILE_BASE_NAME = "anthology"
_DATE_STR = datetime.now().strftime("%y%m%d")
_FOLDER_PATH = f"anthology_{_DATE_STR}"
_ZIP_FILE_PATH = f"anthology_bib-{_DATE_STR}"


def create_zip(folder_path: str, zip_file_path: str):
    """Creates a zip file from a folder."""

    shutil.make_archive(zip_file_path, 'zip', folder_path)
    print(f'zip file {zip_file_path} successfully created')


def combine_at_items(split_list):
    """Combines bibtex entries starting with '@' with the next item.

    Args:
        split_list: A list of string bibtex lines.

    Returns:
        A new list with combined items.
    """

    combined_list = []
    i = 0
    while i < len(split_list):
        if split_list[i].startswith('@'):
            # Combine the current item with the next one if it exists
            if i + 1 < len(split_list):
                combined_item = split_list[i] + split_list[i + 1]
                combined_list.append(combined_item)
                i += 2
            else:
                combined_list.append(split_list[i])
                i += 1
        else:
            combined_list.append(split_list[i])
            i += 1
    return combined_list


def split_individual_items(content: str):
    """Splits the anthology bib into individual bibtex items.

    Args:
        content: The content to split.

    Returns:
        A list of individual items.
    """
    # Split the content into individual items based on the marker
    split_values = re.split(r"\n(@[a-z]{1,}\{)", content)

    # Remove extra characters from each one
    split_values_clean = []
    for x in split_values:
        split_values_clean.append(re.sub('\t', '    ', x.strip('\n')))

    split_values_clean = combine_at_items(split_values_clean)
    return split_values_clean


def write_to_files(items: list, folder_path: str, bib_base_name: str, file_size_limit=45 * 1024 * 1024):
    """
    Writes items in a list to files, splitting them into multiple files if the size exceeds the limit.

    Args:
        items: The list of items to write.
        file_size_limit: The maximum size of each file in bytes (default: 50MB).
    """

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    current_file_size = 0
    file_index = 0
    current_file = os.path.join(folder_path, f"{bib_base_name}_{file_index}.bib")

    with open(current_file, "w", encoding="utf-8") as f:
        for item in items:
            item_size = len(str(item).encode("utf-8"))
            if current_file_size + item_size > file_size_limit:
                f.close()

                #create new file
                file_index += 1
                current_file = os.path.join(folder_path, f"{bib_base_name}_{file_index}.bib")
                current_file_size = 0
                f = open(current_file, "w", encoding="utf-8")

            # Write the item to the current file
            f.write(str(item) + "\n")
            current_file_size += item_size

    f.close()


def main():
    r = requests.get(_BIB_FILE_URL)
    if r.ok:
        print("Saving file.")
        split_vals = split_individual_items(r.content.decode("utf-8"))
        write_to_files(split_vals, _FOLDER_PATH, _BIB_FILE_BASE_NAME)
        create_zip(_FOLDER_PATH, _ZIP_FILE_PATH)
        shutil.rmtree(_FOLDER_PATH, ignore_errors=True)
    else:
        print("Download failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
