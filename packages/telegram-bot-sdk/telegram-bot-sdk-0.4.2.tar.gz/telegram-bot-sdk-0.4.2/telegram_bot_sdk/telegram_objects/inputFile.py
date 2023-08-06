import os


class InputFile:
    """This class represents the content of a file to be uploaded"""
    def __init__(self, file_path):
        self.file_data = open(file_path, "rb").read()
        self.file_name = os.path.basename(file_path)
        self.mime_type = "audio/mpeg"
