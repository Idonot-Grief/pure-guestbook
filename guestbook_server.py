import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

JSON_FILE = r"path/to/your/html/host/root/"
PORT = 8080

# Ensure file exists
try:
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        json.load(f)
except:
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

class GuestbookHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from anywhere
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data)
            name = data.get('name', '').strip()
            text = data.get('text', '').strip()
            if not name or not text:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Name and text required'}).encode())
                return

            # Load current messages
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                messages = json.load(f)

            # Append new message
            messages.append({
                'name': name,
                'text': text,
                'date': datetime.now().strftime("%m-%d-%y")
            })

            # Save back
            with open(JSON_FILE, 'w', encoding='utf-8') as f:
                json.dump(messages, f, indent=2)

            self._set_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())

        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_GET(self):
        # Optional: just return the JSON if someone GETs the port
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                messages = json.load(f)
            self._set_headers()
            self.wfile.write(json.dumps(messages).encode())
        except:
            self._set_headers(500)
            self.wfile.write(json.dumps([]).encode())

if __name__ == "__main__":
    server = HTTPServer(('', PORT), GuestbookHandler)
    print(f"Guestbook server running on port {PORT}...")
    server.serve_forever()
