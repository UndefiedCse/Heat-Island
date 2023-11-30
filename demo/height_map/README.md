# LiDAR Demo
This is my sample code for working DSM, and DTM data as well as visualize the data. I have not checked out LAS file. There are some packages/libraries that we need to install such as `rasterio` and `pyproj`. Please refer to `Installation.md` for additional information.

## Database
I use DSM and DTM data from [Scottish Remote Sensing database](https://remotesensingdata.gov.scot/).
I put bash file for downloading sample data. `NT27SE` is a smaller map with ~50MB, I used for checking for bug. `NT16NE` is a bigger file ~350MB, I used this chunk for visualize. All the pictures below are obtained from `NT16NE`.

## Performance issue
The coordinate system used in the dataset is not in latitude and longitude. A coordinate transformation is required using `pyproj` package but this process is a bottleneck in this code.

## Datamap with no missing data
If you choose dataset from `phase 5`, there is no missing data. Here is some example from Edinburgh.
![p5 dsm full](pic/dsm_full_p5.png)
![p5 dtm full](pic/dtm_full_p5.png)
![p5 hmap full](pic/hmap_full_p5.png)

Zoom in
![p5 dsm home](pic/dsm_home_p5.png)
![p5 dtm home](pic/dtm_home_p5.png)
![p5 hmap home](pic/hmap_home_p5.png)

## DSM, DTM, Height map
the area is pretty suburban and there is no tall building in the map. Most trees are taller than house in the map.
![DSM full map](pic/dsm_full.png)
![DTM full map](pic/dtm_full.png)
![Height map](pic/hmap_full.png)
There are some missing elevation point in DTM map.
![DSM missing point](pic/dsm_missing.png)
![DTM missing point](pic/dtm_missing.png)
![Height map with missing point](pic/hmap_missing.png)
Basic shape of house
![DSM village](pic/dsm_home.png)
![DTM village](pic/dtm_home.png)
![Height map village](pic/hmap_home.png)