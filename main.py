import os
import time
import tkinter
import osmnx as ox

from PIL import Image
import pyscreenshot
from selenium import webdriver

# Removing fields from Google Maps
remove_from_view = [
    "var element = document.getElementById(\"omnibox-container\");element.remove();",
    "var element = document.getElementById(\"watermark\");element.remove();",
    "var element = document.getElementById(\"vasquette\");element.remove();",
    "var element = document.getElementsByClassName(\"app-viewcard-strip\");element[0].remove();",
    "var element = document.getElementsByClassName(\"scene-footer-container\");element[0].remove();",

]

# Removing labels from Google Maps Satellite View
remove_labels = [
    "var element = document.getElementsByClassName(\"searchbox-hamburger-container\")[0];"
    "element.getElementsByTagName(\"button\")[0].click();",
    "var element = document.getElementsByClassName(\"widget-settings-earth-item\")[0];"
    "element.getElementsByTagName(\"button\")[1].click();",

]


def js_code_execute(driver, js_string: str):
    """Execute the JS code"""
    driver.execute_script(js_string)


def get_screen_resolution() -> tuple:
    """Return tuple of (width, height) of screen resolution in pixels."""
    root = tkinter.Tk()
    root.withdraw()
    return root.winfo_screenwidth(), root.winfo_screenheight()


def calc_latitude_shift(screen_height: int, percent_hidden: float, zoom: int) -> float:
    """Return the amount to shift latitude per row of screenshots."""
    return -0.000002051 * screen_height * (1 - percent_hidden) * (1 / 1.7 ** (zoom - 18))


def calc_longitude_shift(screen_width: int, percent_hidden: float, zoom: int) -> float:
    """Return the amount to shift longitude per column of screenshots."""
    return 0.00000268 * screen_width * (1 - percent_hidden) * (1 / 1.7 ** (zoom - 18))


def screenshot(screen_width: int, screen_height: int,
               offset_left: float, offset_top: float,
               offset_right: float, offset_bottom: float) -> Image:
    """Return a screenshot of only the pure maps area."""
    x1 = offset_left * screen_width
    y1 = offset_top * screen_height
    x2 = (offset_right * -screen_width) + screen_width
    y2 = (offset_bottom * -screen_height) + screen_height
    image = pyscreenshot.grab(bbox=(x1, y1, x2, y2))

    offset_top = 1 / 6
    x1 = offset_top * screen_height
    y1 = offset_top * screen_height
    x2 = (1 - offset_top) * screen_height
    y2 = (1 - offset_top) * screen_height
    image = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
    return image


def scale_image(image: Image, scale: float) -> Image:
    """Scale an Image by a proportion, maintaining aspect ratio."""
    width = round(image.width * scale)
    height = round(image.height * scale)
    image.thumbnail((width, height))
    return image


def combine_images(images: list) -> Image:
    """Return combined image from a grid of identically-sized images.
    images is a 2d list of Image objects. The images should
    be already sorted/arranged when provided to this function.
    """
    img_width = images[0][0].width
    img_height = images[0][0].height
    new_size = (img_width * len(images[0]), img_height * len(images))
    new_image = Image.new('RGB', new_size)

    # Add all the images from the grid to the new, blank image
    for rowindex, row in enumerate(images):
        for colindex, image in enumerate(row):
            location = (colindex * img_width, rowindex * img_height)
            new_image.paste(image, location)

    return new_image


def getting_boundary_coordinates(lat: float, long: float) -> (float, float, float, float):
    lat_coef = 0.00035
    long_coef = 0.00095

    north = lat + lat_coef
    south = lat - lat_coef
    east = long + long_coef
    west = long - long_coef

    return north, south, east, west


