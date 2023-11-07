# Case 1: Architect
## Use case: Selecting building location
* Allows user to enter a latitude/longitude coordinate of the position building site. Alternatively, they can click a location on a displayed map.
* Input: Latitude/longitude (float, unless too long, then string), or a click identifying such info (will be converted into float/string)
* Output: Latitude/Longitude (float/string)

## Use case: Building
* Contains important general information about the buildings.
* Input: latitude/longitude (float/string)
* Output: Building specs (building object, not displayed towards user)
  * Building height
  * Latitude/longitude
  * general building size

## Select seaon/date of interest or average yearly temperature
* Allows user to choose between spring/summer/fall/winter/annual to determine what season, or annual weather, they wish to see.
* Input: Click one of five choices, result should be string
* Output: ?
  
## Past weather data
