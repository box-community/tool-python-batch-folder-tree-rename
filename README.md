# folder-tree-rename

## Install
```
pip install -r requirements.txt
```

## Description
Folder-tree-rename renames folders with `folder_prefix` if it's not already there. It also removes `folder_suffix` at the end of the folder if it exists.

## Configuration (JWT Authentication)
Folder-tree-rename uses JWT to authenticate to Box. For a primer on JWT, check out <a href="https://github.com/box-community/jwt-app-primer">this link</a>. Use the `user_id` variable in `config.py` to specify the user whose files are to be renamed. Use the `base_folder_id` variable in `config.py` to specify the folder tree you want to change. For example if all of the files are in a folder called "entrusted", you would find the id of the folder in the url of the page used to access the folder, and use that value as the `base_folder_id`. If you want to run on all folders in the account, use the value '0'.


## Use Case
Below is an example folder

![Before.PNG](img/Before.PNG)

The config. Notice the `base_folder_id` came from the url above

![Configuration1.PNG](img/Config.PNG)

Every folder now has the new prefix and none have the old suffix

![After.PNG](img/After.PNG)

Also notice every subfolder is also changed!

![After2.PNG](img/After2.PNG)