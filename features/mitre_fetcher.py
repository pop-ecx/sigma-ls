"""
Fetch MITRE tags locally 
"""
import os
import json

# Load the MITRE ATT&CK data from the JSON file
def load_mitre_attack_data():
    """
    load json data
    """
    base_dir = os.path.dirname(__file__)
    mitre_file_path = os.path.join(base_dir, 'mitre_attack.json')
    with open(mitre_file_path, "r") as f:
        return json.load(f)

def search_mitre(params):
    """
    Handle a custom request to search for MITRE ATT&CK tags by keyword.
    
    Args:
        params: Contains the 'keyword' for the search. Can be a dict or an object with attributes.
        
    Returns:
        dict: Matching MITRE ATT&CK tags and descriptions or an error message.
    """
    # Extract the 'keyword' based on the type of params
    if isinstance(params, dict):
        keyword = params.get("keyword", "").lower()
    elif hasattr(params, "keyword"):  # For objects with an attribute 'keyword'
        keyword = getattr(params, "keyword", "").lower()
    else:
        return {"error": "Invalid parameters format. 'keyword' is missing."}

    if not keyword:
        return {"error": "No keyword provided for search."}

    mitre_data = load_mitre_attack_data()

    matching_entries = [
        {"tag": entry["tag"], "description": entry["description"]}
        for entry in mitre_data
        if keyword in entry["name"].lower() or keyword in entry["description"].lower()
    ]

    if matching_entries:
        return {"matches": matching_entries}
    return {"error": f"No matches found for keyword: {keyword}"}
