
import json
import os
import requests

from dotenv import load_dotenv
from bs4 import BeautifulSoup

PosterPath = "https://image.tmdb.org/t/p/original/"
folder_name = "website"

def api_movie():
    #api for finding movies playing in region united states
    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1&region=US"

    #get api key
    load_dotenv()
    api_key = os.getenv('API_KEY')

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    response = requests.get(url, headers=headers)
    theatreMovies = json.loads(response.text)

    return theatreMovies["results"]


# Press the green button in the gutter to run the script.
def build_poster_site(theatreMovies):
    file_name = 'index.html'
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


    for movie in theatreMovies:
        posterSite += "<a href=" + str(movie["id"]) + ".html""><img src=" + PosterPath + movie["poster_path"] + "alt=\"Description of image\" class=\"responsive-image\"></a>"

    posterSite += "</body></html>"

    file_path = os.path.join(folder_name, file_name)
    with open(file_path, 'w') as file:
        file.write(posterSite)

    print(f'Text has been saved to {file_path}')


def build_individual_site(theatreMovies):
    api_key_omdb = os.getenv('API_KEY_OMDB')
    for movie in theatreMovies:
        file_name = str(movie["id"]) + ".html"
        #Api for more movie info and review info
        #movie["original_title"]
        r = requests.get('http://www.omdbapi.com/?t=' + movie["title"] + '&apikey=' + api_key_omdb)

        # Parsing the HTML
        omdb = json.loads(r.text)

        #Api for trailers
        q = requests.get('https://api.kinocheck.de/movies?tmdb_id=' + str(movie["id"]) + '&categories=Trailer')

        # Parsing the HTML
        kinoTrailers = json.loads(q.text)

        individualSite = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="files/individualStyle.css">
        </head>"""

        #Background image
        try:
            individualSite += """<body> <img class="bg" src=""" + PosterPath + movie["backdrop_path"] + """>"""
        except:
            print("Error on backdrop for :" + movie["title"])
            individualSite += "<body style=\"background-color:black\">"


        individualSite += "<title>" + movie["title"] + "</title>"

        individualSite += """<header><a href="index.html" class="home-button"><img style="height: 28px;" src="files/homeIcon.svg"></a> <button id=\"openModalBtn\" class=\"trailer-button\"><img style=\"height: 28px;\" src=\"files/trailerIcon.svg\"></a></button><button id=\"toggleButton\" class=\"toggle-button\"><img style=\"height: 28px;\" src=\"files/showinfo.svg\"></button></header>"""

        individualSite += "<div id=\"page-wrap\"><h1>" + movie["title"]

        try:
            individualSite += "<span class=\"inline-text\">" + omdb["Genre"] + "</span></h1>"
        except:
            individualSite += "</h1>"
            print("Error on Genre for : " + movie["title"])


        try:
            individualSite += "<p style=\"text-indent: 40px;margin: -34px 0 0 0;\">" + "Rated: " + omdb[
                "Rated"] + " | Runtime: " + omdb["Runtime"] + "</p>"
        except:
            print("Error on Rated or Runtime for : " + movie["title"])

        ##add overview paragraph
        individualSite += "<p>" + movie["overview"] + "</p>"
        try:
            individualSite += "<p style=\"text-indent: 0px;margin: 0 0 0 0;\">" + "Directed By: " + omdb[
                "Director"] + " | Written By: " + omdb["Writer"] + "</p>"
        except:
            print("Error on Director or Writer for : " + movie["title"])
        try:
            rating = omdb["Ratings"]
            individualSite += "<hr></hr>"
            for k in rating:
                individualSite += "<p style=\"text-indent: 0px;margin: 0 0 0 0;\">" + k["Source"] + ": " + k[
                    "Value"] + "</p>"
        except:
            individualSite += "<p> No Review information found for " + movie["title"] + "</p>"
            print("Error on Ratings for: " + movie["title"])

        try:
            youtubeLink = "https://www.youtube.com/embed/" + kinoTrailers['trailer']['youtube_video_id']
            individualSite += "<div class=\"center\">"
        except:
            youtubeLink = ""
            print("Error on youtube link for : " + movie["title"])

        individualSite += """</div></div>
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
            <p id=\"youtubelinksrc\"  style="display: none;">""" + youtubeLink + "</p> <script src=\"files/movieScript.js\"></script></body></html>"
        file_path = os.path.join(folder_name, file_name)
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(individualSite)
        except:
            print("Error for file_path : " + movie["title"])

if __name__ == '__main__':
    # Check if the folder exists, if not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    movies_json = api_movie()
    build_poster_site(movies_json)
    build_individual_site(movies_json)
