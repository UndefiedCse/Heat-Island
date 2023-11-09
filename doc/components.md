# Use case 1: Selecting building location
## Components
* Map view that allows users to visualize building and location
* User interface (textbox?) that receives specific building coordinate (Latitude/longitude)
## Description
* What it does: Allows user to enter a latitude/longitude coordinate of the position building site. Alternatively, they can click a location on a displayed map.
* Input: Latitude/longitude (float, unless too long, then string), or a click identifying such info (will be converted into float/string)
* Output: Latitude/Longitude (float/string)

# Use case 2: Mapping average Building height by neighborhood(?)
## Components
* Database with building height and location
* Map view ...
## Description
* What it does: Contains important general information about the buildings.
* Input: latitude/longitude (float/string)
* Output: Building specs (building object, not displayed towards user)
  * Building height
  * Latitude/longitude
  * general building size

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
