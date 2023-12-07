'''
Starting python page for Heat Island. User will run this page to get acess to the maps, etc.
'''

import time

from heat_island.getcoor.getcoor import select_coordinate
from heat_island.data_process import input_file_from_data_dir
from heat_island.geo_process import create_hexagon

cities = {"seattle": (47.606, -122.333)}
EXISTING = False
# boundaryPath = 'data/seattle-city-limits.geojson'

# If users want to input another set of data (new city)
print("We currently have data for the following city/cities:")
print(*cities)
response = input("What city would you like to view? Type 'New' for a new city.")

while not EXISTING:
    if response.lower() in cities :
        city = response.lower()
        # How to get access to the info needed for using Seattle map + Weather?
        EXISTING = True
    elif response.lower() == 'new':
        # 3. Request city name, and append to above list, cities
        city = input("What is the name of the new city?").lower()
        coordNew = input("What is the latitude/longitude coordinates of this city?")
        cities[city] = coordNew

        # Requests required data for new model formation/new height info       
        print('''Move your weather data into the 'data' directory, using the following
        format: 'city_weather'. e.g. 'seattle_weather'.''')
        filler = input("Press any key to continue")
        print('''Move your city boundary into the 'data' directory, using the following 
        format: 'city_boundary'. e.g. 'seattle_boundary'.''')
        filler = input("Press any key to continue")
        print('''Move your building data into the 'data' directory, using the following 
        format: 'city_building'. e.g. 'seattle_building'.''')
        filler = input("Press any key to continue")

        radius = input("Please set the radius used for ML Training. Enter 0 for default.")
        EXISTING = True
    else:
        print("This is not a valid response. Please either type a city name or 'New'.")
        response = input("What city would you like to view? Type 'New' for a new city.")

#input_file_from_data_dir(file name)
print("Please display both this page, and the following map simultaneously.")
time.sleep(2)  #Pauses to allow readers to read the message above
# Possibly loop, starting from here.

# Finding necessary directories
weatherFileDir = input_file_from_data_dir(city + "_weather")
boundaryFileDir = input_file_from_data_dir(city + "_boundary")
buildingFileDir = input_file_from_data_dir(city + "_building")

MOREPOINTS = True
while MOREPOINTS:
    # Returns latitude/longitude coordinates.
    print("Please select the coordinate where you want to run the weather model.")
    x, y = select_coordinate(boundaryFileDir)
    regionalCoord = create_hexagon(x, y, radius)

    # Call regionalCoord -> height here

    # Call the ML model here?

    # Call functions for applying ML here
    print('''Please hold on as the algorithm computes
    the expected temperature within the region.''')

    # Display data - What will it look like? Will create a folium pop-up regardless; can be a graph
    # or (various heights with various temperature predictions), or just a line of text as popup
    # and a text here directly.
    # Chart visualization look here: https://python-visualization.github.io/folium/latest/user_guide/ui_elements/popups.html
    # Look at the Vega/Vega Lite Charts
    more = input("Would you like to test more points? (y/n)")
    for i in range(3):
        if more.lower() == "n":
            MOREPOINTS = False
            break
        if more.lower() == "y":
            break
        else:
            if i == 2:
                print("We will stop running after another typo.")
            more = input("That's not a valid response. Please try again.")
        