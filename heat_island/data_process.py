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
    This function is designed for the 'weather_<location>.csv' file. 

    It: 
    1. removes any rows that lack temperature data,
    2. eliminates duplicates based on the 'Station ID' column,
    3. drop the 'Note' column.

    Example usage:
    preprocess_csv('weather_Seattle.csv')
    """
  
    # Construct the file path
    input_file_path = input_file_from_data_dir(input_file_name)

    # Load the CSV file into a dataframe
    df = pd.read_csv(input_file_path)
    print(df) # print original dataframe

    # Drop the rows where temprature is missing
    df = df.dropna(subset=['Ave temp annual_F'])

    # Drop duplicates based on the 'Station ID' column
    # This will keep only the first occurrence of each unique ID
    df = df.drop_duplicates(subset=['Station ID'])

    # Drop the 'Note' column
    df = df.drop(columns=['Note'])
    print(df) # print the modified dataframe

    # Construct the output file path to save in the same directory as input file
    output_file_name = 'processed_' + input_file_name
    output_file_path = os.path.join(os.path.dirname(input_file_path), output_file_name)
    
    # Save the processed DataFrame back to CSV
    df.to_csv(output_file_path, index=False)

    print(f"Processed file saved as: {output_file_path}")

