from typing import Optional

from .models import GTFSFeed, Operator
from .utils.file import download_zip

feeds = [
    # USA
    GTFSFeed(
        id="mbta",
        location_code="us-ma",
        url="https://cdn.mbta.com/MBTA_GTFS.zip",
        name="Massachusets Bay Transit Authority",
        operators=[
            Operator(
                id="MBTA",
                name="MBTA",
                full_name="Massachusets Bay Transit Authority",
                short_name="MBTA",
            ),
            # Operator(id="CCRTA", name="Cape Cod Regional Transit Authority"),
        ],
    ),
    GTFSFeed(
        id="cta",
        location_code="us-il",
        url="http://www.transitchicago.com/downloads/sch_data/google_transit.zip",
        name="Chicago Transit Authority",
        operators=[
            Operator(
                id="CTA",
                name="Chicago Transit Authority",
                full_name="Chicago Transit Authority",
                short_name="CTA",
            ),
        ],
    ),
    # USA
    # GTFSFeed(
    #     location_code="US-MA",
    #     folder_name="MBTA",
    #     agency_name="MBTA",
    #     id="MBTA",
    # ),
    # GTFSFeed(
    #     location_code="US-IL",
    #     folder_name="CTA",
    #     agency_name="Chicago Transit Authority",
    #     id="CTA",
    # ),
    # # Singapore
    # GTFSFeed(location_code="SG", folder_name="SG", agency_name="SMRT", id="SMRT"),
    # GTFSFeed(location_code="SG", folder_name="SG", agency_name="SBST", id="SBS"),
    # GTFSFeed(location_code="SG", folder_name="SG", agency_name="LTA", id="LTA"),
    # GTFSFeed(location_code="SG", folder_name="SG", agency_name="TTS", id="TTS"),
    # GTFSFeed(location_code="SG", folder_name="SG", agency_name="GAS", id="GAS"),
]


def get_feed(location_code: str, id: Optional[str] = None):
    for feed in feeds:
        if (
            location_code is None or feed.location_code.lower() == location_code.lower()
        ) or (id is None or feed.id.lower() == id.lower()):
            return feed
    return None


def download_gtfs(location_code: str, id: str):
    feed = get_feed(location_code, id)
    if feed is None:
        print(f"Could not find feed {location_code}:{id}")
        return

    download_zip(feed.url, f"./GTFS_feeds/{feed.location_code}/{feed.id}")
