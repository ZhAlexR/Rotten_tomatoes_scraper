import requests


def get_html(set_url, save_to):
    site_url = set_url
    response = requests.get(site_url)
    with open(save_to, "w") as file:
        file.write(response.text)