import pandas as pd
import geopandas as gpd
import shapely.geometry
import mercantile
from tqdm import tqdm
import os
import tempfile
import fiona

from data_process import input_file_from_data_dir

# Example that previous offered
# aoi_geom = {
#     "coordinates": [
#         [
#             [-122.16484503187519, 47.69090474454916],
#             [-122.16484503187519, 47.6217555345674],
#             [-122.06529607517405, 47.6217555345674],
#             [-122.06529607517405, 47.69090474454916],
#             [-122.16484503187519, 47.69090474454916],
#         ]
#     ],
#     "type": "Polygon",
# }

# Read in the GeoJSON file for Seattle city limits
seattle = gpd.read_file(input_file_from_data_dir("seattle-city-limits.geojson"))
# Extract the first geometry object from the GeoDataFrame
aoi_geom = seattle.geometry[0]
aoi_shape = shapely.geometry.shape(aoi_geom)
# Get the bounds of the area of interest (AOI)
minx, miny, maxx, maxy = aoi_shape.bounds
# For Seattle city limit:
# minx = -122.40985799299995
# miny = 47.64445376000003
# maxx = -122.24563167199994
# maxy = 47.73416571200005
# Slightly increase the area of interest to ensure coverage
minx = minx - 0.001 # minimum longitude
miny = miny - 0.001 # minimum latitude
maxx = maxx + 0.001 # maximum longitude
maxy = maxy + 0.001 # maximum latitude

# Define the output file name for the building footprints
output_fn = os.path.join("data","example_building_footprints.geojson")


# Initialize an empty set to store quad keys
quad_keys = set()
# Generate quad keys for tiles within the bounds at zoom level 9
for tile in list(mercantile.tiles(minx, miny, maxx, maxy, zooms=9)):
    quad_keys.add(int(mercantile.quadkey(tile)))
# Convert the set of quad keys to a list
quad_keys = list(quad_keys)
print(f"The input area spans {len(quad_keys)} tiles: {quad_keys}")


# Read the dataset links CSV file
df = pd.read_csv(
    "https://minedbuildings.blob.core.windows.net/global-buildings/dataset-links.csv"
)
# Debug print statement - can be removed in production
# print(df)

# Debug statement
quad_keys = [21230021]
# Initialize index and a list to combine rows from different files
idx = 0
combined_rows = []

# Create a temporary directory to store downloaded files
with tempfile.TemporaryDirectory() as tmpdir:
    # List to store temporary file names
    tmp_fns = []
    # Iterate over each quad key
    for quad_key in tqdm(quad_keys):
        # Find rows in the dataset that match the current quad key
        rows = df[df["QuadKey"] == quad_key]
        # Debug print statement - can be removed in production
        # print(rows)

        # If exactly one row is found for the quad key
        if rows.shape[0] == 1:
            # Get the URL of the GeoJSON file
            url = rows.iloc[0]["Url"]
            # Read the GeoJSON file from the URL
            df2 = pd.read_json(url, lines=True)
            # Debug print statement - can be removed in production
            # print(url)
            print(df2)

            # Convert geometry data to Shapely shapes
            df2["geometry"] = df2["geometry"].apply(shapely.geometry.shape)

            # Create a GeoDataFrame from the data
            gdf = gpd.GeoDataFrame(df2, crs=4326)
            print(gdf)

            # Define the file name for the temporary file
            fn = os.path.join(tmpdir, f"{quad_key}.geojson")
            tmp_fns.append(fn)

            # Write the GeoDataFrame to a GeoJSON file if it doesn't exist
            if not os.path.exists(fn):
                gdf.to_file(fn, driver="GeoJSON")
        # If multiple rows are found for a quad key, raise an error
        elif rows.shape[0] > 1:
            raise ValueError(f"Multiple rows found for QuadKey: {quad_key}")
        # If no rows are found for a quad key, raise an error
        else:
            raise ValueError(f"QuadKey not found in dataset: {quad_key}")

    # Iterate over each temporary file
    for fn in tmp_fns:
        with fiona.open(fn, "r") as f:
            # Read each row in the file
            for row in tqdm(f):
                row = dict(row)
                shape = shapely.geometry.shape(row["geometry"])

                # Check if the shape is within the area of interest
                if aoi_shape.contains(shape):
                    # Remove the 'id' key if it exists
                    if "id" in row:
                        del row["id"]
                    # Add a new 'id' property
                    row["properties"] = {"id": idx}
                    idx += 1
                    # Add the row to the combined rows list
                    combined_rows.append(row)

    # Debug print statement - can be removed in production
    # print(combined_rows)

# Define the schema for the output file
schema = {"geometry": "Polygon", "properties": {"id": "int"}}

# Write the combined rows to the output file
with fiona.open(output_fn, "w", driver="GeoJSON", crs="EPSG:4326", schema=schema) as f:
    f.writerecords(combined_rows)



# # get_centroid: take geometry of building footprint and compute the centroid coordinate
# def get_centroid(gdf):
#     gdf['centroid'] = gdf.geometry.centroid
#     print(gdf)

# # get_centroid(weather)
# building = gpd.read_file(input_file_from_data_dir("seattle_building_footprints.geojson"))
# get_centroid(building)