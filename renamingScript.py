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


def pretty_print(folder_name, nest_level):
    string = ''
    for i in xrange(0, nest_level):
        string += ' '
    return string + "/" + folder_name


def rename(folder, nest_level):
    if folder.name:
        if folder.name[-11:] == "[Sensitive]":
            if folder.name[-12] == " ":
                new_folder = folder.rename(folder.name[:-12])
            else:
                new_folder = folder.rename(folder.name[:-11])
        else:
            new_folder = folder

        if new_folder.name[0:15] == "(Box Entrusted)":
            if new_folder.name == folder.name:
                print(pretty_print(new_folder.name, nest_level))
                f.write(pretty_print(new_folder.name, nest_level) + "\n")
            else:
                print(pretty_print(folder.name + " => " + new_folder.name, nest_level))
                f.write(pretty_print(folder.name + " => " + new_folder.name, nest_level) + "\n")
        elif (new_folder.name[0:15] == "{Box Entrusted}") or (new_folder.name[0:15] == "[Box Entrusted]"):
            if new_folder.name[15] == " ":  # To make sure there's a space (Probably not needed)
                renamed_folder = new_folder.rename("(Box Entrusted) " + new_folder.name[16:])
                print(pretty_print(folder.name + " => " + renamed_folder.name, nest_level))
                f.write(pretty_print(folder.name + " => " + renamed_folder.name, nest_level) + "\n")
            else:
                renamed_folder = new_folder.rename("(Box Entrusted) " + new_folder.name[15:])
                print(pretty_print(folder.name + " => " + renamed_folder.name, nest_level))
                f.write(pretty_print(folder.name + " => " + renamed_folder.name, nest_level) + "\n")
        else:
            renamed_folder = new_folder.rename("(Box Entrusted) " + new_folder.name)  # rename
            print(pretty_print(folder.name + " => " + renamed_folder.name, nest_level))
            f.write(pretty_print(folder.name + " => " + renamed_folder.name, nest_level) + "\n")


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
