import sys
import rasterio
import numpy as np 
import matplotlib.pyplot as plt

dsm_file = 'LiDAR/DSM/NT16NE_50CM_DSM_PHASE3.tif'
dtm_file = 'LiDAR/DTM/NT16NE_50CM_DTM_PHASE3.tif'

with rasterio.open(dsm_file) as src_dsm, rasterio.open(dtm_file) as src_dtm:
    dsm = src_dsm.read(1)
    dtm = src_dtm.read(1)

height_map = dsm-dtm

# Set up figure and axes for DTM visualization
plt.figure(figsize=(8, 8))
plt.imshow(dtm, cmap='terrain', extent=src_dtm.bounds, origin='upper')
plt.colorbar(label='Elevation (meters)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Digital Terrain Model (DTM)')
plt.show()

# Set up figure and axes for DSM visualization
plt.figure(figsize=(8, 8))
plt.imshow(dsm, cmap='terrain', extent=src_dsm.bounds, origin='upper')
plt.colorbar(label='Elevation (meters)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Digital Surface Model (DSM)')
plt.show()


plt.figure(figsize=(8,8))

cmap = plt.get_cmap('gray')

# Display the height map as an image
plt.imshow(height_map, cmap=cmap, extent=src_dsm.bounds, origin='upper')

# Add a color bar for reference
plt.colorbar(label='Elevation (meters)')

# Set labels for the X and Y axes
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Set a title for the plot
plt.title('Height Map (DSM - DTM)')

# Show the plot
plt.show()