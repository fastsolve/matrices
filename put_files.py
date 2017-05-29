#!/usr/bin/env python3

"""
Upload a list of files to Google Drive using PyDrive.
User authentication is required.
"""


def parse_args(description):
    "Parse command-line arguments"

    import argparse

    # Process command-line arguments
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-p', '--parent',
                        help='ID of the Google Drive folder to containt file',
                        default="0ByTwsK5_Tl_PemN0QVlYem11Y00")

    parser.add_argument('files', metavar='FILE',
                        nargs='+',
                        help='local file name to upload')

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


def upload_files(gauth, folder_id, files):
    "Print file information into a file"

    from pydrive.drive import GoogleDrive
    drive = GoogleDrive(gauth)

    for fname in files:
        f = drive.CreateFile({"parents":
                             [{"kind": "drive#fileLink", "id": folder_id}]})
        f.SetContentFile(fname)
        f.Upload()


if __name__ == "__main__":

    args = parse_args(description=__doc__)
    gauth = authenticate()

    upload_files(gauth, args.parent, args.files)
