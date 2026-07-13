import json
import re

print("Starting cleanup...")

# 1. Update data.json
with open("api/data.json", "r") as f:
    api_response = json.load(f)

blocks = api_response["data"]["blocks"]

quiz_idx = -1
wishes_idx = -1
for i, b in enumerate(blocks):
    if b["id"] == "Quiz":
        quiz_idx = i
    elif b["id"] == "Wishes":
        wishes_idx = i

# Reorder them if Quiz is before Wishes
if quiz_idx != -1 and wishes_idx != -1 and quiz_idx < wishes_idx:
    quiz_block = blocks.pop(quiz_idx)
    # now wishes is at wishes_idx - 1 (since we popped an earlier element)
    blocks.insert(wishes_idx - 1, quiz_block)
    # Wait, if we pop quiz (index 10), wishes is at 11.
    # After pop, wishes moves to 10.
    # We want wishes to be before quiz.
    # So we should insert quiz AFTER wishes.
    # So we insert at index 11.
    # Wait, let's just build a new list!
    print("Reordered Quiz and Wishes!")
    
# Let's just do it carefully:
new_blocks = []
quiz_block = None
wishes_block = None
for b in blocks:
    if b["id"] == "Quiz":
        quiz_block = b
    elif b["id"] == "Wishes":
        wishes_block = b

if quiz_block and wishes_block:
    for b in blocks:
        if b["id"] == "Quiz":
            new_blocks.append(wishes_block)
            new_blocks.append(quiz_block)
        elif b["id"] == "Wishes":
            pass # already added
        else:
            new_blocks.append(b)
    api_response["data"]["blocks"] = new_blocks
else:
    print("Could not find Quiz or Wishes")

# Update photos
for b in api_response["data"]["blocks"]:
    if b["id"] == "Main":
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

print("Updated data.json")

# 2. Update index.html
with open("index.html", "r") as f:
    html = f.read()

# Remove window.fetch
html = re.sub(r'window\.fetch = async function\(\) \{.*?return origFetch\.apply\(this, arguments\);\n\s*};\n', '', html, flags=re.DOTALL)
html = re.sub(r'const origFetch = window\.fetch;\n', '', html)
html = re.sub(r'const mockedApiData = \{.*?\};\n', '', html)

# Remove setInterval
html = re.sub(r'<script>\s*setInterval\(\(\) => \{.*?\} catch \(e\) \{ \}\n\}, 500\);\n</script>\n', '', html, flags=re.DOTALL)
html = re.sub(r'setInterval\(\(\) => \{.*?try \{.*?\} catch \(e\) \{ \}\n\}, 500\);', '', html, flags=re.DOTALL)

with open("index.html", "w") as f:
    f.write(html)

print("Updated index.html")
