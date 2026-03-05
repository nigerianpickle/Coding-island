import networkx as nx

CONTINUITY_MULTIPLIER = 10

# -------------------
# DATA
# -------------------

# Student preferences
swimmer_rules = {
    "The Nervous/New": ["New RSS/Babies", "High Energy", "Soft-Spoken"],
    "The Fearless/Energetic": ["High Energy", "Technique Driven"],
    "The Hard Worker": ["Technique Driven", "DIA"],
    "The Socialite/Talker": ["Technique Driven", "Soft-Spoken", "High Energy"],
    "The Natural": ["Technique Driven", "Soft-Spoken"],
    "The Slow Progress": ["Adapted", "Technique Driven", "High Energy"],
    "Not Used to 'No'": ["DIA", "Adapted"]
}

# Students and types
student_types = {
    "Student_1": "The Nervous/New",
    "Student_2": "The Hard Worker",
    "Student_3": "The Slow Progress",
    "Student_4": "The Fearless/Energetic",
}

# Student history for continuity
student_history = {
    "Student_1": ["Alice"],
    "Student_2": ["Alice", "Ben"],
    "Student_3": ["Cara"],
    "Student_4": ["Ben"]
}

# Classes (fixed instructors + style + capacity)
classes = {
    "Class_A": {"instructor": "Alice", "style": "Soft-Spoken", "capacity": 2},
    "Class_B": {"instructor": "Ben", "style": "High Energy", "capacity": 2},
    "Class_C": {"instructor": "Cara", "style": "Technique Driven", "capacity": 2}
}

# -------------------
# BUILD GRAPH
# -------------------

G = nx.Graph()

students = list(student_types.keys())
slot_nodes = []

# Expand each class into "slots" to handle capacity
for class_id, data in classes.items():
    for i in range(data["capacity"]):
        slot_node = f"{class_id}_slot_{i}"
        slot_nodes.append(slot_node)

# Add edges between each student and every slot
for student in students:
    swimmer_type = student_types[student]
    preferred_styles = swimmer_rules[swimmer_type]
    history = student_history.get(student, [])

    for class_id, data in classes.items():
        instructor = data["instructor"]
        style = data["style"]
        continuity_score = history.count(instructor)
        style_score = preferred_styles.count(style)
        total_score = continuity_score * CONTINUITY_MULTIPLIER + style_score

        if total_score > 0:
            for i in range(data["capacity"]):
                slot_node = f"{class_id}_slot_{i}"
                G.add_edge(student, slot_node, weight=total_score)

# -------------------
# MAX WEIGHT MATCHING
# -------------------

matching = nx.max_weight_matching(G, maxcardinality=True)

# -------------------
# FORMAT OUTPUT
# -------------------

assignments = {}
for a, b in matching:
    student = a if a in students else b
    slot = b if student == a else a
    class_name = slot.split("_slot_")[0]
    assignments[student] = class_name

# -------------------
# PRINT RESULTS
# -------------------

print("--- STUDENT → CLASS ASSIGNMENTS ---")
for student, cls in assignments.items():
    print(f"{student} → {cls}")
