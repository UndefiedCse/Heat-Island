# heat_island
# Urban Heat Island Effect
The urban heat island effect is a phenomenon where urban areas, where structures such as buildings and roads are highly concentrated, experience significantly higher temperatures than surrounding rural areas. The Urban Heat Island Effect Project, leveraging machine learning algorithms, aims to accurately predict temperature variations within urban environments based on location and physical characteristics of the area, with a particular focus on building height and terrain. 

![alt text](doc/urban_heat_island_profile.jpg)

(picture credit: [Urbanland](https://urbanland.uli.org/public/four-approaches-to-reducing-the-urban-heat-island-effect/))

The **heat_island** package is designed to estimate the local temperature based on the heights of the surrounding buildings. It is currently designed to work for the city of Seattle, but can be used for other cities with proper data formatting. Upon running, users will have the option to select locations of interest on a map, then receive an expected temperature for each location.

## Data sources:
* [Building footprint and height](https://github.com/microsoft/GlobalMLBuildingFootprints)
* [Terrain](https://apps.nationalmap.gov/downloader/)
* [Weather Underground](https://www.wunderground.com/)

### Target area
City of Seattle (city boundary is acquired from [Seattle GeoData](https://data-seattlecitygis.opendata.arcgis.com/datasets/c5f3575dd7d545ada27064c74ac74f52_0/explore?location=47.622532%2C-122.278830%2C11.00))


## Software dependencies
### Programming language:
- Python version 3.10 and above

### Python packages needed:
- folium
- geojson
- geopandas
- matplotlib
- mercantile
- numpy
- pandas
- pyperclip
- rasterio
- rasterstats
- scikit-learn
- scipy
- shapely
- tqdm


## Description

### Data processing
Data processing was carried out using the scripts `data_process.py`, `height_acquire.py`, and `geo_process.py`. These scripts are designed to preprocess `.csv` and `.geojson` files, ensuring that they meet our specific requirements.

### Model training and testing

Before training the model, we needed to preprocess the data by dropping all data with `NaN` value. Then we standardized all features using `StandardScaler` function in `sklearn`.

In the model training, we choose the best regression model between `Linear Regression`, `Random Forest Regression`, and `K-Nearest Neighbor`

For each regression model, hyperparameters were optimized using 5-fold cross validation. To evaluate the best regression model after getting the best hyperparameter for each model, we used Root Mean Square Error (RMSE) and chose the model with the lowest RMSE.

After getting the best regression model, we saved the model and scale in `.bin` format and we provided loading function (`load_model`) to load the model after save.


### User interaction / visualization

A map will be displayed using an existing library called Folium. From here, users will be able to select points of interest on a map. After the system is done computing the expected temperatures, it will display the results in the console. All displays are run directly on 'heat_island_main.py'.

## Installation
- Create a virtual environment based on the environment dependency. `conda env create -f environment.yml`
- Run the main page. `python heat_island_main.py`

## Directory Structure
```
Heat-Island (master)
|    .gitignore
|    LICENSE
|    README.md
|    environment.yml
|    heat_island_main.py
|
|----- .github/workflows
|    |    python-flake8.yml
|    |    python-unittest.yml
|    |    python-pylint.yml
|
|----- doc
|    |    user-story.md
|    |    use_cases.md
|    |    components.md
|    |    urban_heat_island_profile.jpg
|    |    Technology Review CSE583.pptx
|    |    CSE583 Final Presentation.pptx
|
|----- data
|    |    seattle_boundary.geojson
|    |    seattle_weather.csv
|    |    processed_seattle_weather.csv
|    |    seattle_building_footprints.geojson
|    |    example_aggr_hexagon(2).geojson
|    |    seattle_model.bin
|
|----- heat_island (package)
|    |    __init__.py
|    |    data_process.py
|    |    geo_process.py
|    |    height_acquire.py
|    |    terrain_acquire.py
|    |    getcoor.py
|    |    model.py
|
|----- tests
|    |    __init__.py
|    |    test_geo_process.py
|    |    test_height_acquire.py
|    |    test_getcoor.py
|    |    test_model.py
|    |----- data
|    |    |    nan.geojson
|    |    |    normal.geojson
|    |    |    small.geojson
|
|----- demo
|    |    data_processing.ipynb
```


## Team Members
Zihan (Lilac) Hong, Krittin Kulrattanaruks, Lori Won, Yongqin Zhao. 
(Sort by the first letter of the last name.)


