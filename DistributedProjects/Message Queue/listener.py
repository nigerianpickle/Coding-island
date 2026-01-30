import time
import socket
from multicast import multicastReceiverSocket
import multicast  # to patch _getIP on Windows
import traceback



# --- Multicast settings ---
GROUP = "239.0.0.1"
PORT = 6000  #matches the workers deafult OUTPUT_PORT

# Create multicast socket (already joined to the group)
try:
    sock = multicastReceiverSocket(GROUP, PORT)
except Exception as e:
    print("Failed to create multicast socket:")
    traceback.print_exc()
    exit(1)

print(f"Listening for multicast messages on {GROUP}:{PORT}")

try:
    while True:
        data, addr = sock.recvfrom(1024)  # blocking call
        print(f"[Multicast] {data.decode().strip()} (from {addr})")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping multicast listener...")
    sock.close()
