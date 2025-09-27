# shark_cleaning_functions.py

# Import necessary libraries
import numpy as np
import re

# --- Data Type and Value Cleaning Functions ---

def clean_age(age_value):
    """
    Safely converts an age value to a float.
    Handles potential errors by returning NaN for non-numeric values.
    
    Args:
        age_value: The input value from the 'Age' column.
        
    Returns:
        The age as a float, or np.nan if conversion fails.
    """
    try:
        # Attempt to convert the input value to a float.
        # We use float because it's a flexible numeric type that can represent NaN.
        return float(age_value)
    except (ValueError, TypeError):
        # If the conversion fails (e.g., input is "teen" or None),
        # catch the error and return a standard missing value, np.nan.
        return np.nan

def clean_year_numeric(year_value):
    """
    Safely converts a year value to an integer.
    Handles potential errors by returning NaN for non-numeric or invalid year values.
    
    Args:
        year_value: The input value from the 'Year' column.
        
    Returns:
        The year as an integer, or np.nan if conversion fails.
    """
    try:
        # Attempt to convert the input value to an integer.
        return int(year_value)
    except (ValueError, TypeError):
        # If conversion fails, return np.nan.
        return np.nan

# --- String Extraction Functions using Regular Expressions ---

def extract_year(date_str):
    """
    Extracts the first 4-digit year from a date string using regex.
    
    Args:
        date_str: The string from the 'Date' column.
        
    Returns:
        A string containing the 4-digit year, or None if not found.
    """
    # First, check if the input is actually a string. If not, we can't search it.
    if not isinstance(date_str, str):
        return None
    
    # Define the regular expression pattern.
    # r'\d{4}' means: find a sequence of exactly 4 digits (\d).
    pattern = r'\d{4}'
    
    # Search the string for the first occurrence of the pattern.
    match = re.search(pattern, date_str)
    
    # If a match object is returned, it means the pattern was found.
    if match:
        # The .group(0) method returns the actual text that was matched.
        return match.group(0)
    else:
        # If no match is found, return None.
        return None

def extract_month(date_str):
    """
    Extracts the first 3-letter month abbreviation from a date string.
    
    Args:
        date_str: The string from the 'Date' column.
    
    Returns:
        A string of the 3-letter month, or None if not found.
    """
    # Ensure the input is a string.
    if not isinstance(date_str, str):
        return None
    
    # Convert the string to lowercase to make the search case-insensitive.
    date_str = date_str.lower()
    
    # Define the regex pattern.
    # The '|' character means "OR". This pattern looks for 'jan' OR 'feb' OR 'mar', etc.
    pattern = r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)'
    
    # Search the string for the pattern.
    match = re.search(pattern, date_str)
    
    # If a match is found...
    if match:
        # ...return the matched text.
        return match.group(0)
    else:
        # ...otherwise, return None.
        return None

# --- Categorization Functions ---

def categorize_time(time_str):
    """
    Categorizes a time string into broad periods by checking for patterns.
    """
    if not isinstance(time_str, str):
        return 'unknown'
    
    time_str = time_str.lower()

    # Check for keywords first (added 'midday' and 'late')
    if 'afternoon' in time_str or 'midday' in time_str:
        return 'afternoon'
    elif 'morning' in time_str:
        return 'morning'
    elif 'evening' in time_str or 'dusk' in time_str:
        return 'evening'
    elif 'night' in time_str:
        return 'night'
    
    # Regex: Look for "18h00" OR "1800"
    # The parentheses () create capturing groups for the hour part.
    match = re.search(r'(\d{2})h\d{2}|(\d{2})\d{2}', time_str)
    
    if match:
        # Check which group was captured to get the hour
        # .group(1) captures the digits from the '18h00' pattern
        # .group(2) captures the digits from the '1800' pattern
        # check which one was found to get the hour
        hour_str = match.group(1) if match.group(1) else match.group(2)
        hour = int(hour_str)
        
        # Categorize based on the hour
        if 5 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 17:
            return 'afternoon'
        elif 17 <= hour < 21:
            return 'evening'
        else:
            return 'night'
    else:
        return 'unknown'

# --- Pandas Series Cleaning Functions ---

