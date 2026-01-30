import sys
import socket
import time
from multicast import multicastSenderSocket


# Usage:
#   python worker.py <workQueueHost:port> <outputPort> <syslogPort>

# Default values 
DEFAULT_WORKQUEUE_HOST = "localhost"
DEFAULT_WORKQUEUE_PORT = 5001  # port worker connects to (worker_port)
DEFAULT_OUTPUT_PORT = 6000     # multicast output
DEFAULT_SYSLOG_PORT = 7000     # syslog UDP port
MCAST_GRP = "239.0.0.1"



# Parse command-line arguments
if len(sys.argv) >= 2:
    host_port = sys.argv[1]
    if ":" in host_port:
        HOST, PORT = host_port.split(":")
        PORT = int(PORT)
    else:
        HOST = host_port
        PORT = DEFAULT_WORKQUEUE_PORT
else:
    HOST = DEFAULT_WORKQUEUE_HOST
    PORT = DEFAULT_WORKQUEUE_PORT
    print(f"No work queue host/port specified. Using default {HOST}:{PORT}")

OUTPUT_PORT = int(sys.argv[2]) if len(sys.argv) >= 3 else DEFAULT_OUTPUT_PORT
SYSLOG_PORT = int(sys.argv[3]) if len(sys.argv) >= 4 else DEFAULT_SYSLOG_PORT
SYSLOG_ADDR = ("127.0.0.1", SYSLOG_PORT)

print(f"Worker connecting to work queue at {HOST}:{PORT}")
print(f"Multicasting on {MCAST_GRP}:{OUTPUT_PORT}")
print(f"Sending logs to UDP {SYSLOG_ADDR}")



def log_syslog(message: str):
    """Send a syslog message via UDP."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as log_sock:
        log_sock.sendto(message.encode(), SYSLOG_ADDR)

def perform_job(job_id, job_text):
    """Send job words to multicast output port, 0.25 s apart."""
    sock = multicastSenderSocket()
    for word in job_text.split():
        msg = f"[Job {job_id}] {word}".encode()
        sock.sendto(msg, (MCAST_GRP, OUTPUT_PORT))
        time.sleep(0.25)
    sock.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        log_syslog(f"Worker connected to {HOST}:{PORT}")

        while True:
            log_syslog("Fetching job")
            s.sendall(b"GET_JOB\n")

            data = s.recv(1024)
            if not data:
                log_syslog("Server closed connection")
                break

            message = data.decode().strip()

            if message.startswith("JOB "):
                parts = message.split(maxsplit=2)
                job_id = int(parts[1])
                job_text = parts[2] if len(parts) > 2 else ""
                log_syslog(f"Starting job {job_id}")

                perform_job(job_id, job_text)

                log_syslog(f"Completed job {job_id}")
                s.sendall(f"DONE {job_id}\n".encode())

            elif message == "NO_JOBS":
                time.sleep(2)
            else:
                log_syslog(f"Unexpected message: {message}")
                time.sleep(2)

if __name__ == "__main__":
    main()
