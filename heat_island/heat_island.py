'''
Starting python page for Heat Island. User will run this page to get acess to the maps, etc.
'''

import folium
import time

from heat_island.getcoor import getcoor

cities = {"seattle": (47.606, -122.333)}
existing = False

# If users want to input another set of data (new city)
print("We currently have data for the following city/cities:")
print(*cities)
response = input("What city would you like to view? Type 'New' for a new city.")

while existing == False:
    if response.lower() in cities :
        city = response
        # How to get access to the info needed for using Seattle map + Weather?
        existing = True
    elif response.lower() == 'new':
        # 3. Request city name, and append to above list, cities
        city = input("What is the name of the new city?")
        coordNew = input("What is the latitude/longitude coordinates of this city?")
        cities[city] = coordNew
        # DO SOMETHING - I'm not sure exactly what information we would need
        # 1. Request weather data, in specific format
        # 2. Request city LIDAR data, in specific format
        # 4. Need to verify the existing model works for this new set of data. If not, 
        #     let user know that current model doesn't work; will need to retrain? 
        existing = True
    else:
        print("This is not a valid response. Please either type a city name or 'New'.")
        response = input("What city would you like to view? Type 'New' for a new city.")

print("Please display both this page, and the following map simultaneously.")
time.sleep(2)  #Pauses to allow readers to read the message above
# Possibly loop, starting from here.
# Call functions from getcoor.py here! Returns latitude/longitude coordinates.

# Call the ML model here?
# Call functions for applying ML here

print("Please hold on as the algorithm computes the expected temperature within the region.")

# Display data - What will it look like? Will create a folium pop-up regardless; can be a graph
# or (various heights with various temperature predictions), or just a line of text as popup
# and a text here directly.
# Chart visualization look here: https://python-visualization.github.io/folium/latest/user_guide/ui_elements/popups.html
# Look at the Vega/Vega Lite Charts
