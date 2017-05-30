#!/usr/bin/env python3

"""
List file names, their IDs and sizes in the test suite using mydrive
"""


def list_files(drive, folder_id):
    "Obtain list of files and put into dictionary"

    # Obtain the list of files
    file_list = drive.ListFile({'q': "'" + folder_id + "' in parents " +
                                "and trashed=false"}).GetList()

    # List files in sorted order
    ls = {}
    for file1 in file_list:
        ls[file1['title']] = file1['id'], int(file1['fileSize'])

    return ls


if __name__ == "__main__":
    import os
    from pydrive.drive import GoogleDrive
    from auth import authenticate
    import argparse

    # Process command-line arguments
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('id',
                        nargs='?',
                        help='ID of the Google Drive folder to be listed',
                        default="0ByTwsK5_Tl_PemN0QVlYem11Y00")

    args = parser.parse_args()
    folder_id = args.id

    # Athenticate
    src_dir = os.path.dirname(os.path.realpath(__file__))
    gauth = authenticate(src_dir, "r")

    # Create drive object
    drive = GoogleDrive(gauth)
    ls = list_files(drive, folder_id)

    for key, value in sorted(ls.items()):
        print(key + ', ' +
              'id: ' + value[0] + ', ' +
              'size: ' + str(value[1]) + ';')
