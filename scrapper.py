from bs4 import BeautifulSoup
from pathlib import Path
import requests
import json
from urllib3.exceptions import InsecureRequestWarning
from unidecode import unidecode

def to_scrap(url_to_scrap:str, output_json:Path, output_img:Path):
    """
    Scrapes data from the specified URL, downloads images, and creates entries in JSON format.

    Args:
        url_to_scrap (str): The URL of the page to scrape.
        output_json (Path): The directory path to store the JSON data.
        output_img (Path): The directory path to store downloaded images.

    Returns:
        None
    """
    # Suppress only the InsecureRequestWarning because SPC does need SSL certificate to work on requests (security)
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    # Get the content of the page
    content_page = requests.get(url_to_scrap, verify=False)  # verify=False because SSL certificate is required to request
    soup_page = BeautifulSoup(content_page.content, "html.parser")

    # find the entries in rows
    items = soup_page.find("div", class_="row row-cols-1 row-cols-md-3 row-cols-lg-4").find_all("div", class_="mb-4")
    len_items = len(items)
    counter_items = 1


    # Dictionary instead of a list
    entries = {}  
    for item in items:
        print(str(counter_items) + "/" + str(len_items))
        # Extract information from each entry block
        year = "2023"
        title = item.find("h5", class_="card-title").text.strip()
        text_autor = item.find("p", class_="card-text").text.strip()
        country = item.find("span", class_="badge bg-secondary").text.strip()
        category = item.find("span", class_="badge bg-info").text.strip()
        link_to_dataviz = item.find("a", class_="btn btn-primary")["href"]
        image_url = "https://dataviz.pacificdata.org" + item.find("img")["src"]

        # Download the image
        img_filename = f"{counter_items}_{text_autor}.png" #all the img are png so we dont need to change the extension
        # fix the name of the image
        img_filename = img_filename.lower() # lowercase the string
        img_filename = img_filename.replace(' ', '_') # replace space with underscore
        img_filename = unidecode(img_filename) # normalize the string, remove accents
        # save the image in this path
        image_pathname = output_img / img_filename
        with open(image_pathname, "wb") as image_file: 
            img_data = requests.get(image_url, verify=False)  # get the data from the image, verify False because SSL certificate is required to request
            image_file.write(img_data.content)
            
        # fix the absolute url for link_to_dataviz
        if link_to_dataviz[0] == "/":
            link_to_dataviz = "https://dataviz.pacificdata.org" + link_to_dataviz

        # Create an entry dictionary with "Dataviz x" key
        entries[f"Dataviz {counter_items}"] = {
            "title": f"Dataviz {counter_items}--{year} : {title}",
            "field_dataviz_title": title,
            "field_dataviz_owner": text_autor,
            "field_dataviz_country": country,
            "field_dataviz_button": link_to_dataviz,
            "field_dataviz_prize": False,
            "field_dataviz_rankedprize": "",
            "field_dataviz_type": category,
            "field_dataviz_type_ID": "",
            "field_dataviz_year": year,
            "field_dataviz_year_ID": "",
            "field_dataviz_img": img_filename,
            "field_dataviz_img_alt": f"Image de la dataviz {counter_items}",
            "field_dataviz_img_ID": "",
        }

        print(
            f'title: {title},\n text: {text_autor},\n country: {country},\n category: {category},\n link_to_dataviz: {link_to_dataviz},\n image_filename: {img_filename}, ...\n'
        )
        counter_items += 1

    # Save the information to a JSON file
    json_pathname = output_json / "dataviz.json"
    with open(json_pathname, "w", encoding="utf-8") as json_file:
        json.dump(entries, json_file, ensure_ascii=False, indent=4)

    print("done !")

if __name__ == "__main__":
    # pathlib
    p = Path(__file__).parent
    url_to_scrap = f"https://dataviz.pacificdata.org/challenge-2023.html"
    output_img = p / "output_img"
    output_json = p / "output_json"

    to_scrap(url_to_scrap, output_json, output_img)