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
 * **height_acquire**
    * Acquires building height data for a specified hexagonal area.
    * What it does: takes a hexagon polygon as input, and creates a GeoDataFrame that includes building heights.
    * Inputs: (shapely.geometry.polygon.Polygon) hexagon
    * Returns: (goppandas.GeoDataFrame) A GeoDataFrame containing the heights of buildings within the specified hexagon area
* **average_building_height_with_centroid**
    * Using shapely polygon hexagon to find building information 
    * What it does: Finds the average building height within a region of interest
    * Inputs: (shapely polygon/GeoJson polygon) hexagon, (goppandas.GeoDataFrame) building information
    * Returns: Various statistics related to the distribution of building heights

# Use case 3: Predict temperature of chosen location
* **train**
    * The main function for training the model. It handles data cleaning, splitting, model training, and evaluation.
    * What it does:
        * Get the dataset from **clean_data** 
        * Split dataset into training dataset and test dataset
        * Standardize the features
        * Train linear regression, K-nearest neighbor, and Random Forest Regression usig **find_best_estimator**
        * Save the best model according to score from **get_scores**
    * Input: (str) Path to training dataset, optional list of feature keys, (str, optional) target column name, optional save directory, and file name for the model.
    * Returns: (str) path to the saved model
 * **clean_data**
    * Reads and cleans data from a file, preparing it for further processing in **train**
    * What it does:
        * Load the training dataset from the file path
        * Remove all rows with missing value
    * Input: (str) path to training dataset file, (list) list of feature column's name, (str) output column name
    * Return: (dataframe) dataframe of features, (Series) Series of annual average temperature in fahrenheit
 * **load_model**
    * Retrieves model from model file
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
