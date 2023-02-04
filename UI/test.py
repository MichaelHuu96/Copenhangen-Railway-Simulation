import json
model = {}
trains = []
uid = 1234
atStation = "Køge"
moveTo = "Ølby"
line = ['A','B']

for i in range(3):
    trains.append({"uid":uid, "atStation":atStation, "moveTo":moveTo,"line":line})
model["trains"] = trains
json_object = json.dumps(model, indent=4, ensure_ascii=False)
print(json_object)