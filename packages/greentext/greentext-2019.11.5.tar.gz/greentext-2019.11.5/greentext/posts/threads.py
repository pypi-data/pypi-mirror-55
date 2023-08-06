from datetime import datetime
from typing import List

from requests import get

from greentext.posts import Post
from greentext.users import User

url = "https://a.4cdn.org/{board}/thread/{number}.json"


class Thread(Post):
    def __init__(self, board, thread):
        super().__init__(board, thread)
        self.hit_bump_limit = thread.get("bumplimit")  # type: bool
        self.hit_image_limit = thread.get("imagelimit")  # type: bool
        self.image_count = thread.get("images")  # type: int
        self.last_modified = datetime.fromtimestamp(thread.get("last_modified")) if thread.get(
            "last_modified") is not None else None  # type: datetime
        self.omitted_reply_count = thread.get("omitted_posts")  # type: int
        self.omitted_image_count = thread.get("omitted_images")  # type: int
        self.op = User(thread)  # type: User
        self.posts = None  # type: List[Post]
        self.reply_count = thread.get("replies")  # type: int
        self.semantic_url = thread.get("semantic_url")  # type: str
        self.tag = thread.get("tag")  # type: str

    def __repr__(self):
        return "<Thread(number={})>".format(self.number)

    def download_all_media(self, directory):
        self.media.download()
        self.media.write(directory)
        for media in [post.media for post in self.posts]:
            if media is not None:
                media.download()
                media.write(directory)

    def search(self, term):
        return [post for post in self.posts if term in any([post.comment, post.title])]

    def update(self):
        self.posts = [Post(self.board, post) for post in
                      get(url.format(board=self.board, number=self.number)).json()["posts"]][1:]
