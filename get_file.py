#!/usr/bin/env python3

"""
Download a public file from Google Drive.
"""

import requests
import sys


def parse_args(description):
    "Parse command-line arguments"

    import argparse

    # Process command-line arguments
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-p', '--parent',
                        help='ID of parent folder on Google Drive',
                        default="0ByTwsK5_Tl_PemN0QVlYem11Y00")

    parser.add_argument('-i', '--id',
                        help='file ID on Google Drive',
                        default="")

    parser.add_argument('-o', '--outfile',
                        help='output file name; if missing, write to stdout',
                        default="")

    parser.add_argument('-O', '--remote-name',
                        help='use remote file name for local file name',
                        action="store_true",
                        default=False)

    parser.add_argument('-s', '--silent',
                        default=False,
                        action='store_true',
                        help='silent or quiet mode. ')

    parser.add_argument('file',
                        help='file name to be downloaded',
                        default="")

    args = parser.parse_args()

    return args


def download_file(id, outfile, filesize):
    "Download file with given ID from Google Drive"
    URL = "https://drive.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    write_response_content(response, outfile, filesize)


def get_confirm_token(response):
    "Obtain confirmation token from response"

    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def write_response_content(response, outfile, filesize):
    """ Write the content into outfile of stdout """

    CHUNK_SIZE = 32768
    bar = None

    if filesize:
        try:
            import progressbar
            bar = progressbar.ProgressBar(maxval=filesize)
            bar.start()
            count = 0
        except:
            pass

    if outfile:
        f = open(outfile, "wb")
    else:
        f = sys.stdout.buffer

    for chunk in response.iter_content(CHUNK_SIZE):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)

            if bar is not None:
                count += len(chunk)
                bar.update(count)

    if bar:
        bar.finish()

    if outfile:
        f.close()


if __name__ == "__main__":
    import os
    from pydrive.drive import GoogleDrive
    from auth import authenticate
    from list_files import list_files

    # Process command-line arguments
    args = parse_args(description=__doc__)

    # Athenticate
    src_dir = os.path.dirname(os.path.realpath(__file__))
    gauth = authenticate(src_dir, "r")

    # Create drive object
    drive = GoogleDrive(gauth)

    # Obtain file name and size
    if args.id:
        file_id = args.id
        f = drive.CreateFile({'id': args.id})
        size = int(f['fileSize'])
        filename = f['title']
    elif args.file:
        ls = list_files(drive, args.parent)
        try:
            file_id, size = ls[args.file]
        except:
            print('File', args.file, 'does not exist.')
            sys.exit(-1)
        filename = args.file

    if args.remote_name:
        outfile = filename
    else:
        outfile = args.outfile

    # Disable progressbar in silient mode
    if args.silent:
        size = 0

    download_file(file_id, outfile, size)
