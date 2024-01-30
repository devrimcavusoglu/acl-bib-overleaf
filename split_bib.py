import sys
from datetime import datetime

import requests

_BIB_FILE_URL = "https://aclanthology.org/anthology.bib"
_BIB_FILE_PATH = "anthology.bib"
_BIB_P1_PATH = "anthology.bib"
_BIB_P2_PATH = "anthology_p2.bib"
_ZIP_FILE_PATH = "anthology_bib-{strdate}.zip"
_SPLIT_MARKER = """
@inproceedings{reynolds-1952-conference,
    title = "The conference on mechanical translation held at {M}.{I}.{T}., {J}une 17-20, 1952",
    author = "Reynolds, Craig",
    booktitle = "Proceedings of the Conference on Mechanical Translation",
    month = "17-20 " # jun,
    year = "1952",
    address = "Massachusetts Institute of Technology",
    url = "https://aclanthology.org/1952.earlymt-1.26",
}
"""


def split_files(content: str):
    marker = _SPLIT_MARKER.strip()
    p1, p2 = content.split(marker)
    p1 += "\n" + marker
    with open(_BIB_P1_PATH, "w") as fd_out:
        fd_out.write(p1)
    with open(_BIB_P2_PATH, "w") as fd_out2:
        fd_out2.write(p2)


def create_zip():
    file_path = _ZIP_FILE_PATH.format(strdate=datetime.now().strftime("%y%m%d"))



def main():
    r = requests.get(_BIB_FILE_URL)
    if r.ok:
        print("Saving file.")
        split_files(r.content.decode("utf-8"))
        create_zip()
    else:
        print("Download failed.")
        sys.exit(1)



if __name__ == "__main__":
    main()