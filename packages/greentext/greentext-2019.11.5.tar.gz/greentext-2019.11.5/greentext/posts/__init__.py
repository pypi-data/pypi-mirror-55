from datetime import datetime

from greentext.media import Media
from greentext.users import User


class Post(object):
    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return () == ()
        else:
            return NotImplemented

    def __hash__(self):
        return hash(())

    def __init__(self, board, response):
        self.archive_time = datetime.fromtimestamp(response.get("archived_on")) if response.get(
            "archived_on") is not None else None  # type: datetime
        self.board = board  # type: str
        self.comment = response.get("com")  # type: str
        self.has_spoiler = response.get("spoiler")  # type: bool
        self.is_archived = response.get("archived")  # type: bool
        self.is_stickied = response.get("sticky")  # type: bool
        self.media = Media(self, response) if response.get("filename") is not None else None  # type: Media
        self.number = response.get("no")  # type: int
        self.reply_to = response.get("resto")  # type: int
        self.time = datetime.fromtimestamp(
            response.get("time")) if response.get("time") is not None else None  # type: datetime
        self.title = response.get("sub")  # type: str
        self.user = User(response)  # type: User

    def __repr__(self):
        return "<Post(number={})>".format(self.number)

    def serialize(self):
        return {"board": self.board,
                "comment": self.comment,
                "number": self.number,
                "time": self.time.second,
                "title": self.title,
                "user": self.user.serialize()}
