#!/usr/bin/env python

"""
List file names, their IDs and sizes in the test suite using mydrive
"""


def parse_args(description):
    "Parse command-line arguments"

    import argparse

    # Process command-line arguments
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('id',
                        nargs='?',
                        help='ID of the Google Drive folder to be listed',
                        default="0ByTwsK5_Tl_PemN0QVlYem11Y00")

    args = parser.parse_args()

    return args


def authenticate():
    "Authenticate using web browser and cache the credential"
    from pydrive.auth import GoogleAuth

    # Authenticate Google account
    gauth = GoogleAuth()

    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    return gauth


def list_files(gauth, folder_id, filename):
    "Print file information into a file"

    from pydrive.drive import GoogleDrive

    drive = GoogleDrive(gauth)

    # Obtain the list of files
    file_list = drive.ListFile({'q': "'" + folder_id + "' in parents " +
                                "and trashed=false"}).GetList()

    # List files in sorted order
    ls = {}
    for file1 in file_list:
        ls[file1['title']] = file1['id'], file1['fileSize']

    with open(filename, "w") as f:
        for key, value in sorted(ls.iteritems()):
            f.write('title: ' + key + ', ' +
                    'id: ' + value[0] + ', ' +
                    'size: ' + value[1] + ';\n')


if __name__ == "__main__":
    folder_id = parse_args(description=__doc__).id

    gauth = authenticate()

    # Create drive object
    list_files(gauth, folder_id, "fileinfo")
