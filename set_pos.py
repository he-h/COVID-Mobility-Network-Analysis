import json

with open("data/pos.json", 'r') as s:
    pos = json.load(s)

with open("data/MSAfips.json", 'r') as s:
    fips = json.load(s)


new_loc = dict()

for i in fips.keys():
    loc = [pos[j] for j in fips[i]]
    print(loc)
    new_loc[i] = [sum(k)/len(loc) for k in zip(*loc)]
    print(new_loc[i])

with open('data/loc.json', 'w') as s:
    json.dump(new_loc, s)
