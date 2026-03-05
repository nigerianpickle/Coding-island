from collections import Counter


# DATA
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

# HELPERS
#For each student in a class we see which instructors they had before and tally the votes
def continuity_votes(students):
    votes = []
    for s in students:
        votes.extend(student_history.get(s, []))
        
    #return a count of how many times a student in a class had each instructor before
    return Counter(votes)


#For each student in a class we see their swimmer type and tally the total votes for instructor styles
def style_votes(students):
    votes = []
    for s in students:
        #Get the swimmer type of the student
        swimmer_type = student_types[s]
        votes.extend(swimmer_rules[swimmer_type])
    return Counter(votes)


# MATCHING ENGINE
assignments = {}
used_instructors = set()


#Loop over each class to assign the best instructor
for class_id, students in classes.items():

    cont = continuity_votes(students)
    style = style_votes(students)

    print(f"\nClass {class_id}")
    print("Continuity votes:", cont)
    print("Style votes:", style)

    best_inst = None
    best_score = -1

    #Go through each instructor to find the best match
    for inst in instructors:
        name = inst["name"]

        # Instructor already teaching another class
        if name in used_instructors:
            continue
        
        #Get the instructor score 
        continuity_score = cont.get(name, 0)
        style_score = style.get(inst["style"], 0)

        # Continuity has way higher priority than style
        score = continuity_score * CONTINUITY_MULTIPLIER + style_score

        print(f"Checking {name}: continuity={continuity_score}, style={style_score}, total={score}")

        if score > best_score:
            best_score = score
            best_inst = name

    if best_inst:
        assignments[class_id] = best_inst
        used_instructors.add(best_inst)


# OUTPUT
print("\nFINAL CLASS → INSTRUCTOR ASSIGNMENTS")
for cls, inst in assignments.items():
    print(f"{cls} → {inst}")
