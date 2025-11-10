#!/usr/bin/env python3
import os, socket, threading, json, uuid, time
from urllib.parse import urlparse, parse_qs

HOST = ""
PORT = 8081
BUF = 4096
CRLF = "\r\n"

users = {}       # username -> password
sessions = {}    # session_id -> username
messages = []    # {id, user, text, ts}
next_msg_id = 1
state_lock = threading.Lock()

STATUS_TEXT = {
    200: "OK", 201: "Created", 204: "No Content",
    301: "Moved Permanently", 400: "Bad Request", 401: "Unauthorized",
    403: "Forbidden", 404: "Not Found", 500: "Internal Server Error"
}

def http_response(status=200, headers=None, body=b""):
    headers = headers or {}
    headers.setdefault("Content-Length", str(len(body)))
    headers.setdefault("Connection", "close")
    start = f"HTTP/1.1 {status} {STATUS_TEXT.get(status, 'OK')}{CRLF}"
    h = "".join(f"{k}: {v}{CRLF}" for k, v in headers.items())
    return (start + h + CRLF).encode() + body

def json_body(obj):
    data = json.dumps(obj).encode()
    return data, {"Content-Type": "application/json", "Content-Length": str(len(data))}

def content_type_for(path):
    if path.endswith(".html"): return "text/html; charset=utf-8"
    if path.endswith(".js"): return "application/javascript"
    if path.endswith(".css"): return "text/css"
    if path.endswith(".png"): return "image/png"
    if path.endswith(".jpg") or path.endswith(".jpeg"): return "image/jpeg"
    return "application/octet-stream"

def parse_headers(hbytes):
    lines = hbytes.decode(errors="ignore").split(CRLF)
    req = lines[0]
    hdrs = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            hdrs[k.strip().lower()] = v.strip()
    return req, hdrs

def parse_cookies(headers):
    cookie_line = headers.get("cookie", "")
    cookies = {}
    for c in cookie_line.split(";"):
        if "=" in c:
            k, v = c.strip().split("=", 1)
            cookies[k] = v
    return cookies

def current_user(headers):
    cookies = parse_cookies(headers)
    sid = cookies.get("session")
    with state_lock:
        return sessions.get(sid)

def read_exact(sock, need):
    data = b""
    while len(data) < need:
        part = sock.recv(min(BUF, need - len(data)))
        if not part: break
        data += part
    return data

# ---- API handlers ----

def handle_get_messages(sock, headers, query):
    user = current_user(headers)
    if not user:
        body, h = json_body({"error": "not logged in"})
        sock.sendall(http_response(401, h, body))
        return
    last = int(query.get("last", [0])[0]) if "last" in query else 0
    with state_lock:
        new_msgs = [m for m in messages if m["ts"] > last]
    body, h = json_body({"messages": new_msgs, "now": int(time.time()*1000)})
    sock.sendall(http_response(200, h, body))

def handle_post_messages(sock, headers, body):
    user = current_user(headers)
    if not user:
        body, h = json_body({"error": "not logged in"})
        sock.sendall(http_response(401, h, body)); return
    try:
        text = (json.loads(body.decode()).get("text") or "").strip()
    except: text = ""
    if not text:
        body, h = json_body({"error": "text required"})
        sock.sendall(http_response(400, h, body)); return
    global next_msg_id
    with state_lock:
        msg = {"id": next_msg_id, "user": user, "text": text, "ts": int(time.time()*1000)}
        next_msg_id += 1
        messages.append(msg)
    body, h = json_body(msg)
    sock.sendall(http_response(201, h, body))

def handle_delete_message(sock, headers, mid):
    user = current_user(headers)
    if not user:
        body, h = json_body({"error": "not logged in"})
        sock.sendall(http_response(401, h, body)); return
    try:
        mid = int(mid)
    except:
        body, h = json_body({"error": "bad id"})
        sock.sendall(http_response(400, h, body)); return
    with state_lock:
        for i, m in enumerate(messages):
            if m["id"] == mid:
                if m["user"] != user:
                    body, h = json_body({"error": "cannot delete others"})
                    sock.sendall(http_response(403, h, body)); return
                messages.pop(i)
                sock.sendall(http_response(204, {}, b"")); return
    body, h = json_body({"error": "not found"})
    sock.sendall(http_response(404, h, body))

