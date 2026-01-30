# Name: Daniel Nwogo
# Student ID: 7931833

Ignore plan.txt

## Overview

This assignment implements a simple job queue system made up of three main parts:

# Client – submits jobs and checks their status

# Work Queue – manages job storage and communication between clients and workers

# Worker – retrieves and processes jobs, then reports completion

All components use default ports so they can run together without configuration.

Default Settings

Client connects to the Work Queue on port 5000

Work Queue listens for clients on port 5000 and for workers on port 5001

Worker sends multicast output to 239.0.0.1:6000

Syslog Listener receives logs on 127.0.0.1:7000

# client.py

Connects to the Work Queue using TCP.
Allows job submission (JOB <text>) and status checks (STATUS <id>).
Defaults to port 5000 if none is specified.

Run:
python client.py or python client.py [port]

# work_queue.py

Acts as the main job manager.
Accepts connections from both clients and workers, stores jobs, assigns them, and updates their status.
Uses select for handling multiple connections concurrently.
Defaults to ports 5000 (clients) and 5001 (workers).

Run:

python work_queue.py or python work_queue.py [clientport] [workerport]

# worker.py

Connects to the Work Queue to get jobs.
Processes each job by multicasting messages to the output group and logging to the syslog listener.
Defaults to localhost:5001 for the queue, 6000 for multicast, and 7000 for syslog.

Run:

python worker.py or python worker.py [workQueueIPAndPort] [outputPort] [syslogPort]




# Test files - Not needed for grading
# listener.py

Receives multicast messages from workers for testing.
Listens on 239.0.0.1:6000 by default.

Run:

python listener.py

# syslog_listener.py

Receives and displays log messages sent by workers over UDP.
Listens on 127.0.0.1:7000 by default.

Run:

python syslog_listener.py



# How to Run

Run each script in a separate terminal window in this order:

python work_queue.py
python worker.py
python listener.py(optional)
python syslog_listener.py(optional)
python client.py


Submit jobs from the client using JOB <text> and check their status with STATUS <id>.


# Why does multicast make sense?
Multicast makes sense here because multiple listeners (like monitoring tools, log collectors, or user interfaces) may need to receive the same job output at the same time. Instead of sending identical messages separately to each listener, multicast allows a worker to send one message that is automatically delivered to all subscribed receivers on the multicast group address.
