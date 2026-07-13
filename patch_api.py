import re

with open("api/index.py", "r") as f:
    content = f.read()

# Add handling for /api/invites/get/byURL in do_POST
new_do_post_logic = """
    def do_POST(self):
        if "/api/invites/get/byURL" in self.path:
            import os
            try:
                base_dir = os.path.dirname(__file__)
                with open(os.path.join(base_dir, 'data.json'), 'rb') as f:
                    json_data = f.read()
            except Exception as e:
                json_data = b'{"error": true}'
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json_data)
            return
            
        content_length = int(self.headers.get('Content-Length', 0))
"""

content = re.sub(r'    def do_POST\(self\):\n        content_length = int\(self\.headers\.get\(\'Content-Length\', 0\)\)', new_do_post_logic, content)

with open("api/index.py", "w") as f:
    f.write(content)
