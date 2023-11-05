# LiDAR Demo
This is my sample code for working DSM, and DTM data as well as visualize the data. I have not checked out LAS file. There are some packages/libraries that we need to install such as `rasterio` and `pyproj`. Please refer to `Installation.md` for additional information.

## Database
I use DSM and DTM data from [Scottish Remote Sensing database](https://remotesensingdata.gov.scot/).
I put bash file for downloading sample data. `NT27SE` is a smaller map with ~50MB, I used for checking for bug. `NT16NE` is a bigger file ~350MB, I used this chunk for visualize. All the pictures below are obtained from `NT16NE`.

## DSM, DTM, Height map
![DSM full map](dsm_full.png)
![DTM full map](dtm_full.png)
![Height map](hmap_full.png)
There are some missing elevation point in DTM map.
![DSM missing point](dsm_missing.png)
![DTM missing point](dtm_missing.png)
![Height map with missing point](hmap_missing.png)
Basic shape of house
![DSM village](dsm_home.png)
![DTM village](dtm_home.png)
![Height map village](hmap_home.png)