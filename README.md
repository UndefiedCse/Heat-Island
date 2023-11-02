# Weather-data

Project Outline:

# Datasets:
* Weather, corresponding with location (latitude/longitude).
* Weather, averaged for the city (i.e. "Seattle" weather)
* Building height, corresponding with location (latitude/longitude).

- NOTE: Why use building height?
  - I think we should compare the local temperatures to the average city temperature. Then, we can justify using the building height as affecting the temperature in some way, compared to the average?

# What are we trying to do?
* Correlate building height (averaged over some area) with the local weather

- NOTE: Why not building shapes?
  - I think this would be interesting, but possibly too difficult to do. If we can figure out how to convert this information into a CSV, or learn how to correlate shapes (i.e. lidar) directly into a correlation, this might be fine too. This would make parsing the data a smidge easier maybe?
- NOTE: Why average the building heights?
  - I think the local temperature would at least be dependent on the surrounding buildings, not just the current building. Thus, a small average sounds reasonable to me.
 
# Outcomes
(In simplest forms): Asks for coordinate of location, asks for either 1) expected building height, or 2) how much do you want different from average temperature. Returns the value not inputted.
