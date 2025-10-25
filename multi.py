import socket
import selectors
import time
import types
import sys
import re

#Localhost
HOST="127.0.0.1"
CLIENT_PORT=5000
WORKER_PORT=5001

WORKER_PORT="not used"

sel=selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    #Makes it return immediately if no data is available
    conn.setblocking(False)
    
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


            

#Listening Socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as multiConnection:
    multiConnection.bind((HOST,CLIENT_PORT))
    multiConnection.listen()

    print(f"Multi-server is listening on port {CLIENT_PORT}")
    #Register the socket to be monitored and what should happen when it is accessed
    
    #We also set the blocking to false
    
    multiConnection.setblocking(False)
    
    #sel.register() registers the socket to be monitored with sel.select() for the events that you’re interested in. For the listening socket, you want read events: selectors.EVENT_READ.
    #Make the data none since we dont have any data yet
    sel.register(multiConnection, selectors.EVENT_READ, data=None)
    
    
    
    #event loop
    try:
        while True:
            #Blocks until there are sockets ready for io
            events = sel.select(timeout=None)
            for key, mask in events:
                
                if key.data is None:
                    #A new connection is being made
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()