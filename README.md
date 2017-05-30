# Matrix Test Suite
This module allows downloading and uploading files from Google Drive. In Google Drive, each folder or file has a unique ID such as `0ByTwsK5_Tl_PemN0QVlYem11Y00`. The scripts in this module operate on a folder ID and then the file name within the folder.

### List Files
You can list the file using the following command:
```
list_files.py [folder_id]
```
It will list the IDs and sizes of the files in the folder. If `folder_id` is missing, the default folder is `0ByTwsK5_Tl_PemN0QVlYem11Y00`.

### Download File
You can download a file using the following command:
```
get_file.py -O -p <parent_id> <filename>
```
It downloads a file in the parent folder and saves it using the given name. If `-p <parent_id>` is missing, the default parent folder is `0ByTwsK5_Tl_PemN0QVlYem11Y00`. If `-O` is missing, the file is written to `stdout`.

This script will show the progress while downloading. To disable it, use the '-s' option.

### Upload File
You can upload a list of files onto Google Drive using the following command:
```
put_files.py -p <parent_id> <filename1> ...
```
When you use this command for the first time, it will launch your webbrowser for authentication to access the directory. If `-p <parent_id>` is missing, the default parent folder is `0ByTwsK5_Tl_PemN0QVlYem11Y00`.

Note: If the files already exist in the parent folder, the file will be overwritten.
