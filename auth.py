#!/usr/bin/env python3

"""
Authenticate for Google Drive access.
"""

import sys


def authenticate(src_dir, mode):
    """"
    Authenticate using web browser and cache the credential.
    If mode contains "w", then authenticate for read/write mode.
    """
    from pydrive.auth import GoogleAuth

    # Authenticate Google account
    gauth = GoogleAuth()
    gauth.settings['client_config_file'] = src_dir + '/' + \
        'client_secrets.json'

    if mode.find("w") < 0:
        credfile = 'mycred_readonly.txt'
    else:
        credfile = 'mycred_rw.txt'

    try:
        # Try to load saved client credentials
        gauth.LoadCredentialsFile(src_dir + "/" + credfile)
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
    except KeyboardInterrupt:
        sys.exit(-1)
    except:
        gauth.LocalWebserverAuth()
    finally:
        # Save the current credentials to a file
        gauth.SaveCredentialsFile(src_dir + "/" + credfile)

    return gauth
