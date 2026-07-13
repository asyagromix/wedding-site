import json

# Fix API response duplicate address
with open("api_response.json", "r") as f:
    data = json.load(f)

blocks = data.get("data", {}).get("blocks", [])
for block in blocks:
    if block.get("id") == "DayProgram":
        events = block.get("blocks", {}).get("DP", {}).get("data", {}).get("events", [])
        for ev in events:
            if ev.get("time") == "16:00" and ev.get("title", "").strip() == "Фуршет":
                ev["desc"] = ""

with open("api_response.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Add image replacement to index.html
with open("index.html", "r") as f:
    html = f.read()

img_fix_script = """
    // Fix broken eventrix images
    let images = document.querySelectorAll('img');
    for (let img of images) {
        if (img.src && img.src.includes('eventrix.pro') && img.src.includes('usersFiles')) {
            if (!img.dataset.fixed) {
                img.dataset.fixed = '1';
                if (img.src.includes('inviteMainPhoto')) {
                    img.src = '/og-image.jpg'; // Main photo fallback
                    img.srcset = '';
                } else {
                    img.src = '/3.png'; // Story photo fallback
                    img.srcset = '';
                }
            }
        }
    }
"""

if "Fix broken eventrix images" not in html:
    html = html.replace("// UI Layout Logic", img_fix_script + "\n    // UI Layout Logic")

with open("index.html", "w") as f:
    f.write(html)
