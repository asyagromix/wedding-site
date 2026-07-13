import json

# Update data.json
with open("api/data.json", "r") as f:
    api_response = json.load(f)

for b in api_response["data"]["blocks"]:
    if b["id"] == "Intro":
        if "photo" in b["blocks"]:
            b["blocks"]["photo"]["data"] = ["/photo1.jpg"]
    elif b["id"] == "LStory":
        if "photo" in b["blocks"]:
            b["blocks"]["photo"]["data"] = ["/photo2.jpg"]
    elif b["id"] == "Final":
        if "photos" in b["blocks"]:
            b["blocks"]["photos"]["data"] = ["/photo3.jpg"]

with open("api/data.json", "w") as f:
    json.dump(api_response, f, ensure_ascii=False)

print("Updated data.json photos!")
