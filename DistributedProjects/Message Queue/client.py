import socket
import sys

DEFAULT_PORT = 5000  # fallback port if not specified
HOST = "localhost"

# Usage: python client.py <port>
# Use default if no port argument provided
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    PORT = DEFAULT_PORT
    print(f"No port specified. Using default port {PORT}")

HOST = "localhost"

print(f"Connecting to {HOST}:{PORT}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    
    if not s:
        print("Socket not created")
    else:
        while True:
            inputData= input("Enter data to send/enter exit to quit: ")
            
            if inputData.lower() == "exit":
                print("Exiting")
                break
            else:
                s.sendall(inputData.encode())
                data = s.recv(1024)
                print(f"Received {data!r}")


