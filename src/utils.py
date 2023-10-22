import os


def create_media_directory():
    """
    Function to create a media directory if it doesn't already exist
    """
    media_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media')
    if not os.path.exists(media_directory):
        os.makedirs(media_directory)
    return media_directory


def create_data_folder():
    """
    Function to create a data folder if it doesn't already exist
    """
    parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    data_folder_path = os.path.join(parent_directory, "data")
    if not os.path.exists(data_folder_path):
        os.makedirs(data_folder_path)
    return data_folder_path


def construct_file_path(data_folder, filename):
    """
    Function to construct a full file path within a data folder
    """
    return os.path.join(data_folder, filename)
