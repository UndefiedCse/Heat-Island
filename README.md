# heat_island
# Urban Heat Island Effect
The urban heat island effect is a phenomenon where urban areas, where structures such as buildings and roads are highly concentrated, experience significantly higher temperatures than surrounding rural areas. The Urban Heat Island Effect Project, leveraging machine learning algorithms, aims to accurately predict temperature variations within urban environments based on location and physical characteristics of the area, with a particular focus on building height and terrain. 

![alt text](https://github.com/LilacHo/Heat-Island/blob/main/doc/urban_heat_island_profile.jpg)

(picture credit: [Urbanland](https://urbanland.uli.org/public/four-approaches-to-reducing-the-urban-heat-island-effect/))

The **heat_island** ... (tentative, describe the application of our package)

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
- pandas
- numpy
- matplotlib
- rasterio
- pyproj
- geopandas
- geojson
- ellipsis
- h3pandas
- h3-py
- mercantile
- folium
- rasterstats
- pyperclip
- scikit-learn


## Description

### Data processing
Data processing was carried out using the scripts `data_process.py`, `height_acquire.py`, and `geo_process.py`. These scripts are designed to preprocess `.csv` and `.geojson` files, ensuring that they meet our specific requirements.

### Model training and testing

### User interaction / visualization


## Installation
- Create a virtual environment based on the environment dependency. `conda env create -f environment.yml`

## Directory Structure
```
Heat-Island (master)
|    .gitignore
|    License
|    README.md
|
|----- doc
|    |    user-story.md
|    |    use_cases.md
|    |    components.md
|    |    Technology Review CSE583.pptx
|
|----- data
|    |    seattle-city-limits.geojson
|    |    weather_Seattle.csv
|
|----- heat_island (package)
|    |    __init__.py
|    |  
```


## Team Members
Zihan (Lilac) Hong, Krittin Kulrattanaruks, Lori Won, Yongqin Zhao. 
(Sort by the first letter of the last name.)


