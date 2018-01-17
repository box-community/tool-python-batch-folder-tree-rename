# Import two classes from the boxsdk module - Client and OAuth2
from __future__ import print_function, unicode_literals

from datetime import datetime

import config
from boxsdk import Client, JWTAuth
from boxsdk.exception import BoxAPIException

oauth = JWTAuth(
    client_id=config.client_id,
    client_secret=config.client_secret,
    enterprise_id=config.enterprise_id,
    jwt_key_id=config.jwt_key_id,
    rsa_private_key_file_sys_path=config.rsa_private_key_file_sys_path
)

# Create an authenticated client that can interact with the Box Content API
client = Client(oauth)

user_id = config.user_id
base_folder_id = config.base_folder_id

owner = client.user(user_id=user_id)

oauth.authenticate_app_user(owner)

folder_prefix = config.folder_prefix
folder_prefix_len = len(folder_prefix)
folder_suffix = config.folder_suffix
folder_suffix_len = len(folder_suffix)
folder_prefix2 = folder_prefix.replace("(", "[")  # to test for Brackets instead of paren's
folder_prefix2 = folder_prefix2.replace(")", "]")


def pretty_print(folder_name, nest_level):
    string = ''
    for i in xrange(0, nest_level):
        string += ' '
    return string + "/" + folder_name


def rename(folder, nestLevel):
    if folder.name:
        if folder.name[-folder_suffix_len:] == folder_suffix:
            if folder.name[-folder_suffix_len - 1] == " ":
                newFolder = folder.rename(folder.name[:-folder_suffix_len - 1])
            else:
                newFolder = folder.rename(folder.name[:-folder_suffix_len])
        else:
            newFolder = folder

        if newFolder.name[0:folder_prefix_len] == folder_prefix:  # if the name is already correct
            if newFolder.name[folder_prefix_len] != " ":
                renamedFolder = newFolder.rename(folder_prefix + " " + newFolder.name[folder_prefix_len:])
                print(pretty_print(folder.name + " => " + renamedFolder.name, nestLevel))
                f.write(pretty_print(folder.name + " => " + renamedFolder.name, nestLevel) + "\n")
            else:
                print(pretty_print(newFolder.name, nestLevel))
                f.write(pretty_print(newFolder.name, nestLevel) + "\n")
        elif (newFolder.name[0:folder_prefix_len] == folder_prefix) or (
                folder_prefix2 == newFolder.name[0:folder_prefix_len]):
            if newFolder.name[folder_prefix_len] == " ":  # To make sure there's a space
                renamedFolder = newFolder.rename(folder_prefix + " " + newFolder.name[folder_prefix_len + 1:])
                print(pretty_print(folder.name + " => " + renamedFolder.name, nestLevel))
                f.write(pretty_print(folder.name + " => " + renamedFolder.name, nestLevel) + "\n")
            else:
                renamedFolder = newFolder.rename(folder_prefix + " " + newFolder.name[folder_prefix_len:])
                print(pretty_print(folder.name + " => " + renamedFolder.name, nestLevel))
                f.write(pretty_print(folder.name + " => " + renamedFolder.name, nestLevel) + "\n")
        else:
            renamedFolder = newFolder.rename(folder_prefix + " " + newFolder.name)  # rename
            print(pretty_print(folder.name + " => " + renamedFolder.name, nestLevel))
            f.write(pretty_print(folder.name + " => " + renamedFolder.name, nestLevel) + "\n")


def recurse(folder_id, nest_level):
    contents = client.folder(folder_id=folder_id).get_items(limit=1000, offset=0)
    folders = filter(lambda x: x.type == "folder", contents)
    for folder in folders:
        try:
            rename(folder, nest_level)
            recurse(folder.id, nest_level + 1)  # recursion
        except BoxAPIException as err:
            if err.status == 404:  # the item was not a folder
                pass
            else:
                raise


time = (datetime.now().strftime("_%m-%d-%Y"))
filename = "EntrustedNames" + time + ".txt"
f = open(filename, "w+")
f = open(filename, "a+")

root = client.folder(folder_id=base_folder_id).get()
print(root.name)
recurse(base_folder_id, 0)
f.close()
