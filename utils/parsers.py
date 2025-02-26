import requests
import pandas as pd
from io import StringIO

def fetch_weather_data(url):
    """Fetch raw data from the given URL"""
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text

def parse_weather_data(data):
    """Parse the raw text data into structured format"""
    # Split the data into lines
    lines = data.strip().split('\n')
    
    # Find the start of the data table (after metadata)
    start_line = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('year'):
            start_line = i
            break
    
    # Extract the header and data
    header_line = lines[start_line].lower()
    header = [h.strip() for h in header_line.split()]
    
    # Process data lines
    data_lines = lines[start_line+1:]
    processed_data = []
    
    for line in data_lines:
        if not line.strip():
            continue
        
        values = [v.strip() for v in line.split()]
        if len(values) < len(header):
            # Skip incomplete lines
            continue
            
        entry = {header[i]: values[i] for i in range(len(header))}
        print(entry)
        print('====================================================================================================')
        processed_data.append(entry)
    
    return processed_data

def get_weather_data(url):
    """Fetch and parse weather data from the given URL"""
    raw_data = fetch_weather_data(url)
    return parse_weather_data(raw_data)