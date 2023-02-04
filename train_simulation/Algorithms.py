
from dijkstar import Graph, find_path

class Algorithms:

    def __init__(self, connections, stations, lines):
        self.connections = connections
        self.stations = stations
        self.lines = lines
        self.stationGraph = Graph()
        for _,connection  in connections.items():
            self.stationGraph.add_edge(connection.station_start.name,connection.station_end.name , (connection.distance,connection.station_end.name))

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

    def get_path_trains(self, station_a, station_b):
        result = []
        path = find_path(self.stationGraph, station_a, station_b , cost_func=self.cost_func).nodes
        this_train = [path[0]]
        current = self.stations[path[0]]
        available_lines = current.get_lines()
        for s in path[1:]:
            next = self.stations[s]
            next_available_lines = next.get_lines() & available_lines
            if len(next_available_lines) == 0:
                # means should change train
                result.append({"line": available_lines, "path": this_train})
                available_lines = current.get_lines() & next.get_lines()
                this_train = [this_train[-1], s]
                current = next
            else:
                this_train.append(s)
                current = next
                available_lines = next_available_lines
        result.append({"line": available_lines, "path": this_train})
        return result
                