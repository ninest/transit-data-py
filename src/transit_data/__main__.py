from .line import get_full_line
from .utils.file import write_dict_to_file

lines = [
    ["line-Blue", "Blue"],
    ["line-Orange", "Orange"],
    ["line-Red", "Red"],
    ["line-Green", "Green-B"],
    ["line-Green", "Green-C"],
    ["line-Green", "Green-D"],
    ["line-Green", "Green-E"],
    ["line-Mattapan", "Mattapan"],
]
agency = "MBTA"

for route, line in lines:
    data = get_full_line(agency, route, line)
    write_dict_to_file(data, f"./out/{agency}/lines/{line}.json")
