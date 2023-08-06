from greentext.media import Dimensions


class Thumbnail(object):
    def __init__(self, post: dict):
        self.dimensions = Dimensions(post.get("tn_w"), post.get("tn_h"))  # type: Dimensions
        self.storage_name = "{}{}".format(post.get("tim"), post.get("ext"))  # type: str
