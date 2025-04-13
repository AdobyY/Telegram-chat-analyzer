import pandas as pd
import json

def read_json(file):
    """
    Reads a JSON file and normalizes the 'messages' field into a DataFrame.
    
    Args:
        file: A file-like object containing JSON data.
        
    Returns:
        pd.DataFrame: A DataFrame containing the normalized data.
    """
    content = file.read() 
    data = json.loads(content)  
    df = pd.json_normalize(data['messages'])
    return df


