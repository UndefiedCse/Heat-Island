"""
This module facilitates the interaction between a user and geographic data.
It primarily deals with loading city boundaries from GeoJSON files,
enabling a user to select a specific geographical coordinate
within these boundaries through an interactive map interface.
The module leverages libraries such as folium for map rendering,
shapely for geometric operations,
and pyperclip for clipboard interactions.
It is designed to be user-friendly,
providing clear instructions and
feedback throughout the process of coordinate selection.
"""

import json
import os
import webbrowser
import folium
from shapely.geometry import Polygon, GeometryCollection
import pyperclip


def make_collection(features: list):
    """
    Creates a GeometryCollection object
    representing city boundaries from a list of GeoJSON features.
    Example: make_collection(js['features'])

    Args:
        features (list): list of features

    Raises:
        ValueError: There is no data in features
        ValueError: Unexpected geojson format
        ValueError: No 'geometry' as key in each feature
        ValueError: feature['geometry'] is not a dictionary
        ValueError: No 'coordinates' as a key in feature['geometry']

    Returns:
        GeometryCollection: Set of polygon containing city boundary
    """
    res = []
    if not isinstance(features, list):
        features = list(features)
    if len(features) == 0:
        raise ValueError("Empty geometry")
    if not isinstance(features[0], dict):
        raise ValueError("""Unexpected geojson format:
                             Expect dict in each elements""")
    for raw in features:
        if 'geometry' not in raw.keys():
            raise ValueError("Unexpected .GeoJson format: No 'geometry' key")
        geometry = raw['geometry']
        if not isinstance(geometry, dict):
            raise ValueError("""Unexpected .GeoJson format:
                                 No dict inside argument""")
        if 'coordinates' not in geometry.keys():
            raise ValueError("""Unexpected .GeoJson format:
                                 No 'coordinates' key""")
        for coor in geometry['coordinates']:
            res.append(Polygon(coor))
    return GeometryCollection(res)


def open_browser(json_path: str, output_dir: str = ''):
    """
    Opens a web browser with an interactive map
    for the user to select a point within the specified city boundary.
    The coordinate of the selected point is then copied to the clipboard.

    Args:
        json_path (str): path to city boundary
        output_dir (str, optional): directory for saving local html file.
                                    Defaults to ''.

    Raises:
        ValueError: if output_dir directory does not exist
        ValueError: input .json file does not exist
        ValueError: Unexpected file format
        ValueError: Unexpected .json file structure

    Returns:
        str: path to local html
    """
    if not isinstance(output_dir, str):
        output_dir = str(output_dir)
    if output_dir != '':
        if not os.path.isdir(output_dir):
            raise ValueError("Output directory does not exist")
        if output_dir[-1] != '/':
            output_dir = output_dir + '/'
    if not isinstance(json_path, str):
        json_path = str(json_path)
    if not os.path.isfile(json_path):
        raise ValueError(".geojson file does not exist")
    if json_path[-4:].lower() != 'json':
        raise ValueError("Invalid file type: Expect .json or .geojson")
    with open(json_path, 'r', encoding='utf-8') as f:
        js = json.load(f)
    if 'features' not in js.keys():
        raise ValueError("Unexpected json structure")
    geocollection = make_collection(js['features'])
    left, bot, right, top = geocollection.buffer(0.01).bounds
    midp = (left+right)/2, (top+bot)/2
    m = folium.Map(
        location=midp,
        min_lat=bot,
        max_lat=top,
        min_lon=left,
        max_lon=right,
        max_bounds=True,
        control_scale=True,
        zoom_start=12
    )
    m.add_child(
        folium.ClickForLatLng(
            format_str='"[" + lat + "," + lng + "] Please, check terminal"')
    )
    folium.GeoJson(js).add_to(m)
    html_path = output_dir+'get_coordinate.html'
    m.save(html_path)
    webbrowser.open_new_tab(html_path)
    return html_path


def select_coordinate(path: str, temp_dir: str = '', save_html: bool = False):
    """
    Main function to facilitate the user in selecting a coordinate
    from the city boundary.
    It integrates the process of opening the browser,
    selecting the point, and returning the chosen coordinate.

    Args:
        path (str): path to city boundary
        temp_dir (str, optional): directory for saving local html file.
            Defaults to ''.
        save_html (boll, optional): choose whether to save html or delete
            after complete choosing. Default to ''.

    Raises:
        ValueError: .json file does not exist

    Returns:
        x (float): longitude of the chosen point
        y (float): latitude of the chosen point
    """
    if not isinstance(path, str):
        path = str(path)
    if not os.path.isfile(path):
        raise ValueError("Boundary file does not exist")
    html_path = open_browser(path, temp_dir)
    for i in range(20):
        respond = ''
        print(f'Attempt {i}')
        raw_output = pyperclip.waitForNewPaste()
        y = float(raw_output[raw_output.find(',')+1:raw_output.rfind(']')])
        x = float(raw_output[1:raw_output.find(',')])
        while respond not in ('y', 'n'):
            respond = input(f"""Here is coordinate ({y},{x})
                            \n Enter [y] if satisfied.
                            \n Enter [n] to retry\n""")
            if respond.lower() == 'y':
                break
            if respond.lower() == 'n':
                webbrowser.open_new_tab(html_path)
                break
        if respond.lower() == 'y':
            break
    if not save_html:
        os.remove(html_path)
    return x, y
