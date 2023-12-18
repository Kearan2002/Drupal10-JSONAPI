import requests
import json
from pathlib import Path

def get_taxonomy_ids(jsonpath:Path, base_url:str, taxonomy_names:list):
    """
    Retrieves taxonomy IDs for the specified taxonomy names and stores them in a JSON file.

    Args:
        jsonpath (Path): The file path to store the taxonomy IDs in JSON format.
        base_url (str): The Drupal 10 base URL.
        taxonomy_names (list): A list of taxonomy names.

    Returns:
        dict or None: A dictionary containing taxonomy names and their corresponding IDs if successful, 
                     or None if there was an error during the process.
    """
    all_ids = {}
    # search for all taxonomy names
    for taxonomy in taxonomy_names:
        print(f"\nTaxonomy name: {taxonomy}")
        # Construct the JSON:API endpoint URL
        endpoint_url = f"{base_url}/jsonapi/taxonomy_term/{taxonomy}"

        # Make a GET request to the JSON:API endpoint
        response = requests.get(endpoint_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # create a dictionary with taxonomy name as key
            all_ids[taxonomy] = {}

            # Extract taxonomy IDs from the response using a loop
            for item in data.get('data', []):
                name_taxomony = item['attributes']['name']
                id_taxonomy = item['id']
                all_ids[taxonomy][name_taxomony] = id_taxonomy
                print(f"Taxonomy name: {name_taxomony}, ID: {id_taxonomy}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    
    # write in a json file
    jsonpathname = jsonpath / "id_taxonomy.json"
    with open(jsonpathname, "w", encoding="utf-8") as json_file:
        json.dump(all_ids, json_file, ensure_ascii=False, indent=4)
    
    return all_ids


# pathlib
p = Path(__file__).parent  # get the parent directory of this file


if __name__ == "__main__":
    # Set your Drupal 10 base URL and taxonomy name
    drupal_base_url = "http://pdv2:8080"
    taxonomy_names = ["challenge_edition", "challenge_category"]
    jsonpath = p / "output_json"
    
    # Get taxonomy IDs using the function
    taxonomy_ids = get_taxonomy_ids(jsonpath, drupal_base_url, taxonomy_names)

    # Print the result
    if taxonomy_ids:
        print(f"Taxonomy IDs written in json file: {taxonomy_ids}")
    else:
        print("Failed to retrieve taxonomy IDs.")
