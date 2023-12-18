from pathlib import Path
import json
import get_img
import get_taxomony
import post_content
import post_img
import scrapper

def launch():
    exitor = False
    description = """
        Choose an option:
        1. Webscrap all data from the original website 
        2. Get all taxonomy IDs from the website 
        3. Get all images from the website 
        4. Upload all images to the website 
        5. Upload all content from the website 
        Q. Exit
    """
    p = Path(__file__).parent  # get the parent directory of this file
    
    while not exitor:
        keyinput = input(description)
        match keyinput:
            case "1":
                print("1. Webscrap all data from the original website...")
                url_to_scrap = "https://dataviz.pacificdata.org/challenge-2023.html"
                output_json = p / "output_json"
                output_img = p / "output_img"
                scrapper.to_scrap(url_to_scrap, output_json, output_img)
            case "2":
                print("2. Get all taxonomy IDs from the website...")
                drupal_base_url = "http://pdv2:8080"
                taxonomy_names = ["challenge_edition", "challenge_category"]
                jsonpath = p / "output_json"
                get_taxomony.get_taxonomy_ids(jsonpath, drupal_base_url, taxonomy_names)
            case "3":
                print("3. Get all images from the website...")
                drupal_base_url = "http://pdv2:8080"
                jsonpath = p / "output_json"
                pathtoimgs = p / "output_img"
                get_img.get_imgs_ids(jsonpath, drupal_base_url, pathtoimgs)
            case "4":
                print("4. Upload all images to the website...")
                path_to_img = p / 'output_img' # get the path to the images
                path_to_imgfield = "http://pdv2:8080/jsonapi/node/dataviz/field_dataviz_img/"
                output_json = p / "output_json"
                post_img.upload(path_to_img, path_to_imgfield, output_json)
            case "5":
                print("5. Create all content to the website...")
                api_endpoint = "http://pdv2:8080/jsonapi/node/dataviz"
                # get all the data from the json file
                datavizpath = p / "output_json" / "dataviz.json"
                imagepath = p / "output_json" / "id_image.json"
                taxonomypath = p / "output_json" / "id_taxonomy.json"
                with open(imagepath, "r", encoding="utf-8") as json_file:
                    imagedata = json.load(json_file)
                with open(taxonomypath, "r", encoding="utf-8") as json_file:
                    taxonomydata = json.load(json_file)
                with open(datavizpath, "r", encoding="utf-8") as json_file:
                    datavizdata = json.load(json_file)
                    for dataviz in datavizdata.items(): # iterate over the dictionary items
                        post_content.upload_content(api_endpoint, dataviz[1], imagedata, taxonomydata) # dataviz[1] is the dictionary of the dataviz, dataviz[0] is the key of the dictionary, Dataviz 1, Dataviz 2, etc.
            case "Q":
                exitor = True
            case _: # default
                print("Please choose a valid option")
            
if __name__ == "__main__":
    launch()