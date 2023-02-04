# from others.simulation_skeleton import Person
import json, os, sys, uuid, calendar

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
from train_simulation.Railway import Station

from datetime import datetime, timedelta
import random
from faker import Faker

# from Railway import Station
Passengers = []
Reached = {new_list: [] for new_list in range(1440)}

def getFirstPersonTime():
    return min(Passengers, key=lambda x: x.get_start_time()).get_start_time()

class Person:
    def __init__(
        self, start_station, destination, start_time, uid
    ):  # I think that start station wil be good for us to generate report- can deleted if you are not agree
        self.id = uid
        self.start_station = start_station
        self.destination = destination
        self.isArrived = False
        self.start_time = start_time
        self.end_time = None
        self.travel_time = None
        self.intermediateDestination = ""
        self.atStation = ""
        self.path = []
        self.remainingPath = []
        Passengers.append(self)

    def __str__(self):
        return self.id

    @staticmethod
    def from_json(json_dct):
        Person(
            json_dct["start_station"],
            json_dct["destination"],
            datetime.strptime(json_dct["start_time"], "%Y-%m-%d %H:%M:%S"),
            json_dct["id"],
        )

    @staticmethod
    def create_passengers(critical_stations, time_start, time_end, n_passengers):
        time_start = time_start.replace(microsecond=0)
        time_end = time_end.replace(microsecond=0)

        new_stations_file = open(
            os.path.join(dirname, "../assets/new_stations.json"),
            mode="r",
            encoding="utf-8",
        )
        stations_json = json.load(new_stations_file)
        stations = [x["name"] for x in stations_json]

        rush_hours_weight = 5  # 500% of passengers will be for rush hours
        critical_stations_weight = 0.25  # 25% of the passengers will be directed to critical stations (perhaps  set it at the constructor?)

        rush_hours_passengers = round(
            rush_hours_weight * (n_passengers / (rush_hours_weight + 1))
        )
        out_rush_hours_passengers = n_passengers - rush_hours_passengers
        critical_rush_hours = round(rush_hours_passengers * critical_stations_weight)
        critical_out_rush_hours = round(
            out_rush_hours_passengers * critical_stations_weight
        )

        passengers_list = []
        fake = Faker()

        rush_hours = []
        out_rush_hours = []
        time_stamp = time_start
        while time_stamp < time_end:
            if time_stamp.hour >= 7 and time_stamp.hour < 11:
                rush_hours.append(time_stamp)
            elif time_stamp.hour >= 13 and time_stamp.hour < 18:
                rush_hours.append(time_stamp)
            else:
                out_rush_hours.append(time_stamp)
            time_stamp += timedelta(seconds=1)

        def add_passenger_to(station, possible_times):
            start_station = random.choice(station)
            destination = random.choice(stations)
            while start_station == destination:
                destination = random.choice(stations)
            travel_time = random.choice(possible_times)
            passengers_list.append(
                Person(start_station, destination, travel_time, fake.name())
            )

        for i in range(critical_rush_hours):  # critical + rush
            add_passenger_to(critical_stations, rush_hours)

        for i in range(rush_hours_passengers - critical_rush_hours):  # rush
            add_passenger_to(stations, rush_hours)

        for i in range(critical_out_rush_hours):  # critical
            add_passenger_to(critical_stations, out_rush_hours)

        for i in range(out_rush_hours_passengers - critical_out_rush_hours):  # nothing
            add_passenger_to(stations, out_rush_hours)

        json_string = json.dumps(
            [
                {
                    "id": p.id,
                    "start_time": str(p.start_time),
                    "start_station": p.start_station,
                    "destination": p.destination,
                }
                for p in passengers_list
            ],
            indent=4,
            ensure_ascii=False,
        )
        with open(
            os.path.join(dirname, "../assets/passengers.json"),
            mode="w",
            encoding="utf-8",
        ) as outfile:
            outfile.write(json_string)
        return passengers_list
    
    def arrived(self, arriveTime):
        self.isArrived = True
        self.end_time = arriveTime
        self.travel_time = (self.end_time - self.start_time).total_seconds()
        # print(self.start_time, self.end_time, self.travel_time)
        Reached[self.start_time.hour*60+self.start_time.minute].append(self.travel_time)

    def isArrived(self):
        return self.isArrived

    def getTravelTime(self):
        return self.travel_time

    def delete_person(self):
        del self

    def get_destination(self):
        return self.destination

    def get_start_time(self):
        return self.start_time

    def getlocation(self):
        return self._currentlocation

    def getid(self):
        return self._id

    def setdestination(self, newdestination):
        self.destination = newdestination

    def printInformation(self):
        print(f"current location: {self._currentlocation}")
        print(f"destination: {self.destination}")
        print(f"departuretime: {self._departureTime}")
        if self.isArrived:
            print(f"travel time: {self._travelTime}")


# Person.create_passengers(
#     ["Lyngby", "Nørreport", "Værløse", "København H"],
#     datetime(2022,9,24),
#     datetime(2022,9,24) + timedelta(hours=24),
#     125000 ,
# )
