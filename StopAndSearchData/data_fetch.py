import requests
import pandas as pd
import os

def get_stop_and_search_data(force, date):
    url = f"https://data.police.uk/api/stops-force?force={force}&date={date}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def create_dataframe(data):
    """Convert JSON data to a DataFrame, removing 'location' but keeping its nested fields."""
    
    # Normalize the JSON data into a flat table
    df = pd.json_normalize(data)

    # Drop the 'location' column but keep its nested fields
    if 'location' in df.columns:
        df = df.drop(columns=['location'])

    return df

def update_data(force="metropolitan", year="2023", month="01"):
    """Fetches stop and search data for the given force, year, and month."""

    # Combine year and month to form the date parameter
    date = f"{year}-{month}"
    
    # Fetch the data from the API
    data = get_stop_and_search_data(force, date)
    
    # Generate the CSV file name based on the force
    csv_file = f"{force}_stop_search_data.csv"
    
    # Check if data is available
    if data:
        df = create_dataframe(data)
        
        # Save data to CSV file, or append if it already exists
        if os.path.exists(csv_file):
            existing_data = pd.read_csv(csv_file)
            updated_data = pd.concat([existing_data, df], ignore_index=True).drop_duplicates()
            updated_data.to_csv(csv_file, index=False)
        else:
            df.to_csv(csv_file, index=False)
        
        return f"Data updated successfully and saved to {csv_file}"
    else:
        return f"No data available for the selected date"
