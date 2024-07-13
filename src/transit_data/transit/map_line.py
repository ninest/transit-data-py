import pandas as pd
import folium


def calculate_center(coords_list):
    latitudes = []
    longitudes = []
    for coords in coords_list:
        for lat, lon in coords:
            latitudes.append(lat)
            longitudes.append(lon)
    return [sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)]


def get_map_line_coords(location_code: str, agency: str, route_id: str):
    base_path = f"GTFS_feeds/{location_code}/{agency}"

    # Load the required GTFS files
    routes = pd.read_csv(f"{base_path}/routes.txt", dtype={"route_id": str})
    trips = pd.read_csv(
        f"{base_path}/trips.txt", dtype={"route_id": str, "shape_id": str}
    )
    shapes = pd.read_csv(f"{base_path}/shapes.txt", dtype={"shape_id": str})

    # Filter trips based on the route_id
    line_trips = trips[trips["route_id"] == route_id]

    # Get unique shape IDs for the route
    shape_ids = line_trips["shape_id"].unique()

    # Create a dictionary to hold the coordinates for each shape_id
    shape_coords = {}
    for shape_id in shape_ids:
        shape = shapes[shapes["shape_id"] == shape_id]
        shape = shape.sort_values(by="shape_pt_sequence")
        coords = shape[["shape_pt_lat", "shape_pt_lon"]].values.tolist()
        shape_coords[shape_id] = coords

    # Remove overlaps and create a list of lists of coordinates
    all_coords = []
    for coords in shape_coords.values():
        if not all_coords:
            all_coords.append(coords)
        else:
            for existing_coords in all_coords:
                if existing_coords[-1] == coords[0]:
                    existing_coords.extend(coords[1:])
                    break
            else:
                all_coords.append(coords)

    return all_coords


def visualize_map_line(coords_list, map_zoom_start=12):
    map_center = calculate_center(coords_list)

    # Create a folium map centered around the calculated coordinates
    map_obj = folium.Map(location=map_center, zoom_start=map_zoom_start)

    # Add each branch of the line to the map
    for coords in coords_list:
        folium.PolyLine(coords, color="blue", weight=2.5, opacity=1).add_to(map_obj)

    return map_obj
