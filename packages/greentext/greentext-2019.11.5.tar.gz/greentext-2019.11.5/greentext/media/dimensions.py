class Dimensions(object):
    def __init__(self, width: int, height: int):
        self.height = height  # type: int
        self.width = width  # type: int

    def __repr__(self):
        return "<Dimensions(height={}, width={})>".format(self.height, self.width)

    def serialize(self):
        return {"height": self.height,
                "width": self.width}
