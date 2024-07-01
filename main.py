# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os
import requests
from bs4 import BeautifulSoup

PosterPath = "https://image.tmdb.org/t/p/original/"
folder_name = "website"

def api_movie():
    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1&region=US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NDgyYTkyMWNjMjYzYzZjMzk1M2M1ODZjMmVlMjk3NiIsInN1YiI6IjY2NzViZTViZGU3MmZkMzI3N2IwNTE1NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.i8wBqG0YsocvY_pqpD0BEJQtFguFFGFPk21x-1-aghU"
    }

    response = requests.get(url, headers=headers)
    y = json.loads(response.text)
    # AmtNearbyMovies = len(y["results"])
    # for x in y["results"]:
    #     print(x["original_title"])
    #     print("Poster = " + PosterPath + x["poster_path"])
    #     print("Backdrop = " + PosterPath + x["backdrop_path"])
    #     print(x["overview"])
    return y["results"]


# Press the green button in the gutter to run the script.
def build_poster_site(j):
    # Text to save
    posterSite = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Posters</title>
    <style>
        .responsive-image {
            width: 24.5vw; /* 25% of the viewport width */
            height: auto; /* Adjust height automatically to maintain aspect ratio */
        }
        @media screen and (max-width: 1024px) { /* Specific to this particular image */
            .responsive-image {
                width: 23.8vw; /* 25% of the viewport width */
                height: auto; /* Adjust height automatically to maintain aspect ratio */
            }
        }
    </style>
</head>
<body style="background:black;">"""

    # File path to save the text file
    file_name = 'index.html'

    # Open the file in write mode and save the text
    for x in j:
        posterSite += "<a href=" + str(x["id"]) + ".html""><img src=" + PosterPath + x[
            "poster_path"] + """alt="Description of image" class="responsive-image"></a>"""

    posterSite += "</body></html>"
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, 'w') as file:
        file.write(posterSite)

    print(f'Text has been saved to {file_path}')


def build_individual_site(j):
    for x in j:
        r = requests.get('http://www.omdbapi.com/?t=' + x["original_title"] + '&apikey=1a8842a0')

        # Parsing the HTML
        y = json.loads(r.text)

        q = requests.get('https://api.kinocheck.de/movies?tmdb_id=' + str(x["id"]) + '&categories=Trailer')

        # Parsing the HTML
        z = json.loads(q.text)

        individualSite = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="files/individualStyle.css">
        </head>
        <body style="background-image: url(""" + PosterPath + x["backdrop_path"] + """);">"""

        # File path to save the text file
        individualSite += "<title>" + x["original_title"] + "</title>"
        file_name = str(x["id"]) + ".html"
        individualSite += """        <img class="bg" src=""" + PosterPath + x["backdrop_path"] + """>"""
        individualSite += """<header><a href="index.html" class="home-button"><img style="height: 28px;" src="files/homeIcon.svg"></a> <button id=\"openModalBtn\" class=\"trailer-button\"><img style=\"height: 28px;\" src=\"files/trailerIcon.svg\"></a></button><button id=\"toggleButton\" class=\"toggle-button\"><img style=\"height: 28px;\" src=\"files/showinfo.svg\"></button></header>"""
        individualSite += "<div id=\"page-wrap\"><h1>" + x["original_title"]

        try:
            individualSite += "<span class=\"inline-text\">" + y["Genre"] + "</span></h1>"
        except:
            print("Error on Genre for : " + x["original_title"])
        individualSite += "</h1>"

        try:
            individualSite += "<p style=\"text-indent: 40px;margin: -34px 0 0 0;\">" + "Rated: " + y[
                "Rated"] + " | Runtime: " + y["Runtime"] + "</p>"
        except:
            print("Error on Rated or Runtime for : " + x["original_title"])

        ##add overview paragraph
        individualSite += "<p>" + x["overview"] + "</p>"
        try:
            individualSite += "<p style=\"text-indent: 0px;margin: 0 0 0 0;\">" + "Directed By: " + y[
                "Director"] + " | Written By: " + y["Writer"] + "</p>"

        except:
            print("Error on Director or Writer for : " + x["original_title"])
        try:
            rating = y["Ratings"]
            individualSite += "<hr></hr>"
            for k in rating:
                individualSite += "<p style=\"text-indent: 0px;margin: 0 0 0 0;\">" + k["Source"] + ": " + k[
                    "Value"] + "</p>"
        except:
            individualSite += "<p> No Review information found for " + x["original_title"] + "</p>"
            print("Error on Ratings for: " + x["original_title"])

        try:
            youtubeLink = "https://www.youtube.com/embed/" + z['trailer']['youtube_video_id']
            individualSite += """ <div class="center">"""
        except:
            youtubeLink = ""
            print("Error on youtube link for : " + x["original_title"])

        individualSite += """</div>            </div>
            <!-- The Modal -->
            <div id="videoModal" class="modal" >
                <!-- Modal content -->
                <div class="modal-content">
                    <span class="close"></span>
                    <div class="video-container">
                        <iframe id="youtubeVideo" width="100%" height="100%" src="" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                    </div>
                </div>
            </div>
            <p id=\"youtubelinksrc\"  style="display: none;">""" + youtubeLink + "<p> <script src=\"files/movieScript.js\"></script></body></html>"
        file_path = os.path.join(folder_name, file_name)
        try:

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(individualSite)
        except:
            print("Error for file_path : " + x["original_title"])


if __name__ == '__main__':

    # Check if the folder exists, if not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    jason = api_movie()
    build_poster_site(jason)
    build_individual_site(jason)
