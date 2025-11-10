import select
import socket
import time

HOST = ''
PORT = 8081

HEADERS = """HTTP/1.1 200 OK
Content-Length: {}

"""
BODY = """Hello, world! :)\n\nNum hits: {}"""

hits = 0

def get_file_contents(path) -> bytes:
    f = open(path, "rb")
    contents = f.read()
    f.close()
    return contents

def serve_static(sock, method, uri):
    body = get_file_contents("static" + uri)
    hdrs = HEADERS.format(len(body))
    hdrs = "\r\n".join(hdrs.split("\n"))

    resp = hdrs.encode() + body
    
    print(f"Sending {len(body)} bytes of body, {len(resp)} bytes total.")

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


def handle_request(sock):
    global hits
    try:
        # Client sent a request
        data = sock.recv(1024).decode()
        req = data.split("\n")[0]
        method, uri, _ = req.split(" ")

        # A reminder that browsers are cranky clients. With some requests, if we
        # don't consume the whole request, the browser thinks we've closed the
        # connection mid-request, even if we send them a properly formatted
        # response! We'll fix this in class later...

        print("Received request from", sock.getpeername(),
                ":", method, uri)

        hits += 1

        if method == "GET":
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
