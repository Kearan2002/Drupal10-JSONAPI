import json
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path
from unidecode import unidecode

def upload(path_to_img:Path, path_to_img_field:Path, output_json:Path):
    """
    Uploads images to the specified image field and stores the uploaded image IDs in a JSON file.

    Args:
        path_to_img (Path): The directory path containing images to be uploaded.
        path_to_img_field (str): The JSON:API endpoint for the image field where images will be uploaded.
        output_json (Path): The file path to store the uploaded image IDs in JSON format.

    Returns:
        dict: A dictionary containing image names and their corresponding IDs.
    """

    all_id = {}
    
    # get all img in a list 
    img_list = list(path_to_img.iterdir())
    print(img_list)
    counter_upload = 1
    counter_all_img = len(img_list)

    for img in img_list:
        with open(img, "rb") as file:
            img_name = img.name
            print('Uploading image:', img_name, " - ", counter_upload, "/", counter_all_img)
            
            pst = requests.post(
                path_to_img_field, # you must upload to an image field
                headers={
                    'Accept': 'application/vnd.api+json',        
                    'Content-Type': 'application/octet-stream',
                    'Content-Disposition': f'file; filename="{img_name}"',
                },
                data=file,
                auth=HTTPBasicAuth('admin', 'adm1n'),
                verify=False
            ) 
        # Verification of the response
        if pst.status_code == 201:
            print('Création du contenu réussie ! Code de statut:', pst.status_code)
            # print('Réponse:', pst.json())
            id_image = pst.json()['data']['id']
            all_id[img_name] = id_image  # Convert counter_upload to string
        elif pst.status_code == 500:
            print('Internal Server Error. Code de statut:', pst.status_code)
        else:
            print('Erreur lors de la création du contenu. Code de statut:', pst.status_code)
            # print('Réponse:', pst.text)
        counter_upload += 1
            
    # Save the information to a JSON file
    jsonpathname = output_json / "id_image.json"
    with open(jsonpathname, "w", encoding="utf-8") as json_file:
        json.dump(all_id, json_file, ensure_ascii=False, indent=4)
        
    return all_id


    
p = Path(__file__).parent  # get the parent directory of this file
if __name__ == "__main__":
    path_to_img = p / 'output_img' # get the path to the images
    path_to_imgfield = "http://pdv2:8080/jsonapi/node/dataviz/field_dataviz_img/"
    output_json = p / "output_json"
    
    # USE "Fancy File Delete" Module to delete all images in the image field (after testing)
    print(upload(path_to_img, path_to_imgfield, output_json))