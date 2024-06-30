# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os
import requests
from bs4 import BeautifulSoup

PosterPath = "https://image.tmdb.org/t/p/original/"
folder_name = "website"


def web_scrape(name):
    # Making a GET request
    r = requests.get('https://www.geeksforgeeks.org/python-programming-language/')

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    s = soup.find('div', class_='text')
    content = s.find_all('p')

    # print(content)


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
    <title>Movie Display: Posters</title>
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
                .button {
  background-color: #04AA6D; /* Green */
  border: none;
  color: black;
  padding: 16px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  transition-duration: 0.4s;
  cursor: pointer;
  width: 100%;
  border-radius: 10px;
  font-weight: bold;
}


                #page-wrap {
                  position: relative;
                  margin: 50px auto;
                  width: 40%;
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
                  margin: 10px 0 30px 0;
                  }
                  
                  .inline-text {
                    display: inline;
                    margin-left: 10px; /* Adjust the spacing as needed */
                    font: 15px/2 Georgia, Serif;

               }
               /* Modal styles */
.modal {
    display: none; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 1; /* Sit on top */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    background-color: rgb(0,0,0); /* Fallback color */
    background-color: rgba(0,0,0,0.9); /* Black w/ opacity */
}

/* Modal Content */
.modal-content {
    position: relative;
    margin: auto;
    padding: 0;
    width: 80%;
    max-width: 700px; /* Could be more or less, depending on screen size */
    animation: animatetop 0.4s;
    height: 66%;
}

/* Add Animation */
@keyframes animatetop {
    from {top: -300px; opacity: 0}
    to {top: 0; opacity: 1}
}

/* Close button */
.close {
}

.close:hover,
.close:focus {
    color: #000;
    text-decoration: none;
    cursor: pointer;
}

.video-container {
    padding: 20px;
    text-align: center;
    height: 65%;
}
header {
    display: flex;
    align-items: center;
    padding: 10px;
    background-color: #333;
}

.home-button {
    text-decoration: none;
    color: white;
    background-color: white;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
    position: absolute;
    top: 10px;
    left: 10px;
}

.home-button:hover {
    background-color: #0056b3;
}
               @media screen and (max-width: 1024px) { /* Specific to this particular image */
               .modal-content {
                    height:33%
               }
                #page-wrap{
                    width:90%;
                }
                  img.bg {
                    left: 50%;
                    margin-left: -512px;   /* 50% */
                  }
                }
            </style>
        </head>
        <body style="background-image: url(""" + PosterPath + x["backdrop_path"] + """);">"""

        # File path to save the text file
        individualSite += "<title>" + x["original_title"] + "</title>"
        file_name = str(x["id"]) + ".html"
        individualSite += """        <img class="bg" src=""" + PosterPath + x["backdrop_path"] + """>"""
        individualSite += """<header><a href="index.html" class="home-button"><img style="height: 28px;" src="homeIcon.svg"></a></header>"""
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
            individualSite += """    <button id="openModalBtn" class="button">Watch The Trailer</button>"""
        except:
            print("Error on youtube link for : " + x["original_title"])

        individualSite += """</div>
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
        
                <script>
                // Get the modal
        var modal = document.getElementById("videoModal");
        
        // Get the button that opens the modal
        var btn = document.getElementById("openModalBtn");
        
        // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("close")[0];
        
        // Get the YouTube iframe
        var iframe = document.getElementById("youtubeVideo");
        
        // When the user clicks the button, open the modal
        btn.onclick = function() {
            modal.style.display = "block";
            iframe.src = """ + "\"" + youtubeLink + "\"" + """; // Replace VIDEO_ID with your actual video ID
        }
        
        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
            modal.style.display = "none";
            iframe.src = ""; // Stop the video
        }
        
        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
                iframe.src = ""; // Stop the video
            }
        }
            </script></body></html>"""
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
