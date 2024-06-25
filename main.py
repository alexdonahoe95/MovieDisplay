# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os
import requests
from bs4 import BeautifulSoup
PosterPath = "https://image.tmdb.org/t/p/original/"
folder_name = "website"
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def web_scrape(name):
    # Making a GET request
    r = requests.get('https://www.geeksforgeeks.org/python-programming-language/')

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    s = soup.find('div', class_='text')
    content = s.find_all('p')

    print(content)
def api_movie():
    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1&region=US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NDgyYTkyMWNjMjYzYzZjMzk1M2M1ODZjMmVlMjk3NiIsInN1YiI6IjY2NzViZTViZGU3MmZkMzI3N2IwNTE1NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.i8wBqG0YsocvY_pqpD0BEJQtFguFFGFPk21x-1-aghU"
    }

    response = requests.get(url, headers=headers)
    y = json.loads(response.text)
    AmtNearbyMovies = len(y["results"])
    for x in y["results"]:
        print(x["original_title"])
        print("Poster = " + PosterPath + x["poster_path"])
        print("Backdrop = " + PosterPath + x["backdrop_path"])
        print(x["overview"])
    return y["results"]

# Press the green button in the gutter to run the script.
def build_poster_site(j):

    # Text to save
    posterSite = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Image</title>
    <style>
        .responsive-image {
            width: 24.5vw; /* 25% of the viewport width */
            height: auto; /* Adjust height automatically to maintain aspect ratio */
        }
    </style>
</head>
<body style="background:black;">"""

    # File path to save the text file
    file_name = 'index.html'

    # Open the file in write mode and save the text
    for x in j:
        posterSite += "<a href=" + str(x["id"]) + ".html""><img src=" + PosterPath + x["poster_path"] + """alt="Description of image" class="responsive-image"></a>"""

    posterSite += "</body></html>"
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, 'w') as file:
        file.write(posterSite)


    print(f'Text has been saved to {file_path}')
def build_individual_site(j):
    for x in j:
        individualSite = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Responsive Image</title>
            <style>
                .responsive-image {
                    width: 24.5vw; /* 25% of the viewport width */
                    height: auto; /* Adjust height automatically to maintain aspect ratio */
                }
                                img.bg {
                  /* Set rules to fill background */
                  min-height: 100%;
                  min-width: 1024px;

                  /* Set up proportionate scaling */
                  width: 100%;
                  height: auto;

                  /* Set up positioning */
                  position: fixed;
                  top: 0;
                  left: 0;
                }

                @media screen and (max-width: 1024px) { /* Specific to this particular image */
                  img.bg {
                    left: 50%;
                    margin-left: -512px;   /* 50% */
                  }
                }
                #page-wrap {
                  position: relative;
                  width: 400px;
                  border-radius: 25px;
                  /* margin: 50px auto;  */
                  opacity: 0.85;
                  padding: 20px;
                  background: white;
                  -moz-box-shadow: 0 0 20px black;
                  -webkit-box-shadow: 0 0 20px black;
                  box-shadow: 0 0 20px black;
                }
		            p { font: 15px/2 Georgia, Serif;
                  margin: 0 0 30px 0;
                  text-indent: 40px; }
            </style>
        </head>
        <body style="background-image: url(""" + PosterPath + x["backdrop_path"] + """);">"""

        # File path to save the text file
        file_name = str(x["id"]) + ".html"
        individualSite += """        <img class="bg" src=""" + PosterPath + x["backdrop_path"] + """>
        <div id="page-wrap">"""
        individualSite += "<h1>" + x["original_title"] + "</h1><p>" + x["overview"] + "</p>"

        individualSite +="</div></body></html>"
        file_path = os.path.join(folder_name, file_name)
        try:
            with open(file_path, 'w') as file:
                file.write(individualSite)
        except:
            print("error found" + x["original_title"])
            print(file_path)
            print(individualSite)


    print("nothing")
if __name__ == '__main__':
    # Check if the folder exists, if not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    jason = api_movie()
    build_poster_site(jason)
    build_individual_site(jason)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
