import requests
import json
from pathlib import Path

def get_imgs_ids(jsonpath:Path, base_url:str, path_to_imgs:Path):
    """
    Retrieve image IDs for all images in the specified directory and store them in a JSON file.

    Args:
        jsonpath (Path): The file path to store the image IDs in JSON format.
        base_url (str): The Drupal 10 base URL.
        path_to_imgs (Path): The directory path containing images.

    Returns:
        dict or None: A dictionary containing image names and their corresponding IDs if successful, 
                     or None if there was an error during the process.
    """
    # get all images in the directory 
    image_names = list(path_to_imgs.iterdir())
    
    all_ids = {}
    # search for all image names
    for image in image_names:
        image_fullname = image.name
        print(f"image name: {image}")
        # Construct the JSON:API endpoint URL
        endpoint_url = f"{base_url}/jsonapi/file/file"

        # Make a GET request to the JSON:API endpoint
        response = requests.get(endpoint_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract image IDs from the response using a loop
            for item in data.get('data', []):
                name_image = item['attributes']['filename']
                if name_image == image_fullname: # we must compare the name of the image with the name of the file to get the ID
                    id_image = item['id']
                    all_ids[name_image] = id_image
                    print(f"GET {name_image}, ID: {id_image}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    
    # write in a json file
    jsonpathname = jsonpath / "id_image.json"
    with open(jsonpathname, "w", encoding="utf-8") as json_file:
        json.dump(all_ids, json_file, ensure_ascii=False, indent=4)
    
    return all_ids


# pathlib
p = Path(__file__).parent  # get the parent directory of this file

if __name__ == "__main__":
    # Set your Drupal 10 base URL and image name
    drupal_base_url = "http://pdv2:8080"
    image_dir = p / "output_img"
    jsonpath = p / "output_json"
    
    # Get image IDs using the function
    image_ids = get_imgs_ids(jsonpath, drupal_base_url, image_dir)

    # Print the result
    if image_ids:
        print(f"Images IDs written in json file: {image_ids}")
    else:
        print("Failed to retrieve Image IDs.")
