
from dijkstar import Graph, find_path

class Algorithms:

    def __init__(self, connections, stations):
        self.connections = connections
        self.stations = stations
        self.stationGraph = Graph()
        for _,connectionDic  in connections.items():
            for _,connection  in connectionDic.items():
                self.stationGraph.add_edge(connection.station_start.name,connection.station_end.name , (connection.distance,connection.station_end.name))
                self.stationGraph.add_edge(connection.station_end.name,connection.station_start.name , (connection.distance,connection.station_start.name))

    def cost_func(self, u, v, edge, prev_edge):
        length, name = edge
        if prev_edge:
            prev_name = prev_edge[1]
        else:
            prev_name = None
        cost = length
        if name != prev_name:
            cost += 1
        return cost
    
    def get_path(self, station_a, station_b):
        return(find_path(self.stationGraph, station_a, station_b , cost_func=self.cost_func))

                



