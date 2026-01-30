import socket
import threading
import json
import uuid
import random
import time
import sys

class Node:
    def __init__(self, name="Me!", cli_port=16000, web_port=18080):
        self.name = name
        self.cli_port = cli_port
        self.web_port = web_port

        # UDP socket for gossip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = self.get_local_ip()
        self.port = self.cli_port
        self.peers_lock = threading.Lock()

        # Data structures
        self.peers = {}  # peer_id -> {name, cliPort, webPort, last_seen}
        self.recent_gossips = set()
        self.db = ["", "", "", "", ""]
        self.consensus_db = {}
        
        

        # Config
        self.well_known_peers = [
            ("hawk.cs.umanitoba.ca", 10000),
            ("falcon.cs.umanitoba.ca", 10000),
            ("cormorant.cs.umanitoba.ca", 10000),
            ("nuthach.cs.umanitoba.ca", 10000)
        ]
        self.max_forward = 5
        self.gossip_interval = 60  # seconds
        self.peer_timeout = 120    # seconds
        self.lie_mode = False

    def generate_lie(self):
        lies = [
            "quantum raccoon turbulence",
            "fermented ethernet soup",
            "ultra-mega-turbo pigeon",
            "cursed wifi goblin",
            "dill pickle massacre",
            "Zach is rad",
            "Google? More like schmoogle!"
        ]
        return random.choice(lies)

    # ------------------------
    # Helpers
    # ------------------------
    def hostport_str(self, host, port):
        return f"{host}:{int(port)}"
    
    def handle_leaf_message_SAFE(self, cid, parentid, sender, value, peers, msg):
        """
        SAFE version of leaf-handling logic.
        Does not break on malformed messages.
        Creates placeholder parents only when valid.
        """
        print("\n[SAFE LEAF] Handling leaf message:")
        print("    cid       =", cid)
        print("    parentid  =", parentid)
        print("    sender    =", sender)
        print("    value     =", value)
        print("    peers     =", peers)

        self_id = f"{self.host}:{self.port}"


        # Parent must be a valid UUID
        try:
            uuid.UUID(str(parentid))
        except:
            print(f"[SAFE LEAF] Dropping: invalid parentid format ({parentid})")
            return

        # Message must be intended for me
        if self_id not in peers:
            print(f"[SAFE LEAF] Dropping: message not intended for me. peers={peers}")
            return

        # Create placeholder parent if needed
        if parentid not in self.consensus_db:
            self.consensus_db[parentid] = {
                "index": None,
                "value": None,
                "omlevel": None,
                "parentid": None,
                "peers": [],          
                "responses": {},
                "start_time": time.time()
            }

        parent = self.consensus_db[parentid]
        print("    parent existing responses:", parent["responses"])
        send_leaf = value
        if self.lie_mode:
            send_leaf = self.generate_lie()
            print(f"[LIE MODE] Leaf lie: {send_leaf}")

        parent["responses"][cid] = send_leaf

        # Only attempt finish if parent definition exists
        if parent["peers"]:
            self.try_finish_consensus(parentid)
        else:
            print("[SAFE LEAF] Parent not fully defined yet → waiting.")


    def parse_hostport(self, s):
        # input like "host:port" -> (host, int(port)) 
        h, p = s.split(":", 1)
        return h, int(p)
    
    
    # Get local IP
    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip
    
    def print_known_peers(self):
        while True:
            time.sleep(15)
            with self.peers_lock:
                print("\n--- Known Peers ---")
                for peer_id, info in self.peers.items():
                    print(f"{peer_id} (last seen: {info['last_seen']}) (Name:{info['name']})")
                print("-------------------\n")
                print("Current Database State:")
                print(self.db)
                print("-------------------\n")

    # Message creation
    def create_gossip_message(self):
        return json.dumps({
            "command": "GOSSIP",
            "host": self.host,
            "port": self.port,
            "name": self.name,
            "id": str(uuid.uuid4()),
            "cliPort": self.cli_port,
            "webPort": self.web_port
        }).encode()

    def create_gossip_reply(self):
        return json.dumps({
            "command": "GOSSIP_REPLY",
            "host": self.host,
            "port": self.port,
            "name": self.name,
            "cliPort": self.cli_port,
            "webPort": self.web_port
        }).encode()
        
    
    def start_consensus(self, index, value):
        peers = list(self.peers.keys())
        N = len(peers) + 1
        m = max((N - 1) // 3, 0)

        cid = str(uuid.uuid4())
        self_id = f"{self.host}:{self.port}"

        msg = {
            "command": "CONSENSUS",
            "id": cid,
            "omlevel": m,
            "initiator": self_id,
            "peers": peers,
            "index": index,
            "value": value,
            "parentid": None
        }

        # commit immediately
        self.db[index] = value

        # create root consensus entry
        self.consensus_db[cid] = {
            "index": index,
            "value": value,
            "omlevel": m,
            "parentid": None,
            "peers": peers,
            "responses": { self_id: value },   # <-- FIX 3
            "start_time": time.time()
        }

        # send to peers
        # for p in peers:
        #     h, prt = p.split(":")
        #     self.send_message((h, int(prt)), json.dumps(msg).encode())
            
        # send different lies to each peer
        for p in peers:
            h, prt = p.split(":")
            
            peer_value = value
            if self.lie_mode:
                peer_value = self.generate_lie()
                print(f"[LIE MODE] General → {p}: sending {peer_value}")

            peer_msg = msg.copy()
            peer_msg["value"] = peer_value

            self.send_message((h, int(prt)), json.dumps(peer_msg).encode())

        print(f"Started consensus {cid}, m={m}, value={value}")

    # Send messages
    def send_message(self, peer, message):
        try:
            self.sock.sendto(message, peer)
        except Exception as e:
            print(f"Failed to send message to {peer}: {e}")

    # Handle incoming messages
    def handle_message(self, data, addr):
        
        #Malformed JSON
        try:
            msg = json.loads(data)
        except:
            #print(f"Received malformed message from {addr}")
            return


        cmd = msg.get("command")
        msg_host = msg.get("host")
        msg_port = msg.get("port")

        # Handle consensus messages first
        if cmd == "CONSENSUS":
            self.handle_consensus_message(msg, addr)
            return
        
        # Skip if host or port is missing
        if not msg_host or not msg_port:
            #print(f"Malformed peer info from {addr}: host={msg_host}, port={msg_port}")
            return
        
        # Identify peer by the host/port THEY CLAIM
        peer_id = f"{msg_host}:{msg_port}"


        # Add unknown peers
        if peer_id not in self.peers:
            self.peers[peer_id] = {
                "name": msg.get("name", ""),
                "cliPort": msg.get("cliPort"),
                "webPort": msg.get("webPort"),
                "last_seen": time.time()
            }
            print(f"Added new peer: {peer_id}")
            # Send reply to their host/port
            self.send_message((msg_host, msg_port), self.create_gossip_reply())


        # Update last_seen
        self.peers[peer_id]["last_seen"] = time.time()
        # Handle commands
        if cmd == "GOSSIP":
            if msg["id"] not in self.recent_gossips:
                self.recent_gossips.add(msg["id"])

                # forward gossip to up to 5 peers
                peers_to_forward = random.sample(
                    list(self.peers.keys()),
                    min(self.max_forward, len(self.peers))
                )
                for p in peers_to_forward:
                    h, p_port = p.split(":")
                    self.send_message((h, int(p_port)), data)

        elif cmd == "GOSSIP_REPLY":
            print(f"GOSSIP_REPLY from {peer_id}")

             
    # Handle consensus messages
    def try_finish_consensus(self, cid):
        entry = self.consensus_db[cid]
        peers = entry["peers"]

        # DEBUG PRINTS
        # print("\n[DEBUG FINISH] cid =", cid)
        # print("[DEBUG FINISH] responses =", entry["responses"])
        # print("[DEBUG FINISH] expected peers =", peers)
        # print("[DEBUG FINISH] count =", len(entry["responses"]), "/", len(peers))
        # Need responses from all peers
        if len(entry["responses"]) < len(peers):
            return

        # Compute majority value
        values = list(entry["responses"].values())
        majority = max(set(values), key=values.count)

        print(f"[CONSENSUS COMPLETE] cid={cid} → majority = {majority}")

        # Write to database
        self.db[entry["index"]] = majority

        # If this has a parent, bubble upward
        if entry["parentid"] is not None:
            parent_id = entry["parentid"]
            parent = self.consensus_db[parent_id]
            my_id = f"{self.host}:{self.port}"
            send_up = majority
            if self.lie_mode:
                send_up = self.generate_lie()
                print(f"[LIE MODE] Lying in upward propagation: {send_up}")

            parent["responses"][my_id] = send_up
            self.try_finish_consensus(parent_id)
    
    def handle_consensus_message(self, msg, addr):
        cid = msg.get("id")
        m = msg.get("omlevel")
        if m is None:
            print(f"[CONSENSUS] Dropping malformed message missing omlevel: {msg}")
            return
        
        index = msg["index"]
        value = msg["value"]
        parentid = msg["parentid"]
        if not parentid:      
            parentid = None
        peers = msg["peers"]

        sender = f"{addr[0]}:{addr[1]}"

        self_id = f"{self.host}:{self.port}"

        # Drop consensus messages not meant for me
        if not isinstance(peers, list):
            print(f"[CONSENSUS] Malformed message missing peer list from {addr}: {msg}")
            return
        
        
        # create or load entry
        if cid not in self.consensus_db:
            self.consensus_db[cid] = {
                "index": index,
                "value": value,
                "omlevel": m,
                "parentid": parentid,
                "peers": peers,
                "responses": {},
                "start_time": time.time()
            }

        entry = self.consensus_db[cid]
        entry["responses"][sender] = value
        
        #Add self to responses
        send_value = value

        if self.lie_mode:
            send_value = self.generate_lie()
            print(f"[LIE MODE] Lying in consensus response: received={value}, sending={send_value}")

        entry["responses"][self_id] = send_value
        

        print(f"[CONSENSUS] cid={cid} m={m} sender={sender} val={value}")

        # m > 0 => start subconsensus
        if m > 0:

            # FIX 1 — REMOVE NEW INITIATOR (NOT SENDER)
            sub_peers = [p for p in peers if p != self_id]

            sub_id = str(uuid.uuid4())
            
            sub_send_value = value
            if self.lie_mode:
                sub_send_value = self.generate_lie()
                print(f"[LIE MODE] Subconsensus broadcast lie: {sub_send_value}")

            sub_msg = {
                "command": "CONSENSUS",
                "id": sub_id,
                "omlevel": m - 1,
                "initiator": self_id,
                "peers": sub_peers,
                "index": index,
                "value": sub_send_value,
                "parentid": cid
            }
                
            # create sub-entry
            self.consensus_db[sub_id] = {
                "index": index,
                "value": value,
                "omlevel": m - 1,
                "parentid": cid,
                "peers": sub_peers,
                "responses": { self_id: sub_send_value },  # FIX 3 self vote
                "start_time": time.time()
            }

            # send sub-message
            for p in sub_peers:
                h, prt = p.split(":")
                self.send_message((h, int(prt)), json.dumps(sub_msg).encode())

            return

        # m == 0 => leaf
        if m == 0 and parentid:

            # NEW BEHAVIOR:
            self.handle_leaf_message_SAFE(cid, parentid, sender, value, peers, msg)
            return

    # Listener loop
    def listen_loop(self):
        print(f"Node listening on {self.host}:{self.port}")
        while True:
            try:
                data, addr = self.sock.recvfrom(4096)
            except Exception as e:
                print(f"[FATAL SOCKET ERROR] {e}")
                continue

            try:
                self.handle_message(data, addr)
            except Exception as e:
                print("\n[LISTEN LOOP ERROR] A message caused an exception but listener is still alive.")
                print(f"Error: {e}")
                print(f"Offending addr: {addr}")
                print(f"Raw data: {data}\n")
                continue

    # Heartbeat gossip
    def gossip_heartbeat(self):
        while True:
            message = self.create_gossip_message()
            if self.peers:
                for peer_id in random.sample(list(self.peers.keys()), min(self.max_forward, len(self.peers))):
                    h, p_port = peer_id.split(":")
                    self.send_message((h, int(p_port)), message)

            # Remove inactive peers
            now = time.time()
            for peer_id in list(self.peers.keys()):
                if now - self.peers[peer_id]["last_seen"] > self.peer_timeout:
                    print(f"Dropping inactive peer {peer_id}")
                    del self.peers[peer_id]

            time.sleep(self.gossip_interval)

    # Initial join of network
    def join_mesh(self):
        initial_peers = random.sample(self.well_known_peers, 2)
        gossip_msg = self.create_gossip_message()
        for peer in initial_peers:
            self.send_message(peer, gossip_msg)
        print(f"Sent initial gossip to: {initial_peers}")

    def test_consensus(self):
        # pick an index and a value
        index = 0
        value = "hello"
        
        print(f"Starting quick test consensus on db[{index}] = {value}")
        self.start_consensus(index, value)

        # wait a bit to let gossip/consensus propagate
        time.sleep(5)

        print("Database after test consensus:")
        print(self.db)

    def cli_server(self):
        """Simple TCP CLI server."""
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("0.0.0.0", self.cli_port))
        srv.listen(5)
        print(f"CLI listening on {self.host}:{self.cli_port}")

        while True:
            conn, addr = srv.accept()
            threading.Thread(
                target=self.handle_cli_client, 
                args=(conn, addr), 
                daemon=True
            ).start()

    def handle_cli_client(self, conn, addr):
        conn.sendall(b"Welcome to Daniel's node CLI!\n")
        conn.sendall(b"Commands: peers, current, consensus <idx> <word>, lie, truth, exit\n> ")

        with conn:
            buf = b""
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                buf += data
                # process line by line
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    line = line.decode().strip()
                    if not line:
                        conn.sendall(b"> ")
                        continue

                    parts = line.split()
                    cmd = parts[0].lower()

                    if cmd == "exit":
                        conn.sendall(b"Bye!\n")
                        return

                    elif cmd == "peers":
                        out_lines = []
                        with self.peers_lock:
                            for peer_id, info in self.peers.items():
                                out_lines.append(
                                    f"{peer_id} (last seen: {info['last_seen']}) (Name:{info['name']})"
                                )
                        if not out_lines:
                            conn.sendall(b"No peers known.\n")
                        else:
                            conn.sendall(("\n".join(out_lines) + "\n").encode())

                    elif cmd == "current":
                        conn.sendall((f"DB = {self.db}\n").encode())

                    elif cmd == "consensus":
                        if len(parts) < 3:
                            conn.sendall(b"Usage: consensus <index> <word>\n")
                        else:
                            try:
                                idx = int(parts[1])
                            except ValueError:
                                conn.sendall(b"Index must be an integer.\n")
                                conn.sendall(b"> ")
                                continue
                            word = " ".join(parts[2:])
                            conn.sendall(
                                f"Starting consensus on db[{idx}] = {word}\n".encode()
                            )
                            self.start_consensus(idx, word)

                    elif cmd == "lie":
                        self.lie_mode = True
                        conn.sendall(b"Now lying.\n")

                    elif cmd == "truth":
                        self.lie_mode = False
                        conn.sendall(b"Back to truth.\n")

                    else:
                        conn.sendall(b"Unknown command.\n")

                    conn.sendall(b"> ")
                    
    # Start the node
    def start(self):
        threading.Thread(target=self.listen_loop, daemon=True).start()
        time.sleep(0.5)  # ensure listener is ready

        self.join_mesh()
        threading.Thread(target=self.gossip_heartbeat, daemon=True).start()
        # threading.Thread(target=self.print_known_peers, daemon=True).start()
        threading.Thread(target=self.cli_server, daemon=True).start()

        while True:
            time.sleep(1)


# Run the node
if __name__ == "__main__":
    # Default: OS chooses peer port automatically
    peer_port = 0

    # If program is run like: ./peer 16000
    if len(sys.argv) == 2:
        try:
            peer_port = int(sys.argv[1])
        except ValueError:
            print("Usage: ./peer [peer_port]")
            sys.exit(1)

    # CLI and Web ports MUST NOT conflict with peer network port
    # Use safe high ranges
    cli_port = 50000 + random.randint(0, 5000)
    web_port = 60000 + random.randint(0, 5000)

    # Create node
    node = Node(name="Daniel", cli_port=cli_port, web_port=web_port)

    # Override peer network port
    node.port = peer_port
    node.sock.bind(("0.0.0.0", node.port))

    # If peer_port was 0, OS assigns one — fetch actual port
    node.port = node.sock.getsockname()[1]

    print("========== NODE PORTS ==========")
    print(f"Peer Network Port = {node.port}")
    print(f"CLI Port          = {cli_port}")
    print(f"Web Port          = {web_port}")
    print("================================\n")

    node.start()

