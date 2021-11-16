import csv
import json
import os
import re

import requests
from bs4 import BeautifulSoup

from settings import url, data_dir, headers


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


def collect_data(path_to_folder):
    data_list = []
    for item in os.listdir(path_to_folder):
        with open(f"{path_to_folder}/{item}", "r") as file:
            single_film_html = file.read()
        soup = BeautifulSoup(single_film_html, "lxml")
        movie_name = soup.find("h1", class_="scoreboard__title").text
        movie_info = soup.find("ul", class_="content-meta info").find_all("li")
        data = {"Film": movie_name, }

        for info in movie_info:
            div_item = info.find_all("div")
            clean_label = re.sub(r'^\s+|:|\s+$', '', div_item[0].text)
            if clean_label in headers:
                value = re.sub(r'^\s+|\n|\s+(?= \w)|\s+$', '', div_item[1].text)
                data[clean_label] = value
        data_list.append(data)
    return data_list


def write_data(file_name, data):
    with open(file_name, "w") as file:
        dict_writer = csv.DictWriter(file, fieldnames=headers)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def main():
    # get_html(url, f"{data_dir}/tomato.html")
    # collect_href(f"{data_dir}/tomato.html")
    # collect_movie_html(f"{data_dir}/all_films_list.json", f"{data_dir}/html_collect")
    data = collect_data(f"{data_dir}/html_collect")
    write_data(f"{data_dir}/movie_info.csv", data)


if __name__ == "__main__":
    main()
