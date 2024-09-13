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

def remove_exact_duplicates(new_df, existing_df):
    """
    Compares each field in the new data with the existing data in the CSV file 
    and returns only the rows that are not exact duplicates.
    """

    if existing_df.empty:
        return new_df  # If there's no existing data, return the new data

    # Convert existing DataFrame rows to a set of tuples for comparison
    existing_tuples = set([tuple(row) for row in existing_df.to_numpy()])

    # Initialize an empty DataFrame with the same columns as the existing one
    df_unique = pd.DataFrame(columns=existing_df.columns)

    # Loop through each row in the new DataFrame
    for i, new_row in new_df.iterrows():
        # Convert the current new_row to a tuple
        new_row_tuple = tuple(new_row)

        # Check if the row already exists in the existing DataFrame (as a tuple)
        if new_row_tuple not in existing_tuples:
            # Only concatenate non-empty rows
            if not new_row.isna().all():
                # Concatenate only non-empty rows
                df_unique = pd.concat([df_unique, pd.DataFrame([new_row])], ignore_index=True)

    return df_unique

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
        new_df = create_dataframe(data)
        
        # If the CSV file already exists, load the existing data
        if os.path.exists(csv_file):
            existing_df = pd.read_csv(csv_file)
            
            # Remove duplicates by comparing each field
            non_duplicate_df = remove_exact_duplicates(new_df, existing_df)
            
            if not non_duplicate_df.empty:
                # Append only non-duplicate data
                combined_df = pd.concat([existing_df, non_duplicate_df], ignore_index=True)
                combined_df.to_csv(csv_file, index=False)
                return f"Data updated successfully, {len(non_duplicate_df)} new records added to {csv_file}"
            else:
                return "No new data to add, all records are duplicates."
        else:
            # If the CSV file doesn't exist, save the new data
            new_df.to_csv(csv_file, index=False)
            return f"Data saved to new file {csv_file}"

    else:
        return f"No data available for the selected date"
