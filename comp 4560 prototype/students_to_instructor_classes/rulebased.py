from collections import Counter

CONTINUITY_MULTIPLIER = 10

swimmer_rules = {
    "The Nervous/New": ["New RSS/Babies", "High Energy", "Soft-Spoken"],
    "The Fearless/Energetic": ["High Energy", "Technique Driven"],
    "The Hard Worker": ["Technique Driven", "DIA"],
    "The Socialite/Talker": ["Technique Driven", "Soft-Spoken", "High Energy"],
    "The Natural": ["Technique Driven", "Soft-Spoken"],
    "The Slow Progress": ["Adapted", "Technique Driven", "High Energy"],
    "Not Used to 'No'": ["DIA", "Adapted"]
}

student_types = {
    "Student_1": "The Nervous/New",
    "Student_2": "The Hard Worker",
    "Student_3": "The Slow Progress",
    "Student_4": "The Fearless/Energetic",
    "Student_5": "The Natural"
}

student_history = {
    "Student_1": ["Alice"],
    "Student_2": ["Alice", "Ben"],
    "Student_3": ["Cara"],
    "Student_4": ["Ben"]
}

classes = {
    "Class_A": {"instructor": "Alice", "style": "Soft-Spoken", "capacity": 1, "students": []},
    "Class_B": {"instructor": "Ben", "style": "High Energy", "capacity": 2, "students": []},
    "Class_C": {"instructor": "Cara", "style": "Technique Driven", "capacity": 2, "students": []}
}

# STEP 1 — PRIORITIZE students with continuity first
def continuity_priority(student):
    return len(student_history.get(student, []))

sorted_students = sorted(student_types.keys(), key=continuity_priority, reverse=True)

assignments = {}

print("\n--- MATCHING WITH CLASS CAPACITY ---")

for student in sorted_students:
    swimmer_type = student_types[student]
    preferred_styles = swimmer_rules[swimmer_type]
    history = student_history.get(student, [])

    best_class = None
    best_score = -1

    print(f"\nScoring {student}")

    for class_id, data in classes.items():
        # Skip full classes
        if len(data["students"]) >= data["capacity"]:
            continue

        instructor = data["instructor"]
        style = data["style"]

        style_score = preferred_styles.count(style)
        continuity_score = history.count(instructor)

        total_score = continuity_score * CONTINUITY_MULTIPLIER + style_score

        print(
            f"{class_id} → {instructor}, continuity={continuity_score}, "
            f"style={style_score}, total={total_score}"
        )

        if total_score > best_score:
            best_score = total_score
            best_class = class_id

    # Assign if possible
    if best_class:
        assignments[student] = best_class
        classes[best_class]["students"].append(student)

print("\n--- FINAL CLASS ROSTERS ---")
for class_id, data in classes.items():
    print(f"{class_id}: {data['students']}")
