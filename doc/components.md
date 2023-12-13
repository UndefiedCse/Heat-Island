# Use case 1: Selecting building location
* **open_browser**
    * Map view that allows users to visualize building and location
    * What it does: Displays a map of the city of interest (bounded) using Folium
    * Inputs: (str) path to the file with the city boundary (should be in data folder), [opt, str] path of the directory for saving the boundary-overlayed map
    * Returns: (str) path to the html map
* **select_coordinate**
    * User interface via Folium that allows clicking building coordinates (Latitude/longitude)
    * What it does: Allows a user to select point(s) of interest on a displayed map to return the latitude/longitude coordinates of that point
    * Inputs: (str) path to the file with the city boundary (in data folder), [opt, str] path of the directory for saving the boundary-overlayed map, [opt, bool] decide whether to save the overlayed map
    * Returns: (float) latitude, (float) longitude

# Use case 2: Find average building height based on a latitude/longitude
* **create_hexagon**
    * Selecting smaller hexagonal region surrounding a point
    * What it does: Creates a hexagon to determine the area which to include the heights. It is used to find building height information to build the model and to generate data for user-selected points.
    * Inputs: (float) latitude, (float) longitude
    * Returns: (polygon via shapely) hexagon shaped polygon
* **hex_to_geojson**
    * Converting said hexagon into a GeoJson file
    * What it does: Converts the above hexagon polygon into a geojson file for Folium compatability
    * Input: (polygon via shapely) hexagon shaped polygon, from above method
    * Returns: **(Folium object(?))**
* **average_building_height_with_centroid**
    * Using **shapely polygon** hexagon to find building information 
    * What it does: Finds the average building height within a region of interest
    * Inputs: **(shapely polygon/GeoJson polygon)** hexagon, **(pd dataframe/dictionary??)** building information
    * Returns: Various statistics related to the distribution of building heights

# Use case 3: Predict temperature of chosen location
* **train**
    * Trains ML model
    * What it does: Trains the machine learning model based on the building heights and the corresponding weather. The model is automatically saved within our model folder
    * Input: (str) path to the file with the training dataset **(contains building heights, weather info)**, **?? Not sure what else goes here**
    * Returns: (str) path to the saved model
 * **load_model**
    * Retrieves model from model folder
    * What it does: Retrieves the model that has either been preset (Seattle) or has been saved by the train function from above.
    * Inputs: (str) path to the file with the model = output of train
    * Returns: (regressor) the ML trained model, (sklearn.preprocessing) the scaler associated with the model
 * **predict**
    * Predicts an output based on the given model.
    * What it does: Takes the new coordinate, which has been converted to a **shapely polygon**, and runs it through the ML model to generate an expected temperature.
    * Inputs: (regressor) trained ML model, (sklearn.preprocessing) the scaler associated with the trained model, (dataframe) the data containing the building heights for the selected coordinate
    * Returns: (pd series) Returns the predicted value(s) based on the input coordinate.

# Future Considerations
* Input expected building height, to run each height on the model and generate graph correlating expected temperature and building height
* Selecting for season of interest. Again, need to update the ML model to distinguish between seasons or months.
