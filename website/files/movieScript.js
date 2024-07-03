        // Get the modal
        var modal = document.getElementById("videoModal");

        // Get the button that opens the modal
        var btn = document.getElementById("openModalBtn");

        // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("close")[0];

        // Get the YouTube iframe
        var iframe = document.getElementById("youtubeVideo");

        // When the user clicks the button, open the modal
        window.onload = function() {
            if(document.getElementById("youtubelinksrc").textContent == "")
                document.getElementById("openModalBtn").style.backgroundColor = '#8C92AC';

        };
        btn.onclick = function() {

            if(document.getElementById("youtubelinksrc").textContent == ""){
                console.log("No Trailer Found");
            }
            else{
                modal.style.display = "block";
                iframe.src = document.getElementById("youtubelinksrc").textContent + '?autoplay=1'; // Replace VIDEO_ID with your actual video ID
            }
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
        document.getElementById("toggleButton").addEventListener("click", function() {
            var infoDiv = document.getElementById("page-wrap");
            if (infoDiv.style.display === "none") {
                infoDiv.style.display = "block";
                this.innerHTML = '<img style="height: 28px;" src="files/showinfo.svg">';
                document.getElementById("toggleButton").style = "background-color: green";
            } else {
                infoDiv.style.display = "none";
                this.innerHTML = '<img style="height: 28px;" src="files/showinfo.svg">';
                document.getElementById("toggleButton").style = "background-color: red";
            }
        });