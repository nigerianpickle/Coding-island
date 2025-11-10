import os
import select
import socket
import time

HOST = ''
PORT = 8081

HEADERS = """HTTP/1.1 {} OK
Content-Length: {}

"""
BODY = """Hello, world! :)\n\nNum hits: {}"""

LINE_ENDING = "\r\n"

hits = 0

def create_response(status: int, headers: dict[str, str], 
            body: bytes) -> bytes:
    # r = "HTTP/1.1 {}".format(status)
    r = f"HTTP/1.1 {status}{LINE_ENDING}"
    for k, v in headers.items():
        r += f"{k}: {v}{LINE_ENDING}"
    r += LINE_ENDING
    r = r.encode()

    if body and len(body) > 0:
        r += body
    
    return r

def get_file_contents(path) -> bytes:
    if not os.path.exists(path):
        return None
    
    f = open(path, "rb")
    contents = f.read()
    f.close()
    return contents
    

def serve_static(sock, method, uri):
    body = get_file_contents("static" + uri)
    
    if body:
        resp = create_response(200, 
                           {"Content-Length": len(body)},
                           body)
    else:
        resp = create_response(404, {}, None)

    sock.sendall(resp)
    sock.shutdown(socket.SHUT_RDWR)


def serve_hits(sock):
    body = BODY.format(hits)
    hdrs = HEADERS.format(len(body))
    resp = hdrs + body

    print("Sending response to", sock.getpeername(),
            ":\n", resp)

    # Convert all newlines to CRLF
    "\r\n".join(resp.split("\n"))

    sock.send(resp.encode())

def template_page(path, *vals):
    if not os.path.exists(path):
        return None
    
    f = open(path, "r")
    contents = f.read()
    f.close()
    return contents.format(*vals).encode() 

dynamic_val = "Purple"

def handle_colour_form(sock, uri, data):
    body = template_page("static/templates/colour.html", 
                         dynamic_val)
    resp = create_response(200, {}, body)
    sock.sendall(resp)
    sock.shutdown(socket.SHUT_RDWR)

def handle_request(sock):
    global hits
    try:
        # Client sent a request
        data = sock.recv(10024).decode()
        req = data.split("\n")[0]
        method, uri, _ = req.split(" ")

        # A reminder that browsers are cranky clients. With some requests, if we
        # don't consume the whole request, the browser thinks we've closed the
        # connection mid-request, even if we send them a properly formatted
        # response! We'll fix this in class later...

        # TODO(in-class): Consume whole request

        print("Received request from", sock.getpeername(),
                ":", method, uri)

        hits += 1

        if uri == "/":
            resp = create_response(301,
                                   {"Location": "/index.html"},
                                   None)
            sock.sendall(resp)
        elif uri.startswith("/colour.html"):
            handle_colour_form(sock, uri, data)
        elif method == "GET":
            serve_static(sock, method, uri)
        # else:
        #     serve_hit(sock)
        
        sock.shutdown(socket.SHUT_RDWR)
    except Exception as e:
        print("Error handling request from", sock.getpeername(),
              "\n", e)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST,PORT))
    s.listen()

    recvs = [s]

    while True:
        try:
            r_ready, _, _ = select.select(recvs, [], [])

            for sock in r_ready:
                if sock == s:
                    # Accept new conn through listening sock
                    newconn, addr = s.accept()
                    # FOR THE OSX FOLKS !!! -------------------
                    newconn.setblocking(False)

                    # Example of IP blocking, just close the socket when the bad
                    # client tries to connect!
                    # if addr[0] in ["10.152.119.163", "10.152.9.227"]:
                    #     newconn.close()
                    # else:
                    print("Accepting connetion from", addr)
                    recvs.append(newconn)
                else:
                    handle_request(sock)
                    sock.close()
                    # Done listening to them!
                    recvs.remove(sock)
        except OSError as e:
            print("Socket error:", e)
