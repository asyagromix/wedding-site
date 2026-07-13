with open("index.html", "r") as f:
    html = f.read()

import re

# Swap og-image.jpg with 4.png for the main photo, and 3.png for the story
html = html.replace("img.src = '/og-image.jpg';", "img.src = '/4.png';")
html = html.replace("el.style.backgroundImage = 'url(/og-image.jpg)';", "el.style.backgroundImage = 'url(/4.png)';")

with open("index.html", "w") as f:
    f.write(html)
