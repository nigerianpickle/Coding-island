# Name: Daniel Nwogo
# Student ID: 7931833


This program implements a peer-to-peer gossip network and the Oral Messages (OM(m)) consensus protocol as required for Assignment 3.
Each node:
- Discovers peers using UDP gossip
- Maintains a small distributed database of 5 words
- Participates in recursive OM(m) consensus
- Handles Byzantine behavior (optional)
- Never crashes due to malformed or adversarial messages


# How to Run
python3 peer.py [peer_port]

- peer_port is optional
- If not provided, OS chooses a random port


# Connecting to the CLI
Once the program starts, it prints something like

Peer Network Port = xxxx
CLI Port          = yyyy
Web Port          = zzzz


# To use the CLI
run - telnet host yyyy


you'll see:
Welcome to Daniel's node CLI!
Commands: peers, current, consensus <idx> <word>, lie, truth, exit


| Command                    | Description                       |
| -------------------------- | --------------------------------- |
| `peers`                    | Show known peers + last seen time |
| `current`                  | Print the 5-element database      |
| `consensus <index> <word>` | Start a consensus for db[index]   |
| `lie`                      | Enable Byzantine behavior         |
| `truth`                    | Return to honest behavior         |
| `exit`                     | Quit the CLI session              |


# Notes
Program fulfills discovery, consensus, and robustness requirements.
Works in malformed or message heavy network environments.
Threads sometimes explode and the code stops listening but i belive this issue to be fixed.




