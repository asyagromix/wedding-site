import json

with open("api/data.json", "r") as f:
    api_response = json.load(f)

for b in api_response["data"]["blocks"]:
    if b["id"] == "Intro" and "photo" in b["blocks"]:
        b["blocks"]["photo"]["data"] = [{
            "type": "inviteMainPhoto",
            "index": "wm-8p76BkHh3En7",
            "origTitle": "IMG_9802.jpeg",
            "keyS3": "usersFiles/inviteMainPhoto/40753_wm-8p76BkHh3En7.jpeg",
            "mimeType": "image/jpeg"
        }]
    elif b["id"] == "LStory" and "photo" in b["blocks"]:
        b["blocks"]["photo"]["data"] = [{
            "type": "invitePhoto",
            "index": "EJ5p0KrBGUH2qFa",
            "origTitle": "IMG_9803.png",
            "keyS3": "usersFiles/invitePhoto/40753_EJ5p0KrBGUH2qFa.png",
            "mimeType": "image/png"
        }]
    elif b["id"] == "Final" and "photos" in b["blocks"]:
        b["blocks"]["photos"]["data"] = [{
            "type": "invitePhoto2x",
            "index": "Nv1jFMJuxThljgC",
            "origTitle": "IMG_9804.png",
            "keyS3": "usersFiles/invitePhoto2x/40753_Nv1jFMJuxThljgC.png",
            "mimeType": "image/png"
        }]

with open("api/data.json", "w") as f:
    json.dump(api_response, f, ensure_ascii=False)

# Now inject the image swapper in index.html safely
with open("index.html", "r") as f:
    html = f.read()

script = """
<script>
(function() {
  const replaceImages = () => {
    document.querySelectorAll('img').forEach(img => {
      if (img.src && img.src.includes('selstorage.ru')) {
        img.removeAttribute('srcset');
        img.removeAttribute('sizes');
        if (img.src.includes('inviteMainPhoto')) img.src = '/photo1.jpg';
        else if (img.src.includes('invitePhoto2x')) img.src = '/photo3.jpg';
        else if (img.src.includes('invitePhoto')) img.src = '/photo2.jpg';
      }
    });
    document.querySelectorAll('*').forEach(el => {
      if (el.style.backgroundImage && el.style.backgroundImage.includes('selstorage.ru')) {
        if (el.style.backgroundImage.includes('inviteMainPhoto')) el.style.backgroundImage = 'url(/photo1.jpg)';
        else if (el.style.backgroundImage.includes('invitePhoto2x')) el.style.backgroundImage = 'url(/photo3.jpg)';
        else if (el.style.backgroundImage.includes('invitePhoto')) el.style.backgroundImage = 'url(/photo2.jpg)';
      }
    });
  };

  const observer = new MutationObserver(() => replaceImages());
  document.addEventListener("DOMContentLoaded", () => {
    observer.observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['src', 'style'] });
    replaceImages();
  });
})();
</script>
"""

# Insert before </head>
html = html.replace("</head>", script + "\n</head>")

with open("index.html", "w") as f:
    f.write(html)
