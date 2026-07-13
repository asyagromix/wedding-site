import re, json

with open("index.html", "r") as f:
    html = f.read()

# Fix JSON data
def replacer(match):
    data = json.loads(match.group(1))
    
    # Recursively find and fix photo paths
    def traverse(obj):
        if isinstance(obj, dict):
            if "fType" in obj and obj["fType"] in ["inviteMainPhoto", "invitePhoto", "invitePhoto2x"]:
                for item in obj.get("data", []):
                    if item.get("type") == "inviteMainPhoto":
                        item["keyS3"] = "photo1.jpg"
                        item["url"] = "/photo1.jpg"
                    elif item.get("type") == "invitePhoto":
                        item["keyS3"] = "photo2.jpg"
                        item["url"] = "/photo2.jpg"
                    elif item.get("type") == "invitePhoto2x":
                        item["keyS3"] = "photo3.jpg"
                        item["url"] = "/photo3.jpg"
            for k, v in obj.items():
                traverse(v)
        elif isinstance(obj, list):
            for v in obj:
                traverse(v)
                
    traverse(data)
    # Also add "url" directly to the object if it exists? The frontend might use keyS3 or url. Let's just set keyS3 to the local file, but the frontend might prepend the bucket url. Wait, if it prepends bucket url, it will still go to selstorage.ru.
    # Actually, Eventrix frontend might hardcode the bucket URL: `https://...selstorage.ru/${keyS3}`.
    # If we set keyS3 to a full URL `https://wedding-site-taupe-eight.vercel.app/photo1.jpg`, it might become `https://...selstorage.ru/https://...` which is invalid.
    return "const mockedApiData = " + json.dumps(data) + ";"

html = re.sub(r"const mockedApiData = (\{.*?\});", replacer, html)

# Remove the replaceImages script block
html = re.sub(r"<script>\s*\(function\(\)\s*\{\s*const replaceImages = \(\) => \{.*?\}\)\(\);\s*</script>", "", html, flags=re.DOTALL)

with open("index.html", "w") as f:
    f.write(html)
print("Fixed index.html!")
