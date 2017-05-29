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

    parser.add_argument('-i', '--id',
                        help='file ID on Google Drive',
                        default="")

    parser.add_argument('-l', '--length',
                        type=int,
                        help='size of the file in bytes',
                        default=0)

    parser.add_argument('-s', '--silent',
                        help='silent or quiet mode. ',
                        default=False,
                        action='store_true')

    parser.add_argument('file',
                        help='output file name',
                        default="")

    args = parser.parse_args()

    return args


def download_file_from_google_drive(id, outfile, filesize):
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
    bar.finish()

    if outfile:
        f.close()


def get_file_info(filename):
    'Obtain file ID and size from fileinfo'

    with open('fileinfo') as f:
        for s in f:
            if s.find('title: ' + filename) == 0:
                file_id = s[s.find('id: 0ByTwsK5_Tl_')+4:s.find(', size: ')]
                size = int(s[s.find('size: ')+6:-2])
                return file_id, size

    print('Error: could not find filename ' + filename)
    sys.exit(-1)


if __name__ == "__main__":
    args = parse_args(description=__doc__)

    file_id, outfile, size = args.id, args.file, args.length

    if not file_id:
        file_id, size = get_file_info(outfile)

    # Disable progressbar in silent mode
    if args.silent:
        size = 0

    download_file_from_google_drive(file_id, outfile, size)
