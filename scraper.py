import requests

from settings import url, data_dir


def get_html(set_url, save_to):
    site_url = set_url
    response = requests.get(site_url)
    with open(save_to, "w") as file:
        file.write(response.text)


def main():
    get_html(url, f"{data_dir}/tomato.html")


if __name__ == "__main__":
    main()