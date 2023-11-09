import rasterio
import numpy as np
import matplotlib.pyplot as plt
import pyproj

# Specify the paths to the DTM and DSM GeoTIFF files
dsm_file = 'demo/data/dsm/NT27SW_50CM_DSM_PHASE5.tif'
dtm_file = 'demo/data/dtm/NT27SW_50CM_DTM_PHASE5.tif'

# Define the EPSG codes for the source (British National Grid) and target (WGS 84 - lat/lon) coordinate systems
source_epsg = 'epsg:27700'
target_epsg = 'epsg:4326'  # WGS 84

# Create a PyProj transformer for the conversion
transformer = pyproj.Transformer.from_crs(source_epsg, target_epsg, always_xy=True)

# Open the DTM and DSM files
with rasterio.open(dtm_file) as src_dtm, rasterio.open(dsm_file) as src_dsm:
    dtm_data = src_dtm.read(1)
    dsm_data = src_dsm.read(1)
    dtm_profile = src_dtm.profile  # Retrieve metadata for the DTM

# Get the transform for converting pixel coordinates to lat/lon
transform = src_dtm.transform

# Calculate the latitudes and longitudes for all pixels
rows, cols = dtm_data.shape
x_coords, y_coords = np.meshgrid(np.arange(cols), np.arange(rows))
x_coords_flat, y_coords_flat = x_coords.flatten(), y_coords.flatten()
x_coords_meters, y_coords_meters = transform * (x_coords_flat, y_coords_flat)
lon_values, lat_values = transformer.transform(x_coords_meters, y_coords_meters)

# Reshape the height map and coordinates for plotting
height_map = dsm_data - dtm_data
lon_values = lon_values.reshape(rows, cols)
lat_values = lat_values.reshape(rows, cols)

# Set outlier values to 0
height_map[(height_map < 0) | (height_map > 1000)] = 0
dtm_data[(dtm_data<0)] =0

# # Plot the height map with latitude and longitude as the X and Y axes
# plt.figure(figsize=(8, 8))
# plt.imshow(height_map, cmap='terrain', extent=[lon_values.min(), lon_values.max(), lat_values.min(), lat_values.max()], origin='upper', vmin=0.)
# plt.colorbar(label='Elevation (meters)')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.title('Height Map (DSM - DTM)')
# plt.show()

# # Plot DSM
# plt.figure(figsize=(8, 8))
# plt.imshow(dsm_data, cmap='terrain', extent=[lon_values.min(), lon_values.max(), lat_values.min(), lat_values.max()], origin='upper', vmin=0.)
# plt.colorbar(label='Elevation (meters)')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.title('Digital Surface Model (DSM)')
# plt.show()

# Plot DTM
plt.figure(figsize=(8, 8))
plt.imshow(dtm_data, cmap='terrain', extent=[lon_values.min(), lon_values.max(), lat_values.min(), lat_values.max()], origin='upper', vmin=0.)
plt.colorbar(label='Elevation (meters)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Digital Terrain Model (DTM)')
plt.show()
