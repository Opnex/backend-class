from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = []

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())
    
    def do_POST(self):
        content_size = int(self.headers.get("Content-Length", 0))
        passed_data = self.rfile.read(content_size)

        post_data = json.loads(passed_data)
        print(post_data)
        data.append(post_data)
        self.send_data({
            "message": "Data Recieved",
            "data": post_data
        })
        
def run():
    HTTPServer(('localhost', 8000), BasicAPI).serve_forever()

print("Application is running ")
run()