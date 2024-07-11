from .transit.line import get_full_line
from .transit.stop import get_stops
from .transit.map_line import get_map_line_coords, visualize_map_line
from .gtfs import feeds, download_gtfs
from .utils.file import write_dict_to_file

for feed in feeds:
    download_gtfs(feed.location_code, feed.id)

# MBTA = "MBTA"
# LIRR = "LI"
# SG = "SG"
# CTA = "CTA"

# agencies = [CTA]

# for agency in agencies:
#     stops = get_stops(agency)
#     write_dict_to_file(stops, f"./out/{agency}/stops.json")

# lines = [
#     # [MBTA, "Blue"],
#     # [MBTA, "Orange"],
#     # [MBTA, "Red"],
#     # [MBTA, "Green-B"],
#     # [MBTA, "Green-C"],
#     # [MBTA, "Green-D"],
#     # [MBTA, "Green-E"],
#     # [MBTA, "Mattapan"],
#     # [MBTA, "CR-Worcester"],
#     # [LIRR, "1"],
#     # [LIRR, "2"],
#     # [LIRR, "3"],
#     # [LIRR, "4"],
#     # [LIRR, "5"],
#     # [LIRR, "6"],
#     # [LIRR, "7"],
#     # [LIRR, "8"],
#     # [LIRR, "9"],
#     # [LIRR, "10"],
#     [LIRR, "11"],
#     [LIRR, "12"],
#     # [SG, "EW"],
#     # [SG, "CG"],
#     # [SG, "NS"],
#     # [SG, "CC"],
#     # [CTA, "Blue"],
#     # [CTA, "Red"],
#     # [CTA, "P"],
#     # [CTA, "Y"],
# ]


# for agency, line in lines:
#     data = get_full_line(agency, line)
#     write_dict_to_file(data, f"./out/{agency}/lines/{line}.json")

# for agency, line in lines:
#     lines = get_map_line_coords(agency, line)
#     if len(lines) > 0:
#         write_dict_to_file(lines, f"./out/{agency}/map_lines/{line}.json")
#         map_obj = visualize_map_line(lines)
#         map_obj.save(f"./out/{agency}/map_lines/{line}.html")
#     else:
#         print(f"Unable to visualize {line}")