def create_square_from_osm(outfile: str, c_osm: int, point, dpi=100, dist=2000, default_width=6):
    network_type = 'drive'

    fp = f'./images/{outfile}-osm-{c_osm}.png'

    tag_building = {'building': True}
    tag_nature = {'natural': True, 'landuse': 'forest', 'landuse': 'grass'}
    tag_water = {'natural': 'water'}

    bbox = ox.utils_geo.bbox_from_point(point, dist=dist)
    G = ox.graph_from_point(point, network_type=network_type, dist=dist, truncate_by_edge=True, retain_all=True,
                            clean_periphery=True)

    gdf_building = ox.geometries_from_point(point, tag_building, dist=dist)
    gdf_nature = ox.geometries_from_point(point, tag_nature, dist=dist)
    gdf_water = ox.geometries_from_point(point, tag_water, dist=dist)

    fig, ax = ox.plot_figure_ground(G, default_width=default_width, show=False)

    if not gdf_building.empty:
        fig, ax = ox.plot_footprints(gdf_building, ax=ax, bbox=bbox, filepath=fp, dpi=dpi, save=True)
    if not gdf_nature.empty:
        fig, ax = ox.plot_footprints(gdf_nature, ax=ax, bbox=bbox, color='green', filepath=fp, dpi=dpi, save=True)
    if not gdf_water.empty:
        fig, ax = ox.plot_footprints(gdf_water, ax=ax, bbox=bbox, color='blue', filepath=fp, dpi=dpi, save=True)
    print('finito')


def create_map_from_osm(outfile: str, c_osm: int, north: float, south: float, west: float, east: float):
    dpi = 200
    default_width = 6
    network_type = 'drive'

    fp = f'./images/{outfile}-osm-{c_osm}.png'

    tag_building = {'building': True}
    tag_water = {'natural': 'water'}

    ax = None

    G = ox.graph_from_bbox(north, south, east, west, network_type=network_type,
                           truncate_by_edge=True, retain_all=True, clean_periphery=True)

    gdf_building = ox.geometries_from_bbox(north, south, east, west, tags=tag_building)
    gdf_nature = ox.geometries_from_bbox(north, south, east, west,
                                         tags={'natural': True, 'landuse': 'forest', 'landuse': 'grass'})
    gdf_water = ox.geometries_from_bbox(north, south, east, west, tags=tag_water)

    fig, ax = ox.plot_figure_ground(G, default_width=default_width, dpi=dpi, filepath=fp, show=False)
    if not gdf_nature.empty:
        fig, ax = ox.plot_footprints(gdf_nature, ax=ax, color='green', filepath=fp, dpi=dpi, save=True)
    if not gdf_water.empty:
        fig, ax = ox.plot_footprints(gdf_water, ax=ax, color='blue', filepath=fp, dpi=dpi, save=True)
    if not gdf_building.empty:
        fig, ax = ox.plot_footprints(gdf_building, ax=ax, filepath=fp, dpi=dpi, save=True)


