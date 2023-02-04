import json, os, sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
connections_file = open(os.path.join(dirname, '../assets/connections.json'), mode="r", encoding="utf-8")
line_file = open(os.path.join(dirname, '../assets/lines.json'), mode="r", encoding="utf-8")
station_file = open(os.path.join(dirname, '../assets/stations.json'), mode="r", encoding="utf-8")
lines = json.load(line_file)
connections = json.load(connections_file)
station = json.load(station_file)
new_connections_file = open(os.path.join(dirname, '../assets/new_connections.json'), mode="w", encoding="utf-8")
new_connections = []

def find_distance(c1, c2):
    for c in connections:
        if((c['station A'] == c1 and c['station B'] == c2) or (c['station B'] == c1 and c['station A']==c2)):
            first = min(c1,c2)
            second = max(c1,c2)
            new_connections.append({'station A':first, 'station B':second, 'distance': c['distance']})
            return c['distance']
    first = min(c1,c2)
    second = max(c1,c2)
    new_connections.append({'station A':first, 'station B':second, 'distance': 0})
    return None

def remove_duplicates(list):
    tmp = []
    for i in list:
        if i not in tmp:
            tmp.append(i)
    return tmp

for l in lines:
    aux = [0]+lines[l]
    for current, next in zip(aux, lines[l]):
        if current != 0:
            if current not in station.keys():
                print('missing station: '+ current)
            if (current!=0):
                print(find_distance(current,next))
                
new_connections=remove_duplicates(new_connections)
json_object = json.dumps(new_connections, indent=4, ensure_ascii=False)
new_connections_file.write(json_object)