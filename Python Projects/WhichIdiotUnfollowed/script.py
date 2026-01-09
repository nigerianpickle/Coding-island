import json

with open("following.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# This file ALWAYS stores followed accounts here
following_list = data["relationships_following"]

usernames = []

for item in following_list:
    # Instagram stores the username in "title"
    if "title" in item and item["title"]:
        usernames.append(item["title"])

# Print results
print(f"People you follow ({len(usernames)}):\n")
for username in usernames:
    print(username)




with open("followers_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

followers = {
    item["string_list_data"][0]["value"]
    for item in data
    if item.get("string_list_data")
}

print("HERE ARE YOUR FOLLOWERS")
print(len(followers))
for u in sorted(followers):
    print(u)
