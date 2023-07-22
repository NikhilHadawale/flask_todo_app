import json

x={
    "fname":"Nikhil",
    "lname":"Hadawale",
    "cno":"+91 9595352080"
}

with open("data.json","w") as file:
    json.dump(x,file)

print("Data from File using json.load")

with open("data.json","r") as file:
    print(json.load(file))