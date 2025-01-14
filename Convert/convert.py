import os


def create_folder(folder_dir: str) -> None:
    """
    Creates a folder at the specified directory path if it does not already exist.

    Args:
        folder_dir (str): The directory path where the folder should be created.

    Returns:
        None
    """
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)

def create_file(
        parent_dir: str,
        file_name: str,
        text: str,
        file_type: str = 'md'
) -> None:
    """
    Creates a file with the given name and type at the specified directory path
    with the given text content.

    Args:
        parent_dir (str): The directory path where the file should be created.
        file_name (str): The name of the file that should be created.
        text (str): The content of the file.
        file_type (str): The type of the file. Defaults to 'md'.

    Returns:
        None
    """
    flag = True
    while flag:
        try:
            path = os.path.join(parent_dir, f'{file_name}.{file_type}')
            with open(path, 'w') as f:
                f.write(text)
                f.close()
            flag = False
        except Exception as e:
            print(e)
