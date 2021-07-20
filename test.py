from core.main import create_map


def take_screenshot(lat: float, long: float, row: int, col: int, number: int, file_name: str, gmaps: bool,
                    gmaps_satellite: bool, zoom: int, osm: True):
    """

    Args:
        col: Column count
        file_name: File name of the images
        gmaps: Google Maps View
        gmaps_satellite: Google Maps Satellite
        lat: Latitude of the left corner
        long: Longitude of the left corner
        number: Numbering to output file
        row: Row count
        osm: Open Street Map
        zoom: Zoom value
    Returns:

    """
    create_map(
        gmaps=gmaps,
        gmaps_satellite=gmaps_satellite,
        lat_start=lat,
        long_start=long,
        number=number,
        number_rows=row,
        number_cols=col,
        scale=0.5,
        sleep_time=2,
        offset_left=0,
        offset_top=0.17,
        offset_right=0,
        offset_bottom=0.10,
        osm=osm,
        outfile=file_name,
        zoom=zoom,  # can be changed to match OSM with GMaps
    )


# Example: 2x2 -> 4 images
take_screenshot(
    lat=37.795925,  # Top left corner latitude
    long=-122.3981861,  # Top left corner longitude
    row=2,  # 2 rows
    col=2,  # 2 cols
    file_name="image",  # Map image: "/images/test-{number}.png"
    number=1,  # Starting from 0 like image-0.png, image-1.png ...
    gmaps=False,  # Take screenshot from Google Maps
    gmaps_satellite=False,  # Take screenshot from Google Maps Satellite
    osm=True,  # Generate screenshots from OSM
    zoom=19,
)
