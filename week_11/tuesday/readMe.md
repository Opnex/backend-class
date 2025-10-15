
🟢 GET File Explanation
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from http.server import ...: imports Python’s built-in HTTP server tools.

BaseHTTPRequestHandler → a class that handles HTTP requests (GET, POST, etc.).

HTTPServer → a class that creates a simple web server that listens for requests.

import json → imports the JSON module for converting Python data to and from JSON format.

data = [
    {
        "name": "Sam Larry",
        "track": "AI Developer"
    }
]
A list named data containing a single dictionary.

It acts as your mock database (the data you’ll return when someone makes a GET request).

class BasicAPI(BaseHTTPRequestHandler):
Creates a custom handler class by extending (inherits from) BaseHTTPRequestHandler.

This lets you define how the server should respond to different HTTP methods (like GET, POST, etc.).

    def send_data(self, data, status = 200):
Defines a helper method to send JSON data back to the client.

status=200 is the default HTTP status code for “OK”.

        self.send_response(status)
Built-in method from BaseHTTPRequestHandler that sets the HTTP status code in the response.

        self.send_header("Content-Type", "application/json")
Tells the client that the response is in JSON format.

        self.end_headers()
Ends the HTTP headers section. After this line, the body (actual data) of the response can be sent.

        self.wfile.write(json.dumps(data).encode())
self.wfile is a writable file-like object connected to the client.

json.dumps(data) → converts Python objects into JSON strings.

.encode() → converts the JSON string into bytes (because .write() expects bytes).

    def do_GET(self):
        self.send_data(data)
do_GET is a built-in method name recognized by BaseHTTPRequestHandler.

Whenever a client sends a GET request, this method runs.

It calls send_data(data), so the client gets the data list as a JSON response.

def run():
    HTTPServer(('localhost', 8000), BasicAPI).serve_forever()
Defines a function that creates and runs the server.

'localhost' → means it listens on your own computer.

8000 → the port number.

BasicAPI → the handler class to use.

.serve_forever() → keeps the server running continuously until you stop it manually.

print("Application is running ")
run()
Prints a message to the console.

Starts the server by calling run().

✅ Summary of the GET file:
When you run this file and visit http://localhost:8000 in your browser, the server responds with:

[
  {"name": "Sam Larry", "track": "AI Developer"}
]



🟠 POST File Explanation
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
Same as before:

BaseHTTPRequestHandler: handles incoming HTTP requests.

HTTPServer: starts a simple web server.

json: helps convert between Python objects and JSON strings.

data = []
Starts with an empty list.

This will act as your in-memory “database,” where all POSTed data will be stored while the program runs.

class BasicAPI(BaseHTTPRequestHandler):
Defines a new handler class for your HTTP requests.

You’ll teach it what to do when a POST request comes in.

    def send_data(self, payload, status = 200):
Helper method to send a JSON response to the client.

It takes:

payload: the data to send back.

status: the HTTP status code (default = 200 OK).

        self.send_response(status)
Sends the status line of the HTTP response (e.g., “HTTP/1.0 200 OK”).

        self.send_header("Content-Type", "application/json")
Adds a response header that says: “the content I’m sending is JSON.”

        self.end_headers()
Marks the end of the headers section.
(Everything after this will be part of the response body.)

        self.wfile.write(json.dumps(payload).encode())
Converts the Python object (payload) into a JSON string and encodes it into bytes before writing it to the response.

.wfile stands for “write file” — it’s how the server sends information to the client.

📥 Handling the POST Request
    def do_POST(self):
This method runs automatically whenever a POST request is received.

In HTTP, POST is used to send data to the server (e.g., when submitting a form or creating a new record).

        content_size = int(self.headers.get("Content-Length", 0))
Reads the Content-Length header from the client’s request.

This header tells the server how many bytes of data are in the body of the request.

Converts it to an integer.

        passed_data = self.rfile.read(content_size)
.rfile stands for “read file” — it lets the server read the body of the incoming request.

.read(content_size) reads exactly that many bytes.

        post_data = json.loads(passed_data)
Converts the JSON string (received from the client) into a Python dictionary.

Example:

'{"name": "Sam", "track": "AI"}' → {"name": "Sam", "track": "AI"}
        print(post_data)
Prints the received data in the console — just for you to see what the client sent.

        data.append(post_data)
Adds the received dictionary into the data list (your in-memory database).

So, each time you POST new data, it gets stored.

        self.send_data({
            "message": "Data Recieved",
            "data": post_data
        })
Sends a response back to the client confirming receipt.

The response looks like:

{
  "message": "Data Recieved",
  "data": {"name": "Sam", "track": "AI"}
}
def run():
    HTTPServer(('localhost', 8000), BasicAPI).serve_forever()
Starts an HTTP server on port 8000, using your BasicAPI class to handle requests.

print("Application is running ")
run()
Prints a message and starts the server.

✅ Summary of the POST file:
When you run it, you can send data to http://localhost:8000 (e.g., using Postman or curl) with a POST request like:

{
  "name": "Tunde",
  "track": "Backend Developer"
}
Then the server:

Reads that JSON,

Converts it to a Python dictionary,

Stores it in the data list,

Sends back a confirmation JSON.