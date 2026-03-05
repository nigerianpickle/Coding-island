import networkx as nx
from collections import Counter

CONTINUITY_MULTIPLIER = 10

# ======================
# DATA (same as before)
# ======================

swimmer_rules = {
    "The Nervous/New": ["New RSS/Babies", "High Energy", "Soft-Spoken"],
    "The Fearless/Energetic": ["High Energy", "Technique Driven"],
    "The Hard Worker": ["Technique Driven", "DIA"],
    "The Socialite/Talker": ["Technique Driven", "Soft-Spoken", "High Energy"],
    "The Natural": ["Technique Driven", "Soft-Spoken"],
    "The Slow Progress": ["Adapted", "Technique Driven", "High Energy"],
    "Not Used to 'No'": ["DIA", "Adapted"]
}

instructors = [
    {"name": "Alice", "style": "Soft-Spoken"},
    {"name": "Ben", "style": "High Energy"},
    {"name": "Cara", "style": "Technique Driven"},
    {"name": "Dan", "style": "Adapted"},
    {"name": "Eva", "style": "DIA"}
]

student_types = {
    "Student_1": "The Nervous/New",
    "Student_2": "The Hard Worker",
    "Student_3": "The Slow Progress",
    "Student_4": "The Fearless/Energetic"
}

classes = {
    "Class_A": ["Student_1", "Student_2", "Student_3"],
    "Class_B": ["Student_4"]
}

student_history = {
    "Student_1": ["Alice"],
    "Student_2": ["Alice", "Ben"],
    "Student_3": ["Cara"],
    "Student_4": ["Ben"]
}

# ======================
# HELPERS
# ======================

def continuity_votes(students):
    votes = []
    for s in students:
        votes.extend(student_history.get(s, []))
    return Counter(votes)

def style_votes(students):
    votes = []
    for s in students:
        swimmer_type = student_types[s]
        votes.extend(swimmer_rules[swimmer_type])
    return Counter(votes)

# BUILD GRAPH

G = nx.Graph()

# Add nodes
G.add_nodes_from(classes.keys(), bipartite=0)
G.add_nodes_from([i["name"] for i in instructors], bipartite=1)

# Add weighted edges
for class_id, students in classes.items():
    cont = continuity_votes(students)
    style = style_votes(students)

    for inst in instructors:
        name = inst["name"]

        continuity_score = cont.get(name, 0)
        style_score = style.get(inst["style"], 0)

        score = continuity_score * CONTINUITY_MULTIPLIER + style_score

        if score > 0:
            G.add_edge(class_id, name, weight=score)

# RUN MATCHING

matching = nx.algorithms.matching.max_weight_matching(G)

# OUTPUT

print("\nGRAPH MATCH RESULTS")
for a, b in matching:
    if a in classes:
        print(f"{a} → {b}")
    else:
        print(f"{b} → {a}")
