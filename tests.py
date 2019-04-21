# Four Fundamental Forces with JSON
d = {}

d["gravity"] = {
    "mediator": "gravitons",
    "relative strength": "1",
    "range": "infinity"
}
d["weak"] = {
    "mediator": "W/Z bosons",
    "relative strength": "10^25",
    "range": "10^-18"
}
d["electromagnetic"] = {
    "mediator": "photons",
    "relative strength": "10^36",
    "range": "infinity"
}
d["strong"] = {
    "mediator": "gluons",
    "relative strength": "10^38",
    "range": "10^-15"
}

import json

# encoding to JSON
data = json.dumps(d)

# write to a file
with open("4forces.json", "w") as f:
    f.write(data)

# reads it back
with open("4forces.json", "r") as f:
    data = f.read()

# decoding the JSON to dictionay
d = json.loads(data)

print(d)
