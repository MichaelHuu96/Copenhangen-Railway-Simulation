# from others.simulation_skeleton import Person
import json, os, sys, uuid, calendar

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
from train_simulation.Railway import Station

from datetime import datetime, timedelta
import random


# from Railway import Station


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

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
    #fake = Faker()

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
            Person(start_station, destination, str(travel_time), "fake.name()")
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
                "start_time": p.start_time,
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


class Person:
    def __init__(self, start_station, destination, start_time, id):  # I think that start station wil be good for us to generate report- can deleted if you are not agree
        self.start_station = start_station
        self.destination = destination
        self.isArrived = False
        self.start_time = start_time
        self.end_time = None
        self.travel_time = None
        self.id = id
        self.path = []
        self.remainingPath = []
        self.intermediateDestination = ""
        self.atStation = ""
        self.timeSpentWaiting = timedelta(seconds=0)
        self.timeSinceBegunWaiting = start_time

    def updateTimeSpentWaiting(self,time):
        self.timeSpentWaiting += time - self.timeSinceBegunWaiting

    def updateTimeSinceBegunWaiting(self,time):
        self.timeSinceBegunWaiting = time

        
    def setPath(self,path):
        self.path = path
        self.remainingPath = path[:]
        self.intermediateDestination = self.remainingPath[0]["path"][-1]

    def updatePath(self, arriveTime, station):
        if self.destination == self.intermediateDestination:
            self.arrived(arriveTime)
        else:
            self.updateTimeSinceBegunWaiting(arriveTime)
            self.remainingPath.pop(0)
            self.intermediateDestination = self.remainingPath[0]["path"][-1]
            station.add_passenger(self)

    def arrived(self, arriveTime):
        self.isArrived = True
        self.end_time = arriveTime
        self.travel_time = (self.end_time - self.start_time)

    def isArrived(self):
        return self.isArrived
    
    def delete_person(self):
        del self

    def ride_duration(self):
        return self.end_time - self.time

    def getdestination(self):
        return self.destination

    def getid(self):
        return self.id

    def getTravelTime(self):
        return self.travel_time

    def setdestination(self, newdestination):
         self._destination = newdestination
    
    def setlocation(self, newlocation):
         self._destination = newlocation
    
    def setdepartureTime(self, newdepartueTime):
         self._destination = newdepartueTime
        
    def printInformation(self):
        print(f"id: {self._id}")
        print(f"current location: {self._currentlocation}")
        print(f"destination: {self._destination}")
        print(f"departuretime: {self._departureTime}")
        if self._isArrived:
            print(f"travel time: {self._travelTime}")
