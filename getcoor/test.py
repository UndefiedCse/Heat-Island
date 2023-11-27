import folium
import json
import webbrowser
with open('data/seattle-city-limits.geojson','r') as f:
    js = json.load(f)
m = folium.Map()
m.add_child(folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "] Please close this window and continue the program"'))
folium.GeoJson(js).add_to(m)
m.save('test.html')
webbrowser.open_new_tab('test.html')