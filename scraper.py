import json
import os

import requests
from bs4 import BeautifulSoup

from settings import url, data_dir


def get_html(set_url, save_to):
    site_url = set_url
    response = requests.get(site_url)
    with open(save_to, "w") as file:
        file.write(response.text)


def collect_href(path_to_file):
    with open(path_to_file, "r") as source:
        html_doc = source.read()
    soup = BeautifulSoup(html_doc, "lxml")
    films_href = soup.find(class_="table").find_all("a", class_="unstyled articleLink")

    all_films = {}
    for item in films_href:
        film_name = item.text.strip()
        single_page_href = f"https://www.rottentomatoes.com{item.get('href')}"
        all_films[film_name] = single_page_href

    with open(f"{data_dir}/all_films_list.json", "w") as file:
        json.dump(all_films, file, indent=4, ensure_ascii=False)


def collect_movie_html(path_to_file, html_collection):
    with open(path_to_file, "r") as file:
        all_films_list = json.load(file)
        os.makedirs(html_collection)
    counter = 1
    for film_name, film_href in all_films_list.items():
        request_ = requests.get(film_href)
        response = request_.text

        with open(f"{html_collection}/{film_name}.html", "w") as file:
            file.write(response)
        print(f"HTML for {film_name} was created [{counter}/{len(all_films_list)}]")
        counter += 1


def main():
    # get_html(url, f"{data_dir}/tomato.html")
    # collect_href(f"{data_dir}/tomato.html")
    collect_movie_html(f"{data_dir}/all_films_list.json", f"{data_dir}/html_collect")


if __name__ == "__main__":
    main()