def handle_post_user(sock, _, body):
    try: data = json.loads(body.decode())
    except: data = {}
    u, p = (data.get("user") or "").strip(), (data.get("pass") or "").strip()
    if not u or not p:
        body, h = json_body({"error":"missing user or pass"})
        sock.sendall(http_response(400, h, body)); return
    with state_lock:
        if u in users:
            body, h = json_body({"error":"user exists"})
            sock.sendall(http_response(400, h, body)); return
        users[u] = p
    body, h = json_body({"ok": True})
    sock.sendall(http_response(200, h, body))

def handle_post_login(sock, _, body):
    try: data = json.loads(body.decode())
    except: data = {}
    u, p = data.get("user"), data.get("pass")
    with state_lock:
        if users.get(u) != p:
            body, h = json_body({"error":"invalid credentials"})
            sock.sendall(http_response(403, h, body)); return
        sid = str(uuid.uuid4()); sessions[sid] = u
    b, h = json_body({"ok": True, "user": u})
    h["Set-Cookie"] = f"session={sid}; HttpOnly; Path=/; SameSite=Lax"
    sock.sendall(http_response(200, h, b))

def handle_delete_login(sock, _):
    b, h = json_body({"ok": True})
    h["Set-Cookie"] = "session=deleted; Max-Age=0; Path=/"
    sock.sendall(http_response(200, h, b))

def handle_get_login(sock, headers):
    u = current_user(headers)
    if u:
        b, h = json_body({"loggedIn": True, "user": u})
        sock.sendall(http_response(200, h, b))
    else:
        b, h = json_body({"loggedIn": False})
        sock.sendall(http_response(200, h, b))

# ---- Static files ----

def serve_static(sock, path):
    if path == "/":
        sock.sendall(http_response(301, {"Location": "/index.html"})); return
    fs_path = os.path.normpath("static" + path)
    if not fs_path.startswith("static") or not os.path.exists(fs_path):
        b, h = json_body({"error":"not found"})
        sock.sendall(http_response(404, h, b)); return
    with open(fs_path, "rb") as f: data = f.read()
    sock.sendall(http_response(200, {"Content-Type": content_type_for(fs_path)}, data))

# ---- Connection handler ----

def handle_client(conn, addr):
    try:
        data = b""
        while b"\r\n\r\n" not in data:
            part = conn.recv(BUF)
            if not part: break
            data += part
            
        
        if not data: return
        head, body = data.split(b"\r\n\r\n", 1)
        req, hdrs = parse_headers(head)
        parts = req.split()
        if len(parts) < 3: return
        method, target = parts[0], parts[1]
        parsed = urlparse(target)
        path, query = parsed.path, parse_qs(parsed.query)
        clen = int(hdrs.get("content-length","0"))
        if len(body) < clen:
            body += read_exact(conn, clen - len(body))

        # Routes
        if path.startswith("/api/"):
            if path == "/api/user" and method == "POST":
                handle_post_user(conn, hdrs, body)
            elif path == "/api/login" and method == "POST":
                handle_post_login(conn, hdrs, body)
            elif path == "/api/login" and method == "DELETE":
                handle_delete_login(conn, hdrs)
            elif path == "/api/login" and method == "GET":
                handle_get_login(conn, hdrs)
            elif path == "/api/messages" and method == "GET":
                handle_get_messages(conn, hdrs, query)
            elif path == "/api/messages" and method == "POST":
                handle_post_messages(conn, hdrs, body)
            elif path.startswith("/api/messages/") and method == "DELETE":
                mid = path.split("/")[-1]
                handle_delete_message(conn, hdrs, mid)
            else:
                b, h = json_body({"error":"unknown"})
                conn.sendall(http_response(404, h, b))
        else:
            serve_static(conn, path)
    except Exception as e:
        b, h = json_body({"error": str(e)})
        try:
            conn.sendall(http_response(500, h, b))
        except:
            pass
    finally:
        try: conn.shutdown(socket.SHUT_RDWR)
        except: pass
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(64)
        print(f"Listening on :{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