def clean_country(country_series):
    """
    Cleans a pandas Series of country names.
    This function standardizes names by making them lowercase, removing whitespace,
    and applying a dictionary of corrections.
    
    Args:
        country_series: A pandas Series containing country names.
        
    Returns:
        A cleaned pandas Series with standardized country names.
    """
    # Use the .str accessor in pandas to apply string methods to the entire Series.
    # This is much more efficient than a loop.
    cleaned_series = country_series.str.lower().str.strip()

    # This dictionary maps common misspellings or variations to a standard name.
    country_corrections = {
        "unitedkingdom": "united kingdom", "reunion island": "reunion",
        "srilanka": "sri lanka", "southkorea": "south korea",
        "trinidadandtobago": "trinidad and tobago", "trinidad & tobago": "trinidad and tobago",
        "maldive islands": "maldives", "western samoa": "samoa",
        "saintkittsandnevis": "saint kitts and nevis", "st kitts": "saint kitts and nevis",
        "nevis": "saint kitts and nevis", "st martin": "saint martin",
        "st. martin": "saint martin", "st. maartin": "saint martin",
        "british new guinea": "papua new guinea", "new britain": "papua new guinea",
        "new guinea": "papua new guinea", "admiralty islands": "papua new guinea",
        "netherlands antilles": "curacao", "grand cayman": "cayman islands",
        "andaman": "india", "nicobar islandas": "india", "andaman islands": "india",
        "ceylon (sri lanka)": "sri lanka", "st helena, british overseas territory": "saint helena",
        "san domingo": "dominican republic", "turks & caicos": "turks and caicos",
        "federated states of micronesia": "micronesia", "british isles": "united kingdom",
        "canary islands": "spain", "united arab emirates (uae)": "united arab emirates",
        "british west indies": "west indies", "solomon islands / vanuatu": "solomon islands",
        "equatorial guinea / cameroon": "equatorial guinea", "british overseas territory": "united kingdom",
        "johnston island": "united states minor outlying islands", "palestinian territories": "palestine",
        "french polynesia": "france", "united states minor outlying islands": "usa",
        "british virgin islands": "united kingdom", "between portugal & india": "portugal",
        "american samoa": "usa", "puerto rico": "usa", "guam": "usa",
        "northern mariana islands": "usa", "bermuda": "united kingdom",
        "cayman islands": "united kingdom", "falkland islands": "united kingdom",
        "saint helena": "united kingdom", "reunion": "france", "mayotte": "france",
        "new calledonia": "france", "martinique": "france", "saint martin": "france",
        "curacao": "netherlands", "aruba": "netherlands", "greenland": "denmark",
        "coast of africa": "africa", "west indies": "caribbean", "cook islands": "new zealand",
        "diego garcia": "united kingdom", "asia": "other", "the balkans": "croatia",
        "hong kong": "china", "columbia": "colombia", "burma": "myanmar",
        "ceylon": "sri lanka", "sudan?": "sudan", "andaman / nicobar islandas": "india",
        "england": "united kingdom", "scotland": "united kingdom", "azores": "portugal",
        "okinawa": "japan", "hawaii": "usa", "roatan": "honduras",
        "bahrein": "bahrain", "asia?": "other", "red sea / indian ocean": "indian ocean",
        "red sea?": "indian ocean", "ocean": "other", "trinidad": "trinidad and tobago",
        "tobago": "trinidad and tobago", "st kitts / nevis": "saint kitts and nevis",
        "korea": "south korea", "central pacific": "pacific ocean",
        "mid-pacifc ocean": "pacific ocean", "mid atlantic ocean": "atlantic ocean",
        "indian ocean?": "indian ocean", "red sea": "indian ocean",
        "southwest pacific ocean": "south pacific ocean", "northern arabian sea": "arabian sea",
        "java": "indonesia",
    }
    
    # Use .map() to apply the corrections. If a country isn't in the dictionary, .map() creates a NaN.
    # Use .fillna(cleaned_series) to fill those NaNs with their original (but now cleaned) values.
    # This ensures we only change the names that are in our dictionary.
    corrected_series = cleaned_series.map(country_corrections).fillna(cleaned_series)
    
    return corrected_series

def clean_state(state_series):
    """
    Cleans and standardizes state/province names.
    """
    # Make everything lowercase and remove extra spaces
    cleaned_series = state_series.str.lower().str.strip()

    # Create a dictionary to map abbreviations to full names
    state_corrections = {
        'nsw': 'new south wales',
        'qld': 'queensland',
        'ca': 'california',
        'fl': 'florida'
    }
    
    # Apply the corrections, keeping the original value if no mapping exists
    corrected_series = cleaned_series.map(state_corrections).fillna(cleaned_series)
    
    return corrected_series

