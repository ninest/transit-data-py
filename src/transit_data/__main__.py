from .line import get_full_line
from .stop import get_stops
from .utils.file import write_dict_to_file

MBTA = "MBTA"
LIRR = "LI"

agencies = [MBTA, LIRR]

for agency in agencies:
    stops = get_stops(agency)
    write_dict_to_file(stops, f"./out/{agency}/stops.json")

lines = [
    # [MBTA, "Blue"],
    # [MBTA, "Orange"],
    # [MBTA, "Red"],
    # [MBTA, "Green-B"],
    # [MBTA, "Green-C"],
    # [MBTA, "Green-D"],
    # [MBTA, "Green-E"],
    # [MBTA, "Mattapan"],
    # [LIRR, "1"]
]


# for agency, line in lines:
#     data = get_full_line(agency, line)
#     write_dict_to_file(data, f"./out/{agency}/lines/{line}.json")
