from datetime import datetime

from greentext.users.countries import Country


class User(object):
    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return () == ()
        else:
            return NotImplemented

    def __hash__(self):
        return hash(())

    def __init__(self, response):
        self.cap_code = response.get("capcode")  # type: str
        self.country = Country(response) if response.get("country") is not None else None  # type: Country
        self.id = response.get("id")  # type: str
        self.name = response.get("name")  # type: str
        self.pass_year = datetime.fromtimestamp(response.get("since4pass")) if response.get(
            "since4pass") is not None else None  # type: datetime
        self.trip_code = response.get("trip")  # type: str

    def serialize(self):
        return {"cap_code": self.cap_code,
                "country": self.country.serialize() if self.country is not None else None,
                "id": self.id,
                "name": self.name,
                "pass_year": self.pass_year,
                "trip_code": self.trip_code}
