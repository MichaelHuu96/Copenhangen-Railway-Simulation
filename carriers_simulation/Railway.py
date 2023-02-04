import json, simpy
from collections import defaultdict

Stations = {}
Connections = defaultdict(dict)
Lines = {'a':[], 'b':[], 'c':[], 'f':[]}

class Station():
    def __init__(self, name:str, x, y, passengers:int, idle_time, lines:[str], is_last_station:bool):
        self.name = name
        self.x = x
        self.y = y
        self.__idle_time = idle_time
        self.__lines = set(lines)
        self.__passengers = []
        self.__numberPassengers = 0
        self.__numberCarriers = 0
        self.__is_last_station = is_last_station
        self.CHAIN_STARTEGY = True
        Stations[name] = self
        for l in lines:
            Lines[l].append(name)

        # chain strategy
        self.request_empty_carriers = []

    def setEnvironment(self, env, capacity, simulation_start):
        self.__env = env
        self.loader = simpy.Resource(self.__env, capacity=capacity)
        self.__simulation_start = simulation_start

    def enqueue(self, carrier):
        yield self.__env.process(carrier.stop_in(self))

    def loadPassenger(self, passenger):
        delta = (passenger.get_start_time() - self.__simulation_start)
        yield self.__env.timeout(delta.total_seconds())
        self.__passengers.append(passenger)
        self.__numberPassengers+=1

    def getPassengers(self, carrier, max_passengers):
        while not self.__passengers:
            yield self.__env.timeout(1)
        main_passenger = self.__passengers.pop(0)
        carrier._passengers.append(main_passenger)
        carrier._destination = main_passenger.get_destination()
        if self.CHAIN_STARTEGY:
            Stations[main_passenger.get_destination()].request_empty_carriers.append(self.name)
        for p in self.__passengers:
            if len(carrier._passengers)>=max_passengers:
                break
            if p.get_destination() == carrier._destination:
                carrier._passengers.append(p)

    def sendEmptyCarrier(self, carrier):
        carrier._passengers = []
        carrier._destination = self.request_empty_carriers.pop(0)

    @staticmethod
    def processPassengers(env, passengers):
        for p in passengers:
            env.process(Stations[p.start_station].loadPassenger(p))

    # for info printing
    def __str__(self):
        return f"""
            "name": {self.name},
            "x": {self.x},                                                                                                                                                                                                                                                                                                  
            "y": {self.y},
            "idle_time": {self.get_idle_time()},
            "passengers": {self.get_passengers()},
            "is_last_station": {self.is_last_station()},
            "lines": {self.get_lines()}"""

    def get_passengers(self)->list:
        return self.__passengers

    def get_lines(self)->list:
        return self.__lines

    def is_last_station(self)->bool:
        return self.__is_last_station

    def get_idle_time(self)->int:
        return self.__passengers
    
    def sub_passengers(self, passengers):
        for passenger in passengers:
            self.__passengers.remove(passenger)

    def add_passenger(self,passenger):
        self.__passengers += [passenger]

    def sub_passenger(self,passenger):
        self.__passengers.remove(passenger)

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
        Connections[station_start][station_end] = self
        Connections[station_end][station_start] = self
    
    # for info printing
    def __str__(self):
        return f"""
            "station_start": {self.station_start.name},
            "station_end": {self.station_end.name},
            "distance": {self.distance}"""

    @classmethod
    def from_json(self, json_dct):
        Connection(json_dct['station A'],
                   json_dct['station B'],
                   json_dct['distance']),
        Connection(json_dct['station B'],
                   json_dct['station A'],
                   json_dct['distance'])

        
        
