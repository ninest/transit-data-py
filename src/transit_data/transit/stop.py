import pandas as pd

from transit_data.models import GTFSFeed, Operator
from transit_data.utils.pandas import notNaN


# def get_stops(location_code: str, feed_id: str, operator_id: str):
def get_stops(feed: GTFSFeed, operator: Operator):
    base_path = f"GTFS_feeds/{feed.location_code}/{feed.id}"

    stops = pd.read_csv(f"{base_path}/stops.txt", dtype={"stop_id": str})

    # Ensure 'parent_station' is in stops DataFrame, if not, create it
    if "parent_station" not in stops.columns:
        stops["parent_station"] = stops["stop_id"]
    else:
        # Fill NaN parent_stations with their own stop_id
        stops["parent_station"] = stops["parent_station"].fillna(stops["stop_id"])

    # Ensure all potential fields are present
    for col in ["stop_address", "stop_url", "zone_id", "vehicle_type"]:
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
                "stop_id": stop["stop_id"],
                "stop_name": stop["stop_name"],
                "stop_url": stop_url,
                "stop_address": notNaN(stop["stop_address"]),
                "parent_station": parent_station,
                "location": location,
                "zone_id": notNaN(stop["zone_id"]),
                "vehicle_type": notNaN(stop["vehicle_type"]),
                "wheelchair_boarding": notNaN(stop["wheelchair_boarding"]),
            }
        )

    return return_stops
