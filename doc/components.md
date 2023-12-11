# Use case 1: Selecting building location
* Map view that allows users to visualize building and location
    * Name: open_browser
    * What it does: Displays a map of the city of interest (bounded) using Folium
    * Inputs: (str) path to the file with the city boundary (should be in data folder), [opt, str] path of the directory for saving the boundary-overlayed map
    * Returns: (str) path to the html map
* User interface via Folium that allows clicking building coordinates (Latitude/longitude)
    * Name: select_coordinate
    * What it does: Allows a user to select point(s) of interest on a displayed map to return the latitude/longitude coordinates of that point
    * Inputs: (str) path to the file with the city boundary (in data folder), [opt, str] path of the directory for saving the boundary-overlayed map, [opt, bool] decide whether to save the overlayed map
    * Returns: (float) latitude, (float) longitude

# Use case 2: Mapping average building height based on a latitude/longitude
* Selecting smaller hexagonal region surrounding a point
    * Name: create_hexagon
    * What it does: Creates a hexagon to determine the area which to include the heights
    * Inputs: (float) latitude, (float) longitude
    * Returns: (polygon via shapely) hexagon shaped polygon
* Converting said hexagon into a GeoJson file **for user to see??**
    * Name: hex_to_geojson
    * What it does: Converts the above hexagon polygon into a geojson file for Folium compatability
    * Input: (polygon via shapely) hexagon shaped polygon, from above method
    * Returns: (Folium object(?))
* Using GeoJson **(or shapely polygon)** hexagon to find building information
    * Name: average_building_height_with_centroid
    * What it does: Finds the average building height within a region of interest
    * Inputs: (shapely polygon/GeoJson polygon) hexagon, **(pd dataframe??)** building information
    * **Returns:** Various statistics related to the distribution of building heights

# Use case 3: Visualize time series weather data by station
## Components
* Database with tempearature data across different weather stations
## Description
* What it does: Allows user to choose between spring/summer/fall/winter/annual to determine what season, or annual weather, they wish to see.
* Input: Click one of five choices, result should be string
* Output: ?
  
# Use case 4: Get predicted temperature by entering location and building height
## Components
* Database with pretrained model
* User interface that allows users to enter Latitude/longitude, building height
* User interface that displays the predicted temperature
## Description
* Input: latitude/longitude (float), building height (float)
* Output: temperature (float)

# Future Considerations
* Input expected building height, to run each height on the model and generate graph correlating expected temperature and building height
* Selecting for season of interest. Again, need to update the ML model to distinguish between seasons or months.
