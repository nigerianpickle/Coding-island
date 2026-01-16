import socket
import select
import sys
import queue

#Localhost
HOST=""
DEFAULT_CLIENT_PORT = 5000
DEFAULT_WORKER_PORT = 5001


#  Command line arguments
if len(sys.argv) >= 3:
    CLIENT_PORT = int(sys.argv[1])
    WORKER_PORT = int(sys.argv[2])
else:
    CLIENT_PORT = DEFAULT_CLIENT_PORT
    WORKER_PORT = DEFAULT_WORKER_PORT
    print(f"No ports specified. Using defaults: CLIENT_PORT={CLIENT_PORT}, WORKER_PORT={WORKER_PORT}")



# Data structures to hold jobs and their states
jobs = {}  
jobIDCounter=1 
jobsAvailable=[]


# Create listening sockets for client and worker connections
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.bind((HOST, CLIENT_PORT))
client_socket.listen()
client_socket.setblocking(False)

worker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
worker_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
worker_socket.bind((HOST, WORKER_PORT))
worker_socket.listen()
worker_socket.setblocking(False)


print(f"Listening for clients on {CLIENT_PORT}")
print(f"Listening for workers on {WORKER_PORT}")


inputs = [client_socket, worker_socket]

outputs = [ ]

# Outgoing message queues (socket:Queue)
message_queues = {}

while True:
    #Select returns three lists:
    #We want lists that are ready to be read, written to, or have an error
    readable, writable, exceptional = select.select(inputs, outputs, inputs,0)

    for s in readable:
        if s is client_socket:
            # A client is connecting
            conn, addr = client_socket.accept()
            print(f"Accepted client from {addr}")
            conn.setblocking(False)
            inputs.append(conn)
            message_queues[conn] = queue.Queue()

        elif s is worker_socket:
            # A worker is connecting
            conn, addr = worker_socket.accept()
            print(f"Accepted worker from {addr}")
            conn.setblocking(False)
            inputs.append(conn)
            message_queues[conn] = queue.Queue()

        else:
            # Existing client or worker sent data
            try:
                data = s.recv(1024)
            except ConnectionResetError:
                # Client/worker crashed or closed unexpectedly
                print("Connection reset by peer.")
                if s in outputs:
                    outputs.remove(s)
                if s in inputs:
                    inputs.remove(s)
                s.close()
                message_queues.pop(s, None)
                continue
            except OSError:
                # Socket no longer valid
                continue
            if data:
                #Data recieved from one of our Clients
                try:
                    message = data.decode().strip()
                    peer = s.getpeername()
                except OSError:
                    peer = "(disconnected)"
                print(f"Received: {message} from {peer}")
                #Job submission from client
                if message.startswith("JOB "):
                    jobText = message[4:]  # everything after 'JOB '
                    jobID = jobIDCounter
                    jobIDCounter += 1

                    jobs[jobID] = {"text": jobText, "state": "waiting"}
                    jobsAvailable.append(jobID)
                    print(f"Stored job {jobID}: {jobText}")
                
                    # Acknowledge job receipt
                    print(f"Sending job ID {jobID} to client {s.getpeername()}")
                    response = f"{jobID}\n".encode()
                    message_queues[s].put(response)
                    if s not in outputs:
                        outputs.append(s)
                #Status request from client
                elif message.startswith("STATUS "):
                    try:
                        requestedID = int(message.split()[1])  # extract ID safely
                    except (IndexError, ValueError):
                        response = b"INVALID_REQUEST\n"
                    else:
                        if requestedID in jobs:
                            status = jobs[requestedID]["state"]
                        else:
                            status = "unknown job ID"

                        print(f"STATUS request for job {requestedID}: {status}")

                        response = f"{status.upper()}\n".encode()

                    # Send the response back to client
                    message_queues[s].put(response)
                    if s not in outputs:
                        outputs.append(s)
                
                #Worker is connecting
                elif message.startswith("GET_JOB"):
                    if jobsAvailable:
                        # Get the first waiting job
                        jobID = jobsAvailable.pop(0)
                        jobData = jobs[jobID]["text"]

                        # Mark it as running
                        jobs[jobID]["state"] = "running"

                        print(f"Assigned job {jobID} to worker {s.getpeername()}")

                        # Send the job text and ID to the worker
                        response = f"JOB {jobID} {jobData}\n".encode()
                        message_queues[s].put(response)
                        
                        #Add it to outputs socket
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        # No jobs available
                        response = b"NO_JOBS\n"
                        message_queues[s].put(response)
                        if s not in outputs:
                            outputs.append(s)
                elif message.startswith("DONE"):
                    jobID = int(message.split()[1])
                    if jobID in jobs:
                        jobs[jobID]["state"] = "completed"
                        print(f"Job {jobID} marked as completed by {s.getpeername()}")
                    else:
                        print(f"Received DONE for unknown job {jobID}")
                else:
                    # Unrecognized command
                    print(f"Unknown command from {s.getpeername()}: {message}")
                    response = b"UNKNOWN_COMMAND\n"
                    message_queues[s].put(response)
                    if s not in outputs:
                        outputs.append(s)
            #No Data
            else:
            # No data means connection closed
                try:
                    peer = s.getpeername()
                except OSError:
                    peer = "(disconnected)"
                print(f"Closing connection to {peer}")

                if s in outputs:
                    outputs.remove(s)
                if s in inputs:
                    inputs.remove(s)
                s.close()
                message_queues.pop(s, None)

    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            outputs.remove(s)
        else:
            s.send(next_msg)

    for s in exceptional:
        print(f"Handling exceptional condition for {s.getpeername()}")
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]