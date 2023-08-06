from typing import List

from requests import get

from greentext.posts import catalog
from greentext.posts.threads import Thread

url = "https://a.4cdn.org/boards.json"
available = []


class Board(object):
    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.board, self.title) == (other.board, other.title)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.board, self.title))

    def __init__(self, response: dict):
        self.board = response.get("board")  # type: str
        self.description = response.get("meta_description")  # type: str
        self.is_archived = bool(response.get("is_archived")) if "is_archived" in response else None  # type: bool
        self.is_work_safe = bool(response.get("ws_board")) if "ws_board" in response else None  # type: bool
        self.max_comment_chars = response.get("max_comment_chars")  # type: int
        self.max_filesize = response.get("max_filesize")  # type: int
        self.max_webm_duration = response.get("max_webm_duration")  # type: int
        self.max_webm_filesize = response.get("max_webm_filesize")  # type: int
        self.pages = response.get("pages")  # type: int
        self.posts_per_page = response.get("per_page")  # type: int
        self.reached_image_limit = bool(response.get(
            "image_limit")) if "image_limit" in response else None  # type: bool
        self.threads = None  # type: List[Thread]
        self.title = response.get("title")  # type: str

    def __repr__(self):
        return "<Board({})>".format(self.title)

    def search(self, term):
        return [thread for thread in self.threads if term in [thread.comment, thread.title]]

    def update(self):
        self.threads = [Thread(self.board, j) for i in [catalog.Page(page).threads for page in get(catalog.url.format(
            board=self.board)).json()] for j in i]


def search(term):
    global available

    return [board for board in available if term in [board.board, board.description, board.title]]


def update():
    global available

    boards = {board.board: board for board in [Board(board) for board in get(url).json()["boards"]]}

    updated = boards != available
    available = boards

    return updated
