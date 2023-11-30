# Installation
## Overview
The purpose of this markdown is to guide on how to install relevant package that might be used in the project. Some libraries are hard to install due to their conflicted dependency. I would recommend consult with professor or TA before continue. 

This is a list of commands that I used to be able to install the most recent version (1.3.9) of `rasterio`. If you install packages out of this order, you might end up with older version (1.2.10) of `rasterio`. 
>Currently, there is no difference in term of functionality between using 1.2.10 and 1.3.9 version of `rasterio`.

## Create new environment in anaconda
It is recommend that you create new environment in anaconda before performing any installation.

To create new anaconda environment use command below (For me, I use `cse583` as name for my new environment)

```$ conda create --name [name]```

The command below is used to switch from `(base)` environment to new environment `(name)`

```$ conda activate [name]```

## Install `rasterio` package
To get the most recent version of `rasterio`, we have to install the package right away into our new environment using following command line.

```$ conda install -c conda-forge rasterio```

After finish installing `rasterio`, feel free to install other essential package. However, some packages might take longer time to install. For example, it took 5-10 minutes for me to install 4 basic packages that we installed earlier in the course.

`$ conda install numpy scipy pandas matplotlib`

## Install `pyproj` package
This package is used to transform a coordinate system that used in the data into `EPSG:4326` system which is latitude and longitude system. To install this package run the command line below.

```$ conda install -c conda-forge pyproj```
