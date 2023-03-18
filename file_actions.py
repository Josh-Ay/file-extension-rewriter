from os import listdir


def get_files_and_sub_folders_in_folder(path_to_folder: str):
    """
    Gets all the files and directories/folders in a given directory/folder.
    Returns a tuple containing the list of files and folders found.
    Example output: ([file_1, file_2], [folder_1, folder_2])
    """
    list_of_items_in_folder = listdir(path_to_folder)
    list_of_files = [item for item in list_of_items_in_folder if
                               len(item.split(".")) > 1 and len(item.split(".")[len(item.split(".")) - 1]) > 1]
    list_of_sub_folders = [item for item in list_of_items_in_folder if item not in list_of_files]

    return list_of_files, list_of_sub_folders


def get_nested_files_in_folders_and_subfolders(parent_folder_path: str, folder_list: list, output_list: list):
    """
    Gets all the files and nested files in a list of folders/directory.
    Returns an array of objects specifying the path to each file as well
    as the list of files found in a single folder/directory.
    """
    for folder in folder_list:
        list_of_files, list_of_folders = get_files_and_sub_folders_in_folder(
            parent_folder_path + "/" + folder)
        output_list.append({"path_prefix": parent_folder_path + "/" + folder, "files": list_of_files})

        if len(list_of_folders) > 0:
            get_nested_files_in_folders_and_subfolders(parent_folder_path + "/" + folder, list_of_folders, output_list)

    return output_list

