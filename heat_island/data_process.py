"""
data_process.py: data process functions for heat_island

Functions:
    input_file_from_data_dir(input_file_name): find the targeted file 
        inside the 'data' directory and output input file path.
    preprocess_csv(input_file_name): Drop the rows contains missing 
        temprature data and the duplicates weather station.
"""


import os
import pandas as pd

def input_file_from_data_dir(input_file_name):
    """
    Constructs the absolute file path for a given file located in the 
    'data' directory.

    This function computes the absolute path for a file specified by 
    'input_file_name' that resides in the 'data' directory. The 
    function is useful for consistently locating data files relative 
    to the script's location, making the script more portable and its 
    file references more robust to changes in the working directory.
    
    Parameters:
    input_file_name (str): The name of the file within the 'data' 
    directory. It should include the file extension.

    Returns:
    str(pandas.DataFrame): data frame after process.

    Example usage:
    print(input_file_from_data_dir('weather_Seattle.csv'))
    """
  
    # Get the absolute path to the directory where data_process.py is located
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the file path for any file inside the 'data' directory
    input_file_path = os.path.join(current_directory, '..', 'data', input_file_name)

    return input_file_path


def preprocess_csv(input_file_name):
    """
    Processes a CSV file containing weather data to prepare it for 
    further analysis.

    This function is specifically tailored for 'weather_<location>.csv'
    files. It performs several preprocessing steps on the data: 
    1. removing rows without temperature data, 
    2. eliminating duplicate records based on 'Station ID', and 
    3. dropping the 'Note' column. 
    After processing, the cleaned data is saved as a new CSV file 
    prefixed with 'processed_' in the same directory as the input file.

    Parameters:
    input_file_name (str): The name of the CSV file to process. The 
    file is expected to be in a 'data' directory relative to the 
    script's location.

    Note:
    - This function is designed for the 'weather_<location>.csv' file. 
    - Prints the original and modified dataframes to the console.
    - Saves the processed data to a new CSV file in the same directory 
    as the input file.

    Returns:
    DF: The absolute path of the file within the 'data' directory.

    Example usage:
    preprocess_csv('weather_Seattle.csv')
    """

    # Construct the file path
    input_file_path = input_file_from_data_dir(input_file_name)

    # Load the CSV file into a dataframe
    DF = pd.read_csv(input_file_path)
    # Debug print statement - can be removed in production
    print(DF) # print original dataframe

    # Drop the rows where temprature is missing
    DF = DF.dropna(subset=['Ave temp annual_F'])

    # Drop duplicates based on the 'Station ID' column
    # This will keep only the first occurrence of each unique ID
    DF = DF.drop_duplicates(subset=['Station ID'])

    # Drop the 'Note' column
    DF = DF.drop(columns=['Note'])
    # Debug print statement - can be removed in production
    print(DF) # print the modified dataframe

    # Construct the output file path to save in the same directory as input file
    output_file_name = 'processed_' + input_file_name
    output_file_path = os.path.join(os.path.dirname(input_file_path), output_file_name)

    # Save the processed DataFrame back to CSV
    DF.to_csv(output_file_path, index=False)

    print(f"Processed file saved as: {output_file_path}")

    return DF
