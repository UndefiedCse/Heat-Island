"""This module is used to get coordinate from user input and
check whether the input is inside the boundary
"""
import folium
import json
import webbrowser
import os
from shapely.geometry import Polygon,GeometryCollection
from shapely import contains_xy
import pyperclip

def make_collection(features:list):
    res = []
    if not isinstance(features,list):
        features = list(features)
    if len(features) == 0:
        raise ValueError("Empty geometry")
    if not isinstance(features[0],dict):
        raise ValueError("Unexpected geojson format: Expect dict in each elements")
    for raw in features:
        if not 'geometry' in raw.keys():
            raise ValueError("Unexpected .GeoJson format: No 'geometry' key")
        geometry = raw['geometry']
        if not isinstance(geometry,dict):
            raise ValueError("Unexpected .GeoJson format: No dict inside argument")
        if not 'coordinates' in geometry.keys():
            raise ValueError("Unexpected .GeoJson format: No 'coordinates' key")
        for coor in geometry['coordinates']:
            res.append(Polygon(coor))
    return GeometryCollection(res)

def open_browser(json_path:str,output_dir:str=''):
    if not isinstance(output_dir,str):
        output_dir = str(output_dir)
    if output_dir != '':
        if not os.path.isdir(output_dir):
            raise ValueError("Output directory does not exist")
        if output_dir[-1] != '/':
            output_dir = output_dir + '/'
    if not isinstance(json_path,str):
        json_path = str(json_path)
    if not os.path.isfile(json_path):
        raise ValueError(".geojson file does not exist")
    if json_path[-4:].lower() != 'json':
        raise ValueError("Invalid file type: Expect .json or .geojson")
    with open(json_path,'r') as f:
        js = json.load(f)
    if not 'features' in js.keys():
        raise ValueError("Unexpected json structure")
    geocollection = make_collection(js['features'])
    left,bot,right,top = geocollection.buffer(0.01).bounds
    midp = (left+right)/2,(top+bot)/2
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
        folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "] Please, check terminal"')
    )
    folium.GeoJson(js).add_to(m)
    html_path = output_dir+'get_coordinate.html'
    m.save(html_path)
    webbrowser.open_new_tab(html_path)
    return geocollection,html_path

def main(path:str,temp_dir:str=''):
    if not isinstance(path,str):
        path = str(path)
    if not os.path.isfile(path):
        raise ValueError("Boundary file does not exist")
    geo_data,html_path = open_browser(path,temp_dir)
    for i in range(20):
        respond = ''
        print(f'Attempt {i}')
        raw_output = pyperclip.waitForNewPaste()
        coor = raw_output[:raw_output.rfind(']')+1]
        coor = eval(coor)
        while not respond in ('y','n'):
            respond = input(f"Here is coordinate {coor}\n Enter [y] if satisfied.\n Enter [n] to retry\n")
            if respond.lower() == 'y':
                break
            elif respond.lower() == 'n':
                break
        if respond.lower() == 'y':
            break
    # os.remove(html_path)
    return coor