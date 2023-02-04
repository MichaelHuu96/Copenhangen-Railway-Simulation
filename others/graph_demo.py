import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
import json
import matplotlib.image as mpimg
import numpy as np
from matplotlib.animation import FuncAnimation

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)

from train_simulation.Railway import Station, Connection, Stations, Connections

def get_trace_points(point1, point2, step):
    l = np.arange (0, 1+step, step)
    return (l*point2[0]+(1-l)*point1[0]), (l*point2[1]+(1-l)*point1[1])

def update_point(n, x, y, point):
    point.set_data(np.array([x[n], y[n]]))
    return point

stations_file = open(os.path.join(dirname, '../assets/new_stations.json'), mode="r", encoding="utf-8")
json.load(stations_file, object_hook=Station.from_json)

new_connections_file = open(os.path.join(dirname, '../assets/new_connections.json'), mode="r", encoding="utf-8")
json.load(new_connections_file, object_hook=Connection.from_json)

fig, ax = plt.subplots()

G = nx.Graph()
for s in Stations:
    G.add_node(Stations[s].name, pos=(Stations[s].x, Stations[s].y))

pos=nx.get_node_attributes(G,'pos')
for c in Connections:
    G.add_edge(Connections[c].station_start.name, Connections[c].station_end.name, length = Connections[c].distance)


x, y = get_trace_points(pos["Hillerød"], pos["Allerød"], 0.1)
x0, y0 = get_trace_points(pos["Allerød"], pos["Birkerød"], 0.1)
x1, y1 = get_trace_points(pos["Birkerød"], pos["Holte"], 0.1)
x2, y2 = get_trace_points(pos["Holte"], pos["Virum"], 0.1)
x3, y3 = get_trace_points(pos["Virum"], pos["Sorgenfri"], 0.1)
x4, y4 = get_trace_points(pos["Sorgenfri"], pos["Lyngby"], 0.1)
x5, y5 = get_trace_points(pos["Lyngby"], pos["Jærgersborg"], 0.1)
x6, y6 = get_trace_points(pos["Jærgersborg"], pos["Gentofte"], 0.1)
x7, y7 = get_trace_points(pos["Gentofte"], pos["Bernstorffsvej"], 0.1)

x = np.concatenate((x,x0,x1,x2,x3,x4,x5,x6,x7))
y = np.concatenate((y,y0,y1,y2,y3,y4,y5,y6,y7))

train, = ax.plot([x[0]], [y[0]], 'x', color='r')
ani=FuncAnimation(fig, update_point, len(x), fargs=(x, y, train), interval=1)

nx.draw(G, pos, node_size=1, node_color='black')
img = mpimg.imread(os.path.join(dirname, '../assets/map_minmal.png'))
imgplot = plt.imshow(img)

plt.show()
