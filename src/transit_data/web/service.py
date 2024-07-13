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

    def get_stops(self, location_id: str, operator_id: str) -> list[Stop]:
        stops_data = read_json_file(
            f"{BASE_FILE_PATH}/{location_id}/{operator_id}/stops.json"
        )
        stops = [Stop(**data) for data in stops_data]
        return stops

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
        return FullLine(**line_data)


transit_service = FileTransitService()
