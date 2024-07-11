import pandas as pd


def get_full_line(agency: str, route_id: str):
    base_path = f"GTFS_feeds/{agency}"

    routes = pd.read_csv(f"{base_path}/routes.txt", dtype={"route_id": str})
    trips = pd.read_csv(
        f"{base_path}/trips.txt", dtype={"route_id": str, "trip_id": str}
    )
    stop_times = pd.read_csv(
        f"{base_path}/stop_times.txt", dtype={"trip_id": str, "stop_id": str}
    )

    stops = pd.read_csv(f"{base_path}/stops.txt", dtype={"stop_id": str})
    if "parent_station" not in stops.columns:
        stops["parent_station"] = stops["stop_id"]
    else:
        # Fill NaN parent_stations with their own stop_id
        stops["parent_station"] = stops["parent_station"].fillna(stops["stop_id"])

    # Check if the route exists in routes.txt
    line_routes = routes[routes["route_id"] == route_id]
    if line_routes.empty:
        print(f"No route found for route_id: {route_id}")
        print(f"Available routes: {routes['route_id'].unique()}")
        return {}

    line_trips = trips[trips["route_id"].isin(line_routes["route_id"])]
    if line_trips.empty:
        print(f"No trips found for route_id: {route_id}")
        print(f"Available route_ids in trips: {trips['route_id'].unique()}")
        return {}

    # Get stop times for line trips
    line_stop_times = stop_times[stop_times["trip_id"].isin(line_trips["trip_id"])]
    if line_stop_times.empty:
        print(f"No stop_times found for route_id: {route_id}")
        print(f"Available trip_ids in stop_times: {stop_times['trip_id'].unique()}")
        return {}

    # Merge with stops to get stop names
    line_stops = pd.merge(line_stop_times, stops, on="stop_id")
    # Sort by trip, stop seq
    line_stops = line_stops.sort_values(["trip_id", "stop_sequence"])

    # Unique directions (inferred from trips)
    # directions_info = line_trips[["direction_id", "trip_headsign"]].drop_duplicates()
    if "trip_headsign" in line_trips.columns:
        directions_info = (
            line_trips.groupby("direction_id")
            .agg({"trip_headsign": "first"})
            .reset_index()
        )
    else:
        directions_info = (
            line_trips.groupby("direction_id").agg({"trip_id": "first"}).reset_index()
        )
        directions_info["trip_headsign"] = directions_info["trip_id"]

    if directions_info.empty:
        print(f"No directions found for route_id: {route_id}")
        return {}

    stations_by_direction = {}

    for _, direction_info in directions_info.iterrows():
        direction_id = direction_info["direction_id"]
        direction_name = direction_info["trip_headsign"]
        destination = direction_name  # Using trip headsign as the destination

        direction_trips = line_trips[line_trips["direction_id"] == direction_id]
        if direction_trips.empty:
            print(f"No trips found for direction_id: {direction_id}")
            continue

        # Collect all unique stops for this direction, regardless of shape
        direction_stops = line_stops[
            line_stops["trip_id"].isin(direction_trips["trip_id"])
        ]
        if direction_stops.empty:
            print(f"No stops found for direction_id: {direction_id}")
            continue

        # Sort and drop duplicates to get unique stops
        unique_direction_stops = direction_stops.drop_duplicates(
            subset=["stop_id"]
        ).sort_values("stop_sequence")

        stops_info = unique_direction_stops[
            [
                "stop_id",
                "parent_station",
            ]
        ].to_dict("records")

        # Create adjacency list (graph) for the stops
        adjacency_list = {}
        for trip_id, trip_group in direction_stops.groupby("trip_id"):
            trip_group = trip_group.sort_values("stop_sequence")
            for i in range(len(trip_group) - 1):
                from_stop = trip_group.iloc[i]["parent_station"]
                to_stop = trip_group.iloc[i + 1]["parent_station"]
                if from_stop not in adjacency_list:
                    adjacency_list[from_stop] = []
                if to_stop not in adjacency_list[from_stop]:
                    adjacency_list[from_stop].append(to_stop)

        stations_by_direction[direction_id] = {
            "direction_id": direction_id,
            "direction_name": direction_name,
            "destination": destination,
            "stops": stops_info,
            "order": adjacency_list,
        }

    route = line_routes.iloc[0]
    return_line = {
        "line_id": route_id,  # although this is route information, use line
        "line_color": route.get("route_color", ""),
        "line_text_color": route.get("route_text_color", ""),
        "line_long_name": route["route_long_name"],
        "directions": stations_by_direction,
    }

    return return_line
