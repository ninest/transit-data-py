import pandas as pd


def notNaN(val):
    return None if pd.isna(val) else val


def get_stops(agency: str):
    base_path = f"GTFS_feeds/{agency}"

    stops = pd.read_csv(f"{base_path}/stops.txt", dtype={"stop_id": str})
    # Ensure 'parent_station' is in stops DataFrame, if not, create it
    if "parent_station" not in stops.columns:
        stops["parent_station"] = stops["stop_id"]
    else:
        # Fill NaN parent_stations with their own stop_id
        stops["parent_station"] = stops["parent_station"].fillna(stops["stop_id"])

    # Ensure all potential fields are present
    for col in ["stop_address", "zone_id", "vehicle_type"]:
        if col not in stops.columns:
            stops[col] = None

    stops_info = stops.to_dict("records")

    return_stops = []
    for stop in stops_info:
        stop_url = notNaN(stop["stop_url"])
        parent_station = notNaN(stop["parent_station"])
        if stop_url is None and parent_station is None:
            continue

        location = (
            None
            if pd.isna(stop["stop_lat"])
            else {
                "lat": stop["stop_lat"],
                "lon": stop["stop_lon"],
            }
        )
        return_stops.append(
            {
                "stopId": stop["stop_id"],
                "stopName": stop["stop_name"],
                "location": location,
                "stopUrl": stop_url,
                "parentStation": parent_station,
                "stopAddress": notNaN(stop["stop_address"]),
                "zoneId": notNaN(stop["zone_id"]),
                "vehicleType": notNaN(stop["vehicle_type"]),
                "wheelchairBoarding": notNaN(stop["wheelchair_boarding"]),
            }
        )

    return return_stops
