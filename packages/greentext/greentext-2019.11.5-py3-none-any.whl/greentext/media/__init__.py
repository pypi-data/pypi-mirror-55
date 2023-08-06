from json import dumps
from shutil import copyfileobj
from typing import IO

from requests import get

from greentext.media.dimensions import Dimensions
from greentext.media.exceptions import MediaDeletedError
from greentext.media.thumbnails import Thumbnail


class Media(object):
    url = "https://i.4cdn.org/{board}/{storage_name}"  # type: str

    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

    def __init__(self, post, response: dict):
        self.dimensions = Dimensions(response.get("w"), response.get("h"))  # type: Dimensions
        self.file_name = "{}{}".format(response.get("filename"), response.get("ext"))  # type: str
        self.file_size = response.get("fsize")  # type: int
        self.is_deleted = response.get("filedeleted")  # type: bool
        self.md5 = response.get("md5")  # type: str
        self.post = post
        self.storage_name = "{}{}".format(response.get("tim"), response.get("ext"))  # type: str
        self.stream = None  # type: IO
        self.thumbnail = Thumbnail(response)  # type: Thumbnail

    def __repr__(self):
        return "<Media(file_name={}, storage_name={})>".format(self.file_name, self.storage_name)

    def download(self):
        if not self.is_deleted:
            self.stream = get(self.url.format(board=self.post.board, storage_name=self.storage_name), stream=True).raw
        else:
            raise MediaDeletedError(self.file_name)

    def serialize(self):
        return {"dimensions": self.dimensions.serialize(),
                "file_name": self.file_name,
                "md5": self.md5,
                "post": self.post.serialize(),
                "storage_name": self.storage_name}

    def write(self, directory: str):
        with open("{}/{}".format(directory, self.file_name), "wb") as media:
            copyfileobj(self.stream, media)
        with open("{}/{}.meta".format(directory, self.file_name), "w") as meta:
            meta.write(dumps(self.serialize()))
