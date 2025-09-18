import requests

def get_cat_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [breed["name"] for breed in data]
    return []
