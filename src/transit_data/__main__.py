import concurrent.futures
import os

from transit_data.models import GTFSFeed, Operator
from .transit.line import get_full_line, get_lines, get_route_ids
from .transit.stop import get_stops
from .transit.map_line import get_map_line_coords, visualize_map_line
from .gtfs import feeds, download_gtfs
from .utils.file import write_to_file

# for feed in feeds:
#     download_gtfs(feed.location_code, feed.id)

# for feed in feeds:
#     for operator in feed.operators:
#         base_save_path = f"./out/{feed.location_code}/{operator.id}"

#         stops = get_stops(feed.location_code, operator.id)
#         write_to_file(stops, f"{base_save_path}/stops.json")

#         route_ids = get_route_ids(feed.location_code, operator.id)

#         for route_id in route_ids:
#             print(f"Starting {feed.id}/{operator.id}/{route_id}")

#             line = get_full_line(feed.location_code, operator.id, route_id)
#             write_to_file(line, f"{base_save_path}/lines/{route_id}.json")

#             map_line = get_map_line_coords(feed.location_code, operator.id, route_id)
#             if len(map_line) > 0:
#                 write_to_file(map_line, f"{base_save_path}/map_lines/{route_id}.json")
#             else:
#                 print(f"Unable to visualize {line}")

#             print(f"Completing {feed.id}/{operator.id}/{route_id}")


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(process_feed, feeds)


def process_feed(feed: GTFSFeed):
    print(f"Starting {feed.id}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(lambda operator: process_operator(feed, operator), feed.operators)

    print(f"Completed {feed.id}")


def process_operator(feed: GTFSFeed, operator: Operator):
    print(f"Starting {feed.id}/{operator.id}")

    base_save_path = f"./out/{feed.location_code}/{operator.id}"

    stops = get_stops(feed.location_code, operator.id)
    write_to_file(stops, f"{base_save_path}/stops.json")

    lines = get_lines(feed.location_code, operator.id)
    write_to_file(lines, f"{base_save_path}/lines.json")

    route_ids = get_route_ids(feed.location_code, operator.id)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(process_route, feed, operator, route_id, base_save_path)
            for route_id in route_ids
        ]
        concurrent.futures.wait(futures)

    print(f"Completed {feed.id}/{operator.id}")


def process_route(
    feed: GTFSFeed, operator: Operator, route_id: str, base_save_path: str
):
    print(f"Starting {feed.id}/{operator.id}/{route_id}")
    line = get_full_line(feed.location_code, operator.id, route_id)
    write_to_file(line, f"{base_save_path}/lines/{route_id}.json")

    map_line = get_map_line_coords(feed.location_code, operator.id, route_id)
    if len(map_line) > 0:
        write_to_file(map_line, f"{base_save_path}/map_lines/{route_id}.json")
    else:
        print(f"Unable to visualize {line}")

    print(f"Completing {feed.id}/{operator.id}/{route_id}")


main()
