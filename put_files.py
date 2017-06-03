#!/usr/bin/env python3

"""
Upload a list of files to Google Drive using PyDrive.
User authentication is required.
"""

from auth import authenticate
from list_files import list_files


def parse_args(description):
    "Parse command-line arguments"

    import argparse

    # Process command-line arguments
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-p', '--parent',
                        help='ID of the Google Drive folder to containt file',
                        default="0ByTwsK5_Tl_PemN0QVlYem11Y00")

    parser.add_argument('-s', '--silent',
                        help='silent or quiet mode. ',
                        default=False,
                        action='store_true')

    parser.add_argument('files', metavar='FILE',
                        nargs='+',
                        help='local file name to upload')

    args = parser.parse_args()

    return args


def upload_files(drive, folder_id, files, silent):
    "Print file information into a file"
    import sys

    ls = list_files(drive, folder_id)

    for fname in files:
        if fname in ls:
            if not silent:
                sys.stdout.write('Replacing file ' + fname + ' ... ')
            f = drive.CreateFile({'id': ls[fname][0]})
        else:
            f = drive.CreateFile({"parents":
                                 [{"kind": "drive#fileLink",
                                  "id": folder_id}]})
            if not silent:
                sys.stdout.write('Uploading file ' + fname + ' ... ')

        f.SetContentFile(fname)
        f.Upload()

        if not silent:
            sys.stdout.write('Done\n')


if __name__ == "__main__":
    import os
    from pydrive.drive import GoogleDrive

    args = parse_args(description=__doc__)
    src_dir = os.path.dirname(os.path.realpath(__file__))

    gauth = authenticate(src_dir, "w")
    drive = GoogleDrive(gauth)

    upload_files(drive, args.parent, args.files, args.silent)
