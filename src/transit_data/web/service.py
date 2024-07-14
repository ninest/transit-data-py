from abc import ABC, abstractmethod
from typing import Optional

from transit_data.models import FullLine, GTFSFeed, Line, Operator, Stop
from transit_data.gtfs import feeds
from transit_data.utils.file import read_json_file


class ITransitService(ABC):
    @abstractmethod
    def get_feeds(self) -> list[GTFSFeed]:
        raise NotImplementedError

    @abstractmethod
    def get_operators(
        self, location_code: str, feed_id: str | None = None
    ) -> list[GTFSFeed]:
        raise NotImplementedError

    @abstractmethod
    def get_stops(self, operator_id: str) -> list[Stop]:
        raise NotImplementedError


BASE_FILE_PATH = "./out"


class FileTransitService(ITransitService):
    def get_feeds(self) -> list[GTFSFeed]:
        return feeds

    def get_feeds_by_location(self, location_code: str):
        feed_by_location = list(
            filter(lambda f: f.location_code == location_code, feeds)
        )
        return feed_by_location

    def get_operators(
        self, location_code: str, feed_id: str | None = None
    ) -> list[Operator]:
        feed: None | GTFSFeed = None
        for f in feeds:
            if (
                location_code is None
                or f.location_code.lower() == location_code.lower()
            ) or (feed_id is None or f.id.lower() == id.lower()):
                feed = f
        if feed is None:
            return []
        return feed.operators

    def get_operator(self, location_code: str, operator_id: str):
        print(feeds)
        feed = None
        for f in feeds:
            if location_code.lower() == f.location_code.lower():
                feed = f

        if feed is None:
            raise Exception("location code not found")

        for o in feed.operators:
            if o.id.lower() == operator_id.lower():
                return o
        raise Exception("operator id not found")

    def get_stops(self, location_id: str, operator_id: str) -> list[Stop]:
        stops_data = read_json_file(
            f"{BASE_FILE_PATH}/{location_id}/{operator_id}/stops.json"
        )
        stops = [Stop(**data) for data in stops_data]
        return stops

    def get_lines_by_location(self, location_code: str) -> list[Line]:
        feeds = self.get_feeds_by_location(location_code)

        lines: list[Line] = []
        for f in feeds:
            for operator in f.operators:
                lines_data = read_json_file(
                    f"{BASE_FILE_PATH}/{location_code}/{operator.id}/lines.json"
                )
                print(lines_data)
                lines.extend([Line(**data) for data in lines_data])

        return lines

    def get_lines(self, location_code: str, operator_id: str) -> list[Line]:
        lines_data = read_json_file(
            f"{BASE_FILE_PATH}/{location_code}/{operator_id}/lines.json"
        )
        lines = [Line(**data) for data in lines_data]
        return lines

    def get_line(self, location_code: str, operator_id: str, route_id: str) -> FullLine:
        line_data = read_json_file(
            f"{BASE_FILE_PATH}/{location_code}/{operator_id}/lines/{route_id}.json"
        )
        print(line_data["directions"])
        return FullLine(**line_data)


transit_service = FileTransitService()
