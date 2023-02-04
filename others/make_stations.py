import json, os, sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
from train_simulation.Railway import Station, Connection, Stations, Connections

stations_file = open(os.path.join(dirname, '../assets/stations.json'), mode="r", encoding="utf-8")
lines_file = open(os.path.join(dirname, '../assets/lines.json'), mode="r", encoding="utf-8")
new_stations_file = open(os.path.join(dirname, '../assets/new_stations.json'), mode="w", encoding="utf-8")
stations = json.load(stations_file)
lines = json.load(lines_file)
a = lines['a-line']
b = lines['b-line']
c = lines['c-line']
f = lines['f-line']

def is_last_station(s):
    return s == a[0] or s == b[0] or s == c[0] or s == f[0] or s == a[-1] or s == b[-1] or s == c[-1] or s == f[-1] 

def get_lines(s):
    l = []
    if s in a:
        l.append('a')
    if s in b:
        l.append('b')
    if s in c:
        l.append('c')
    if s in f:
        l.append('f')
    return l

new_stations = []
for s in stations:
    new_station = {}
    new_station['name'] = s
    new_station['x'] = stations[s]['X']
    new_station['y'] = stations[s]['Y']
    new_station['idle_time'] = 30
    new_station['passengers'] = 0
    new_station['is_last_station'] = is_last_station(s)
    new_station['lines'] = get_lines(s)
    new_stations.append(new_station)

json_object = json.dumps(new_stations, indent=4, ensure_ascii=False)
new_stations_file.write(json_object)
new_stations_file.close()

#load and get dict all stations
new_stations_file = open(os.path.join(dirname, '../assets/new_stations.json'), mode="r", encoding="utf-8")
json.load(new_stations_file, object_hook=Station.from_json)
print(Stations['Hillerød'])

#load and get dict all connections
new_connections_file = open(os.path.join(dirname, '../assets/new_connections.json'), mode="r", encoding="utf-8")
json.load(new_connections_file, object_hook=Connection.from_json)
print(Connections[('Hillerød','Allerød')])
