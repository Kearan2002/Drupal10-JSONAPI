import requests
from requests.auth import HTTPBasicAuth
import uuid


def upload_content(api_endpoint:str, data_dataviz:dict, id_imgs:dict, id_taxonomy:dict):
    """Uploads content to a Drupal 10 instance using the JSON:API. Creates a new dataviz node with provided data.

    Args:
        api_endpoint (str): The JSON:API endpoint URL for creating content.
        data_dataviz (dict): Dictionary containing data for the dataviz node.
        id_imgs (dict): Dictionary containing image IDs.
        id_taxonomy (dict): Dictionary containing taxonomy IDs.

    Returns:
        None
    """
    uuid_id = str(uuid.uuid4())  # generate a random uuid
    
    # Configuration des informations d'authentification
    username = 'admin'
    password = 'adm1n'
    
    # relationship with taxonomy
    id_taxonomy_year = id_taxonomy['challenge_edition'][data_dataviz['field_dataviz_year']]
    id_taxonomy_type = id_taxonomy['challenge_category'][data_dataviz['field_dataviz_type']]
    # relationship with image
    id_image_dataviz = id_imgs[data_dataviz['field_dataviz_img']]

    # Données du contenu à créer
    data = {
        'data': {
            'type': 'node--dataviz',
            'id': uuid_id,
            'attributes': {
                'title': data_dataviz['title'],
                'field_dataviz_title': {'value': data_dataviz['field_dataviz_title']},
                'field_dataviz_owner': {'value': data_dataviz['field_dataviz_owner']},
                'field_dataviz_prize': {'value': data_dataviz['field_dataviz_prize']},
                'field_dataviz_rankedprize': {'value': ""},
                'field_dataviz_country': {'value': data_dataviz['field_dataviz_country']},
                'field_dataviz_button': {'uri': data_dataviz['field_dataviz_button'], 'title': 'View Dataviz'},
            },
            'relationships': {
                "field_dataviz_img": {
                    "data": {
                        "type": "file--file",
                        "id": id_image_dataviz,
                    },
                },
                "field_dataviz_type": {
                    "data": {
                        "type": "taxonomy_term--challenge_category",
                        "id": id_taxonomy_type,
                    },
                },
                "field_dataviz_year": {
                    "data": {
                        "type": "taxonomy_term--challenge_edition",
                        "id": id_taxonomy_year,
                    },
                },
            },
        },
    }

    # Envoi de la requête POST pour créer le contenu
    response = requests.post(
        api_endpoint,
        json=data,
        auth=HTTPBasicAuth(username, password),
        headers={'Content-Type': 'application/vnd.api+json'},
        verify=False,
    )

    # Vérification du statut de la requête
    if response.status_code == 201:
        print(f"Création du contenu {data_dataviz['title']} réussie !\n Code de statut: {response.status_code}\n")
    else:
        print('Erreur lors de la création du contenu. Code de statut:', response.status_code)
        print('Réponse:', response.text)


if __name__ == "__main__":
    # Configuration de l'URL de l'API REST de Drupal
    drupal_url = 'http://pdv2:8080'
    pathtocontent = '/jsonapi/node/dataviz'  # Remplacez 'article' par le type de contenu que vous souhaitez créer
    
    api_endpoint = drupal_url + pathtocontent
    upload_content(api_endpoint)