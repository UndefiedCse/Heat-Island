# How to use
This is a guide on how to convert `.tif` format into `.csv` in order to be processed in the next step.

Change the `input_path` to your selected file.

The `path` must be relative to where you execute `tif2csv.py`

For example, if you run the file from the repository, `input_path` should be
`'demo/data/dtm/[name].tif'`

For VScode user, you can right click at the file and select `copy relative path` and paste it to the input path

# Output format
The output format is `.csv` file with `lat` for latitude, `lon` for longitude, and `band_{number}` depending on how many band there is since there can be multiple bands.

For Edinburgh example, there is only one band for height so the header of the file is `lat` `lon` and `band_1`

# Warning: Large File size

The csv output is quite large and depend on how big your chunk is. For example, Edinburgh area is around **3.8GB**.

# Next step

I think the next step for this file is that I'll convert this file to python function and put it in our module. Let me know what you think.