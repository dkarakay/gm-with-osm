import matplotlib.pyplot as plt
import osmnx as ox
from IPython.display import Image


def getting_boundary_coordinates(lat: float, long: float) -> (float, float, float, float):
    lat_coef = 0.00034
    long_coef = 0.00095

    north = lat + lat_coef
    south = lat - lat_coef
    east = long + long_coef
    west = long - long_coef

    return north, south, east, west


def create_map_from_osm(outfile: str, c_osm: int, north: float, south: float, west: float, east: float):
    dpi = 100
    default_width = 2
    network_type = 'all'

    fp = f'./images/{outfile}-osm-{c_osm}.png'

    tag_building = {'building': True}
    tag_nature = {'natural': True, 'landuse': 'forest', 'landuse': 'grass'}
    tag_water = {'natural': 'water'}

    ax = None

    G = ox.graph_from_bbox(north, south, east, west, network_type=network_type)

    gdf_building = ox.geometries_from_bbox(north, south, east, west, tags=tag_building)
    gdf_nature = ox.geometries_from_bbox(north, south, east, west, tags=tag_nature)
    gdf_water = ox.geometries_from_bbox(north, south, east, west, tags=tag_water)

    fig, ax = ox.plot_figure_ground(G, default_width=default_width, dpi=dpi, filepath=fp, save=True, show=False,
                                    close=True)
    if ax:
        if not gdf_building.empty:
            fig, ax = ox.plot_footprints(gdf_building, ax=ax, filepath=fp, dpi=dpi, save=True, show=True, close=True)
            print('building found')
        if not gdf_nature.empty:
            fig, ax = ox.plot_footprints(gdf_nature, ax=ax, color='green', filepath=fp, dpi=dpi, save=True, show=False,
                                         close=True)
            print('nature found')
        if not gdf_water.empty:
            fig, ax = ox.plot_footprints(gdf_water, ax=ax, color='blue', filepath=fp, dpi=dpi, save=True, show=False,
                                         close=True)
            print('water found')


latitude = 40.0100192
longitude = -83.0134145
outfile = 'a0'
c_osm = 4
north, south, east, west = getting_boundary_coordinates(lat=latitude, long=longitude)
create_map_from_osm(outfile=outfile, c_osm=c_osm, north=north, south=south, east=east, west=west)
