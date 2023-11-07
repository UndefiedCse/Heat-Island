# Urban Heat Island Effect Project Outline:

# Target Area
Seattle Metropolitan Area (?)

# Datasets:
* Weather (specially, temperature at one day from multiple locations), corresponding with location (latitude/longitude).
* Building height, corresponding with location (latitude/longitude).

- Comment by LH: Building height acts as the causal factor, whereas temperature is the result.
- Comment by YZ: Weather in a fixed time window (say one work, 3 days before and after the target date)? This could help reduce short-term variation of temperature, etc.
- Comment by YZ: Added dataset: Building footprint info. Landuse in term of building/ water/ green area.
- NOTE: Why use building height?
  - I think we should compare the local temperatures to the average city temperature. Then, we can justify using the building height as affecting the temperature in some way, compared to the average?
  - Comment by LH: The concept of "the average city temperature" is indeed challenging to conceptualize, as it raises questions about the specific definition of a 'city' and the selection criteria for the cities in question. A potentially more illustrative comparison might involve contrasting the temperature of an urban area with that of its adjacent rural regions. This approach would underpin our hypothesis, positing that building height significantly influences temperature variations.
  - Comment by YZ: Ideally, I would expect our model to be robust enough: user provide a city dataset, and our model output a map of the tempraature of a larger context, showing how the urban built environemnt influences tempreature. In this regard, we need the morphology of city (can be height and building fotprint , or more deatiled lidar), and weather in a larger context.

# What are we trying to do?
* Correlate building height with the local weather

- NOTE: Why not building shapes?
  - I think this would be interesting, but possibly too difficult to do. If we can figure out how to convert this information into a CSV, or learn how to correlate shapes (i.e. lidar) directly into a correlation, this might be fine too. This would make parsing the data a smidge easier maybe?
- NOTE: Why average the building heights?
  - I think the local temperature would at least be dependent on the surrounding buildings, not just the current building. Thus, a small average sounds reasonable to me.
  - Comment by LH: I agree. At least surrounding the weather station.
 
## Model training
* Use latitude/longitude and building height to train a ML (?) model to find the relationship with temperature.
 
# Outcomes
Provide the coordinates and the height of the building, and receive the temperature as the output. If input a list of latitude/longitude with their building height, a heat map can be generated.
