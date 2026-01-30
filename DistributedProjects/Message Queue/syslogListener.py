import socket
import sys

# Usage: python syslog_listener.py <port>
# Example: python syslog_listener.py 6001


SYSLOG_PORT = 7000 # default syslog UDP port
ADDR = ("127.0.0.1", SYSLOG_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ADDR)

print(f"Listening for syslog messages on UDP {SYSLOG_PORT}...")

try:
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"[SYSLOG] {data.decode().strip()} (from {addr})")
except KeyboardInterrupt:
    print("Stopping syslog listener...")
    sock.close()
