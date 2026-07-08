import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon

#%%-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Geospatial Utilities
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

us_state_to_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL",
    "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", 
    "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", 
    "New Hampshire": "NH", "New Jersey": "NJ","New Mexico": "NM","New York": "NY","North Carolina": "NC","North Dakota": "ND","Ohio": "OH","Oklahoma": "OK", "Oregon": "OR", 
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
    "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC", "American Samoa": "AS", "Guam": "GU", "Northern Mariana Islands": "MP", 
    "Puerto Rico": "PR", "United States Minor Outlying Islands": "UM", "Virgin Islands, U.S.": "VI",
}

def USA_Zip_GEOJSON_Import(state=None):
    
    if state is None:
        raise ValueError("State parameter is required. Please provide a 2-letter state abbreviation or full state name.")

    if len(state) == 2:
        state_abb = state.lower()
        if state_abb.upper() not in us_state_to_abbrev.values():
            raise ValueError(f"Invalid state abbreviation: {state}. Please provide a valid 2-letter state abbreviation.")
        state_name = [name for name, abb in us_state_to_abbrev.items() if abb == state_abb.upper()][0].lower().replace(" ", "_")
    
    elif state.title() in us_state_to_abbrev:
        state_name = state.lower().replace(" ", "_")
        state_abb = us_state_to_abbrev[state.title()].lower()
    
    else:        
        raise ValueError(f"Invalid state name: {state}. Please provide a valid full state name.")        
    
    url = f"https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/refs/heads/master/{state_abb}_{state_name}_zip_codes_geo.min.json"

    try:
        geojson = pd.read_json(url)
        print(f"Successfully imported GeoJSON data for {state.title()}.")
        return url
    
    except Exception as e:
        print(f"Error importing GeoJSON data for {state.title()}: {e}")
        return None
