import re

with open("server.py", "r") as f:
    code = f.read()

new_do_GET = """    def do_GET(self):
        if self.path == "/" or (not "." in self.path.split("/")[-1] and not self.path.startswith("/api/")):
            self.path = "/index.html"
            super().do_GET()
            return
            
        if self.path.startswith("/api/invites/get/byURL"):
            try:
                import json
                with open("api_response.json", "r") as f:
                    data = json.load(f)
                    
                if "data" in data:
                    data["data"]["purchased"] = True
                    data["data"]["published"] = True
                    
                    if "blocks" in data["data"]:
                        blocks = data["data"]["blocks"]
                        wishes_idx = next((i for i, b in enumerate(blocks) if b.get("id") == "Wishes"), -1)
                        if wishes_idx != -1:
                            w_block = blocks.pop(wishes_idx)
                            d_idx = next((i for i, b in enumerate(blocks) if b.get("id") == "DressCode"), -1)
                            if d_idx != -1:
                                blocks.insert(d_idx + 1, w_block)
                        
                        for block in blocks:
                            if block.get("id") == "Place":
                                if "address" in block.get("blocks", {}):
                                    block["blocks"]["address"]["data"] = "ул. Карла Маркса, 23, Киров, Кировская обл.,"
                                if "time" in block.get("blocks", {}):
                                    block["blocks"]["time"]["data"] = "14:00"
                            elif block.get("id") == "Map":
                                if "map" in block.get("blocks", {}) and "data" in block["blocks"]["map"] and "d" in block["blocks"]["map"]["data"]:
                                    block["blocks"]["map"]["data"]["d"]["address"] = "ул. Карла Маркса, 23, Киров, Кировская обл.,"
                                    block["blocks"]["map"]["data"]["d"]["coords"] = "58.6137, 49.6662"
                            elif block.get("id") == "Program":
                                if "PR" in block.get("blocks", {}) and "data" in block["blocks"]["PR"] and "items" in block["blocks"]["PR"]["data"]:
                                    for item in block["blocks"]["PR"]["data"]["items"]:
                                        if item.get("time") == "16:00" and "Фуршет" in item.get("title", ""):
                                            item["desc"] = "Октябрьский пр., 49"
                            elif block.get("id") == "Contacts":
                                if "cts" in block.get("blocks", {}) and "data" in block["blocks"]["cts"] and "cts" in block["blocks"]["cts"]["data"]:
                                    for ct in block["blocks"]["cts"]["data"]["cts"]:
                                        for link in ct.get("links", []):
                                            if link.get("d") == "+7 (912) 333-19-46":
                                                link["d"] = "+7 (912) 331-94-61"
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
            return
            
        import os
        import urllib.request
        import ssl
        
        local_path = self.path.lstrip('/')
        if os.path.exists(local_path):
            super().do_GET()
            return
            
        url = f"https://eventrix.pro{self.path}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        try:
            with urllib.request.urlopen(req, context=ctx) as response:
                content_type = response.headers.get('Content-Type', '')
                body = response.read()
                
                if self.path.endswith(".css"):
                    try:
                        css_text = body.decode('utf-8')
                        css_text = css_text.replace("font-display:swap", "font-display:block").replace("font-display: swap", "font-display: block")
                        body = css_text.encode('utf-8')
                    except:
                        pass
                
                self.send_response(200)
                if content_type:
                    self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(body)
        except Exception as e:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")"""

code = re.sub(r"    def do_GET\(self\):.*?(?=class ThreadedTCPServer)", new_do_GET + "\n\n", code, flags=re.DOTALL)

with open("server.py", "w") as f:
    f.write(code)
