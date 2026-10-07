import http.server
import socketserver
import json
import urllib.request
import urllib.parse
import ssl
import sys
import os

PORT = int(os.environ.get("PORT", 8000))
VK_TOKEN = "vk1.a.GZqjYnIiyHtMKq7UfWz3-SzU5KabyxA40z0cu-FHiQ7_wxHTl5rSXRwm0IcLR2gk0ebpDhmZNsoIcDTIvMAcHJL1EOAJB87HSIjUdqpmdO7_BK2UR5wNfVHI1D2EmcSJs-Q_tolKJI41OwPubAGcyUc5HGcRewdp8kq0fD67OvxsW4PC4ICijUiolvzRZPdluCT1jKsEMn0AbGI3VbPEXQ"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        if self.path == "/link_vk.php":
            try:
                data = json.loads(post_data.decode('utf-8'))
                if data.get('secret_key') == 'super_secret_wedding_key_2024':
                    user_id = data.get('user_id')
                    with open("vk_config.json", "w") as f:
                        json.dump({"user_id": user_id}, f)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success"}).encode())
                    return
            except Exception as e:
                pass
                
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Bad Request")
            return
            
        if self.path == "/submit_form":
            try:
                import datetime
                form_data = json.loads(post_data.decode('utf-8'))
                submitted_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # 1. Сохраняем локально в guest_responses.json
                responses_file = "guest_responses.json"
                existing_responses = []
                if os.path.exists(responses_file):
                    try:
                        with open(responses_file, "r", encoding="utf-8") as rf:
                            existing_responses = json.load(rf)
                    except:
                        existing_responses = []
                
                record = {
                    "submitted_at": submitted_at,
                    "data": form_data
                }
                existing_responses.append(record)
                with open(responses_file, "w", encoding="utf-8") as wf:
                    json.dump(existing_responses, wf, ensure_ascii=False, indent=2)

                # 2. Сохраняем в текстовый файл guest_responses.txt
                labels = {
                    "name": "Имя",
                    "attendance": "Присутствие",
                    "alcohol": "Алкоголь",
                    "dish": "Горячее",
                    "music": "Музыка/Трек"
                }
                with open("guest_responses.txt", "a", encoding="utf-8") as tf:
                    tf.write("\n=== Новая анкета от " + str(submitted_at) + " ===\n")
                    for key, val in form_data.items():
                        lbl = labels.get(key, key)
                        tf.write(f"{lbl}: {val}\n")
                    tf.write("=" * 40 + "\n")
                print(f"[Анкета сохранена локально в {responses_file} и guest_responses.txt]")
                
                # 3. Отправка уведомления в ВКонтакте
                user_id = None
                if os.path.exists("vk_config.json"):
                    try:
                        with open("vk_config.json", "r") as f:
                            conf = json.load(f)
                            user_id = conf.get("user_id")
                    except:
                        pass
                if not user_id:
                    user_id = os.environ.get("VK_CLIENT_ID", "156300398")

                message = "🔔 Новая анкета от гостя! (" + str(submitted_at) + ")\n\n"

                for key, val in form_data.items():
                    if val and str(val).strip():
                        lbl = labels.get(key, key)
                        message += f"• {lbl}: {val}\n"

                if user_id and VK_TOKEN:
                    try:
                        vk_url = "https://api.vk.com/method/messages.send"
                        params = urllib.parse.urlencode({
                            'message': message,
                            'peer_id': user_id,
                            'access_token': VK_TOKEN,
                            'v': '5.131',
                            'random_id': 0
                        })
                        req = urllib.request.Request(f"{vk_url}?{params}")
                        urllib.request.urlopen(req)
                        print(f"[Анкета отправлена в VK пользователю {user_id}]")
                    except Exception as vk_err:
                        print("Ошибка отправки в VK:", vk_err)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode())
                
            except Exception as e:
                print("Ошибка обработки анкеты:", e)
                self.send_response(500)
                self.end_headers()
            return
            
        # For Eventrix proxying
        if self.path.startswith("/api/"):
            print("RECEIVED NATIVE API POST REQUEST:", self.path)
            print("DATA:", post_data.decode('utf-8'))
            
            # Попытаемся отправить эти данные в VK, если это сабмит формы
            if "submit" in self.path or "form" in self.path:
                try:
                    form_data = json.loads(post_data.decode('utf-8'))
                    user_id = os.environ.get("VK_CLIENT_ID", "156300398") # ID клиента по умолчанию
                    
                    if not user_id and os.path.exists("vk_config.json"):
                        try:
                            with open("vk_config.json", "r") as f:
                                conf = json.load(f)
                                if conf.get("user_id"):
                                    user_id = conf.get("user_id")
                        except:
                            pass
                            
                    if user_id:
                        message = "🔔 Новая анкета от гостя (Native)!\n\n"
                        # Eventrix usually sends {"fields": {...}} or similar
                        if "fields" in form_data:
                            for key, val in form_data["fields"].items():
                                if val: message += f"• {key}: {val}\n"
                        else:
                            for key, val in form_data.items():
                                if val: message += f"• {key}: {val}\n"
                                
                        vk_url = "https://api.vk.com/method/messages.send"
                        params = urllib.parse.urlencode({
                            'message': message,
                            'peer_id': user_id,
                            'access_token': VK_TOKEN,
                            'v': '5.131',
                            'random_id': 0
                        })
                        req = urllib.request.Request(f"{vk_url}?{params}")
                        urllib.request.urlopen(req)
                except Exception as e:
                    print("Error forwarding native form to VK:", e)
            
            # Фейковый успешный ответ для внутренней формы Eventrix
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": False, "data": True}).encode())
            return
            
        # Заглушка для любых других POST-запросов (без внешних обращений)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": False, "data": True}).encode())

    def do_GET(self):
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
        
        clean_path = self.path.split('?')[0].lstrip('/')
        if os.path.exists(clean_path):
            self.path = '/' + clean_path
            super().do_GET()
            return

        # Заглушка для аналитики, трекеров и сторонних скриптов
        if any(keyword in self.path for keyword in ['script.js', 'analytics', 'telemetry', 'sentry', 'track']):
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            self.wfile.write(b"// stub")
            return

        self.send_response(404)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"Not Found")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

with ThreadedTCPServer(("", PORT), ProxyHandler) as httpd:
    print(f"Serving at port {PORT} with threads")
    httpd.serve_forever()
