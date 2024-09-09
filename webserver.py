import socket
import threading

# Define the IP address(for host) and Port
HOST = socket.gethostbyname(socket.gethostname())
# HOST = "127.0.0.1"
PORT = 6060

# Creating socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the specific host and port
serverSocket.bind(("", PORT))

# A Function to serve HTML files
"""
This function reads the content of the file,
constructs the HTTP response
and return the response
"""
def Serve(path, type):
    # Attempt to open the file
    try:
        with open(path, 'rb') as file:
            # Read the content of the file
            content = file.read()
            response = f"HTTP/1.1 200 OK\nContent-Type: {type}\n\n"
            response = response.encode('utf-8') + content
    # Give error if the file is not found
    except FileNotFoundError:
        response = "HTTP/1.1 404 Not Found\n\nPage not found".encode('utf-8')
    return response


def HandleRequests(clientSocket,clientAddress):
    # Handle the request and send a response
    # Receive client requests

    request = clientSocket.recv(1024).decode('utf-8')
    print(f"Received HTTP request: {request}")

    # Return response
    response = ProcessRequests(request,clientAddress)

    # Send response
    clientSocket.sendall(response)

    # Close the connection with the client
    clientSocket.close()

# A Function to handle the client requests
""" 
This function takes the HTTP request and extracts 
the method and path from it to process the the request based on them
"""
def ProcessRequests(request,clientAddress):

    # Check if the method is GET
    if request.startswith("GET /"):

        # Extract the path from the request
        path = request.split()[1]

        # Print the received HTTP request to the terminal
        print(f"Received HTTP request: {request}")

        # Send main_en.html file with Content-Type: text/html
        if path == '/' or path == '/index.html' or path == '/main_en.html' or path == '/en':
            return Serve('main_en.html', 'text/html')

        # Response with main_ar.html which is an Arabic version of main_en.html
        elif path == '/ar':
            return Serve('main_ar.html', 'text/html')

        # Send the requested html file with Content-Type: text/html
        elif path.endswith('.html'):
            return Serve(path[1:], 'text/html')

        # Send the requested css file with Content-Type: text/css
        elif path.endswith('.css'):
            return Serve(path[1:], 'text/css')

        # Send the png image with Content-Type: image/png
        elif path.endswith('.png'):
            return Serve(path[1:], 'image/png')

        # Send the jpg image with Content-Type: image/jpeg
        elif path.endswith('.jpg'):
            return Serve(path[1:], 'image/jpeg')


        # Redirect to stackoverflow.com website
        elif path == '/so':
            return "HTTP/1.1 307 Temporary Redirect\nLocation: https://stackoverflow.com\n\n".encode('utf-8')
        # Redirect to itc website
        elif path == '/itc':
            return "HTTP/1.1 307 Temporary Redirect\nLocation: https://itc.birzeit.edu/\n\n".encode('utf-8')

        # Default: 404 Not Found
        return errorMSG(clientAddress)

def errorMSG(clientAddress):
    response = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n"

    try:
        with open("NotFound.html", "r") as errorFile:
            error_content = errorFile.read()
            error_content = error_content.replace("[Client IP address and Port]", f"{clientAddress[0]}:{clientAddress[1]}")
            response += error_content
    except FileNotFoundError:
        response += "<html><body><h1>404 Not Found</h1><p>The requested resource was not found.</p></body></html>"

    return response.encode('utf-8')

def start():
    # Listening for incoming connections
    serverSocket.listen(1)
    print(f"Server is listening on {PORT}..")
    while True:
        # Accept incoming client connections
        clientSocket, clientAddress = serverSocket.accept()

        # Create a new thread for each connected client
        thread = threading.Thread(target=HandleRequests, args=(clientSocket, clientAddress))
        thread.start()


if __name__ == "__main__":
    print("Server is starting..")
    start()