def map_continent(country_series):
    """
    Maps a pandas Series of country names to their corresponding continents.
    
    Args:
        country_series: A pandas Series containing cleaned country names.
        
    Returns:
        A pandas Series with continent names.
    """
    # This dictionary maps a country to its continent.
    continent_map = {
        # North America & Caribbean
        "usa": "north america", "canada": "north america", "mexico": "north america",
        "bahamas": "north america", "cuba": "north america", "jamaica": "north america",
        "panama": "north america", "turks and caicos": "north america", "belize": "north america",
        "dominican republic": "north america", "honduras": "north america",
        "nicaragua": "north america", "trinidad and tobago": "north america",
        "barbados": "north america", "grenada": "north america", "el salvador": "north america",
        "haiti": "north america", "antigua": "north america", "caribbean": "north america",
        "guatemala": "north america",
        # South America
        "brazil": "south america", "colombia": "south america", "venezuela": "south america",
        "ecuador": "south america", "chile": "south america", "argentina": "south america",
        "uruguay": "south america", "guyana": "south america", "peru": "south america",
        "paraguay": "south america",
        # Europe
        "france": "europe", "italy": "europe", "united kingdom": "europe",
        "spain": "europe", "croatia": "europe", "greece": "europe",
        "portugal": "europe", "netherlands": "europe", "montenegro": "europe",
        "malta": "europe", "russia": "europe", "norway": "europe",
        "ireland": "europe", "iceland": "europe", "crete": "europe",
        "slovenia": "europe", "monaco": "europe", "cyprus": "europe",
        "denmark": "europe", "sweden": "europe",
        # Africa
        "south africa": "africa", "egypt": "africa", "mozambique": "africa",
        "senegal": "africa", "mauritius": "africa", "kenya": "africa",
        "seychelles": "africa", "sierra leone": "africa", "madagascar": "africa",
        "tanzania": "africa", "somalia": "africa", "libya": "africa",
        "sudan": "africa", "nigeria": "africa", "liberia": "africa",
        "cape verde": "africa", "tunisia": "africa", "guinea": "africa",
        "africa": "africa", "namibia": "africa", "morocco": "africa",
        "comoros": "africa", "angola": "africa", "gabon": "africa",
        "equatorial guinea": "africa", "algeria": "africa", "ghana": "africa",
        "djibouti": "africa",
        # Asia & Middle East
        "india": "asia", "philippines": "asia", "japan": "asia",
        "china": "asia", "iran": "asia", "indonesia": "asia",
        "iraq": "asia", "israel": "asia", "taiwan": "asia",
        "yemen": "asia", "south korea": "asia", "vietnam": "asia",
        "thailand": "asia", "turkey": "asia", "maldives": "asia",
        "singapore": "asia", "saudi arabia": "asia", "malaysia": "asia",
        "myanmar": "asia", "united arab emirates": "asia", "georgia": "asia",
        "syria": "asia", "bangladesh": "asia", "kuwait": "asia",
        "bahrain": "asia", "lebanon": "asia", "jordan": "asia",
        "palestine": "asia",
        # Oceania
        "australia": "oceania", "papua new guinea": "oceania", "new zealand": "oceania",
        "fiji": "oceania", "solomon islands": "oceania", "marshall islands": "oceania",
        "vanuatu": "oceania", "samoa": "oceania", "kiribati": "oceania",
        "palau": "oceania", "micronesia": "oceania", "tuvalu": "oceania",
    }
    
    # Apply the continent map using the same .map().fillna() pattern.
    # If a country isn't in the dictionary, .map() will result in NaN.
    # We then use .fillna() to replace those specific NaNs with the original values from cleaned_series.
    # This ensures we only change names that are in our dictionary.
    continent_series = country_series.map(continent_map).fillna(country_series)
    
    return continent_series

def simplify_species(species_text):
    """
    Categorizes a species string into broader groups by checking for more keywords.
    """
    if not isinstance(species_text, str):
        return 'Unknown'
    
    species_text = species_text.lower()
    
    # Check for the most common and specific types first
    if 'white shark' in species_text:
        return 'White Shark'
    if 'tiger' in species_text:
        return 'Tiger Shark'
    if 'bull' in species_text:
        return 'Bull Shark'
    if 'blacktip' in species_text:
        return 'Blacktip Shark'
    if 'lemon' in species_text:
        return 'Lemon Shark'
    if 'mako' in species_text:
        return 'Mako Shark'
    # --- New keywords added below ---
    if 'nurse' in species_text:
        return 'Nurse Shark'
    if 'hammerhead' in species_text:
        return 'Hammerhead Shark'
    if 'reef' in species_text:
        return 'Reef Shark'
    if 'wobbegong' in species_text:
        return 'Wobbegong Shark'
    if 'unidentified' in species_text or 'questionable' in species_text:
        return 'Unknown'
    # If it just says "shark" but no type, we can classify it as "Unspecified Shark"
    if 'shark' in species_text:
        return 'Unspecified Shark'
        
    return 'Other/Unknown'