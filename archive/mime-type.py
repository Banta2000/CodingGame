import sys
import os
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "True"


# Get Game Start Parameters
def get_start_parameters():
    if HOME_PC:
        FILETYPES = [
            "png image/png",
            "TIFF image/TIFF",
            "css text/css",
            "TXT text/plain",
        ]
        FILES = [
            "example.TXT",
            "referecnce.txt",
            "strangename.tiff",
            "resolv.CSS",
            "matrix.TiFF",
            "lanDsCape.Png",
            "extract.cSs",
        ]

        FILETYPES = [
            "wav audio/x-wav",
            "mp3 audio/mpeg",
            "pdf application/pdf",
        ]

        FILES = [
            "a",
            "a.wav",
            "b.wav.tmp",
            "test.vmp3",
            "pdf",
            ".pdf",
            "mp3",
            "report..pdf",
            "defaultwav",
            ".mp3.",
            "final.",
        ]

    else:
        n = int(input())  # Number of elements which make up the association table.
        q = int(input())  # Number Q of file names to be analyzed.
        FILETYPES = [input() for _ in range(n)]
        FILES = [input() for _ in range(q)]

    FILETYPES2 = {}

    for line in FILETYPES:
        (extension, friendlyname) = line.split(" ")
        FILETYPES2[extension.lower()] = friendlyname
    return FILETYPES2, FILES


# ********************************************************

FILETYPES2, FILES = get_start_parameters()
for filename in FILES:
    extension = filename.split(".")
    if len(extension) == 1:
        print("UNKNOWN")
        continue
    extension = extension[-1].lower()
    if extension in FILETYPES2:
        print(FILETYPES2[extension])
    else:
        print("UNKNOWN")
