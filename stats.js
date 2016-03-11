"use strict";
function main () {
    var links = document.getElementById("content").getElementsByTagName("a");
    var links_length = links.length;
    for (var i = 0; i < links_length; i++) {
        links[i].addEventListener("click", function (e) {navigate(e)}, false);
    }
}

function navigate(e) {
    if (document.getElementById("stats")) {
        if (document.getElementById("stats").checked) {
            e.preventDefault();
            window.location = "/l/" + e.srcElement.href.match("\/stats\/(.+)$")[1];
        }
    }
}

if (window.addEventListener) {
    if (document.readyState !== "loading") {
        main();
    } else {
        window.addEventListener("DOMContentLoaded", main, false);
    }
}