def create_map(lat_start: float, long_start: float, zoom: int,
               number_rows: int, number_cols: int,
               scale: float = 1, sleep_time: float = 0,
               offset_left: float = 0, offset_top: float = 0,
               offset_right: float = 0, offset_bottom: float = 0,
               outfile: str = None, number: int = 0):
    """

    Args:
        lat_start: Top-left coordinate to start taking screenshots.
        long_start: Top-left coordinate to start taking screenshots.
        number: Name of image
        number_rows: Number of rows to take screenshot.
        number_cols: Number of columns to to create screenshot.
        scale: Percent to scale each image to reduce final resolution
            and filesize. Should be a float value between 0 and 1.
            Recommend to leave at 1 for production, and between 0.05
            and 0.2 for testing.
        sleep_time: Seconds to sleep between screenshots.
            Needed because Gmaps has some AJAX queries that will make
            the image better a few seconds after confirming page load.
            Recommend 0 for testing, and 3-5 seconds for production.
        offset_*: Percent of each side to crop from screenshots.
            Each should be a float value between 0 and 1. Offsets should
            account for all unwanted screen elements, including:
            taskbars, windows, multiple displays, and Gmaps UI (minimap,
            search box, compass/zoom buttons). Defaults are set for an
            Ubuntu laptop with left-side taskbar, and will need to be
            tuned to the specific machine and setup where it will be run.
        outfile: If provided, the program will save the final image to
            this filepath. Otherwise, it will be saved in the current
            working directory with name 'testing-<timestamp>.png'
        offset_right: Right offset.
        offset_top: Top offset.
        offset_bottom: Bottom offset.
        offset_left: Left offset.
        zoom: zoom level
    """

    # DRIVER Selection
    # Chromedriver should be in the current directory.
    # Modify these commands to find proper driver Chrome or Firefox
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
    driver = webdriver.Chrome(executable_path=DRIVER_BIN)

    driver.maximize_window()

    # Calculate amount to shift lat/long each screenshot
    screen_width, screen_height = get_screen_resolution()

    # Shifting values for lat and long
    lat_shift = calc_latitude_shift(screen_height, (offset_top + offset_bottom), zoom) - 0.00021
    long_shift = calc_longitude_shift(screen_width, (offset_left + offset_right), zoom) + 0.000595

    # Giving numbers for example and satellite images
    c_map = number
    c_image = number
    c_osm = number

    # Writing coordinates to the file
    f = open("coordinates.txt", "w+")

    satellite_images = [[None for _ in range(number_cols)]
                        for _ in range(number_rows)]

    """
    i = 0 -> Map View
    i = 1 -> Satellite View
    i = 2 -> OpenStreetMap View
    """
    for i in range(1, 3):
        for row in range(number_rows):
            for col in range(number_cols):

                latitude = lat_start + (lat_shift * row)
                longitude = long_start + (long_shift * col)

                if i == 2:
                    point = (latitude - (lat_shift * row), longitude - (long_shift * col) - 0.000375)
                    # north, south, east, west = getting_boundary_coordinates(lat=latitude, long=longitude)
                    # create_map_from_osm(outfile=outfile, c_osm=c_osm, north=north, south=south, east=east, west=west)
                    create_square_from_osm(outfile=outfile, c_osm=c_osm, point=point, dist=35, dpi=200,
                                           default_width=50)
                    c_osm += 1

                elif i == 1:
                    url = 'https://www.google.com/maps/'

                    # Map URL
                    if i == 0:
                        url += '@{lat},{long},{z}z'.format(lat=latitude, long=longitude, z=zoom)
                    # Satellite URL
                    elif i == 1:
                        url += '@{lat},{long},{z}z/data=!3m1!1e3'.format(lat=latitude, long=longitude, z=zoom)

                    driver.get(url)
                    time.sleep(5)

                    # Remove labels from Satellite view
                    if i == 1:
                        js_code_execute(driver, remove_labels[0])
                        time.sleep(3)
                        js_code_execute(driver, remove_labels[1])

                    # Remove fields from Map view
                    for j in remove_from_view:
                        js_code_execute(driver, j)

                    # Let the example load all assets before taking a screenshot
                    time.sleep(sleep_time)
                    image = screenshot(screen_width, screen_height, offset_left, offset_top, offset_right,
                                       offset_bottom)

                    # Scale image up or down if desired, then save in memory
                    image = scale_image(image, scale)
                    if i == 0:
                        # image.save(f"{outfile}-example-{row}-{col}.png")  # To save the row-col position uncomment
                        # image.save(f"./images/{outfile}-example-{c_map}.png")
                        c_map += 1
                    else:
                        # image.save(f"{outfile}-{row}-{col}.png") # To save the row-col position uncomment
                        f.write(f"{outfile}-{c_map}.png -> Lat: {latitude} Long: {longitude} URL: {url} \n")
                        image.save(f"./images/{outfile}-{c_image}.png")
                        satellite_images[row][col] = image
                        c_image += 1

    # Close the browser
    driver.close()
    driver.quit()
    f.close()

    # north, south, east, west = lat_start, lat_start + (lat_shift * number_rows), long_start, long_start + (
    #            long_shift * number_cols)
    # create_map_from_osm(outfile=outfile, c_osm=c_osm, north=north, south=south, east=east, west=west)

    # final = combine_images(satellite_images)

# outfile = 'test.png'

# final.save(outfile)
