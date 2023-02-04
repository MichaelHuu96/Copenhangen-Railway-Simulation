import json

Stations = {}
Connections = {}
Lines = {'a':[], 'b':[], 'c':[], 'f':[]}

class Station():

    def __init__(self, name:str, x, y, passengers:int, idle_time, lines:[str], is_last_station:bool):
        self.name = name
        self.x = x
        self.y = y
        self._idle_time = idle_time
        self._lines = set(lines)
        self._passengers = []
        self._numberCarriers = 0
        self._is_last_station = is_last_station
        self.carriers = []
        self.incomingCarriers = 0
        self.trainArrivalTimes = []
        Stations[name] = self
        for l in lines:
            Lines[l].append(name)

    # for info printing
    # def __str__(self):
    #     return f"""
    #         "name": {self.name},
    #         "x": {self.x},                                                                                                                                                                                                                                                                                                  
    #         "y": {self.y},
    #         "idle_time": {self.get_idle_time()},
    #         "passengers": {self.get_passengers()},
    #         "is_last_station": {self.is_last_station()},
    #         "lines": {self.get_lines()}"""

    def get_passengers(self)->list:
        return self._passengers

    def get_lines(self)->list:
        return self._lines

    def is_last_station(self)->bool:
        return self._is_last_station

    def get_idle_time(self)->int:
        return self._passengers

    def add_passengers(self, passengers):
        self._passengers += passengers
    
    def sub_passengers(self, passengers):
        for passenger in passengers:
            self._passengers.remove(passenger)

    def add_passenger(self,passenger):
        self._passengers += [passenger]

    def add_carrier(self, carrier):
        self.carriers.append(carrier)
        self._numberCarriers += 1

    def sub_carrier(self, carrier):
        self.carriers.remove(carrier)
        self._numberCarriers -= 1

    def sub_passenger(self,passenger):
        self._passengers.remove(passenger)


    def name(self):
        return self.name

    @staticmethod
    def from_json(json_dct):
        Station(json_dct["name"],
                    json_dct["x"],
                    json_dct["y"],
                    json_dct["passengers"],
                    json_dct["idle_time"],
                    json_dct["lines"],
                    json_dct["is_last_station"])


class Connection():
    def __init__(self, station_start, station_end, distance):
        self.station_start = Stations[station_start]
        self.station_end = Stations[station_end]
        self.distance = distance*1000
        Connections[(station_start, station_end)] = self
    
    # for info printing
    def __str__(self):
        return f"""
            "station_start": {self.station_start.name},
            "station_end": {self.station_start.name},
            "distance": {self.distance}"""

    @classmethod
    def from_json(self, json_dct):
        Connection(json_dct['station A'],
                   json_dct['station B'],
                   json_dct['distance']),
        Connection(json_dct['station B'],
                   json_dct['station A'],
                   json_dct['distance'])

        
        
