import pandas as pd
import os

def preprocess_csv(input_file_name):
    
    # Get the absolute path to the directory where data_process.py is located
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the file path for weather_Seattle.csv inside the 'data' subdirectory
    input_file_path = os.path.join(current_directory, '..', 'data', input_file_name)

    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_file_path)

    # Drop the rows where temprature is missing
    df = df.dropna(subset=['Ave temp annual_F'])

    # Drop duplicates based on the 'ID' column
    # This will keep only the first occurrence of each unique ID
    df = df.drop_duplicates(subset=['Station ID'])

    # Construct the output file path to save in the same directory as input file
    output_file_name = 'processed_' + input_file_name
    output_file_path = os.path.join(os.path.dirname(input_file_path), output_file_name)
    
    # Save the processed DataFrame back to CSV
    df.to_csv(output_file_path, index=False)

    print(f"Processed file saved as: {output_file_path}")

'''
# Example usage
preprocess_csv('weather_Seattle.csv')
'''