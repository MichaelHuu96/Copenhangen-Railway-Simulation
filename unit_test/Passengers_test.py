import unittest
import json, os, sys
from datetime import datetime, timedelta

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)

from train_simulation.Person import Person,create_passengers
from train_simulation.Central_Communication import Simulation
from train_simulation.Algorithms import Algorithms

class TestPassenger(unittest.TestCase):
    def test_create_person(self):
        p = Person('start_station', 'destination', datetime.now(),1)
        self.assertEqual(p.start_station, 'start_station')
        self.assertEqual(p.destination, 'destination')
        self.assertEqual(p.isArrived, False)
        self.assertEqual(p.end_time, None)
        self.assertEqual(p.travel_time, None)
        self.assertEqual(p.start_time.strftime('%Y-%m-%d'),datetime.today().strftime('%Y-%m-%d'))
        self.assertEqual(p.id, 1)
        self.assertEqual(p.path, [])
        self.assertEqual(p.remainingPath, [])
        self.assertEqual(p.intermediateDestination, '')
        self.assertEqual(p.atStation, '')

    def test_setPath(self):
        p = Person('Hillerød', 'Allerød', datetime.now(), 'bob')
        sim = Simulation(52, datetime(2018, 10, 22, 0, 0, 0), True)
        algo = Algorithms(sim.connections, sim.stations, sim.lines)
        path = algo.get_path_trains(p.start_station, p.destination)
        p.setPath(path)
        self.assertEqual(p.path, path)
        self.assertEqual(p.remainingPath, path)
        self.assertEqual(p.intermediateDestination, path[0]["path"][-1])

    def test_updatePath(self):
        p = Person('Hillerød', 'Birkerød', datetime.now(), 'bob')
        sim = Simulation(52, datetime(2018, 10, 22, 0, 0, 0), True)
        algo = Algorithms(sim.connections, sim.stations, sim.lines)
        path = algo.get_path_trains(p.start_station, p.destination)
        p.setPath(path)
        p.updatePath((datetime.now()), 'Allerød')
        p.updatePath((datetime.now()), 'Birkerød')
        self.assertEqual(p.isArrived, True)
        self.assertEqual(p.travel_time, (p.end_time - p.start_time))
    def test_arrived(self):
        p = Person('Hillerød', 'Birkerød', datetime.now(), 'bob')
        p.arrived(datetime.now())
        self.assertEqual(p.isArrived, True)
        self.assertEqual(p.travel_time, (p.end_time - p.start_time))
    def test_is_arrived(self):
        p = Person('Hillerød', 'Birkerød', datetime.now(), 'bob')
        p.arrived(datetime.now())
        self.assertEqual(p.isArrived, True)

    def test_create_passengers(self):
        critical_stations =["Hillerød","Lyngby","Gentofte","Køge","Herlev"]
        today =  datetime.now()
        tomorrow = datetime.now() + timedelta(days=1)
        time={'start': today,'end':tomorrow}
        ps = create_passengers(critical_stations,datetime(2018, 10, 22, 6, 0, 0), datetime(2018, 10, 22, 23, 59, 59),100)
        self.assertEqual(len(ps), 100)

    def test_create_json_file(self):
        with open(os.path.join(dirname, '../assets/passengers.json'),  encoding="utf-8") as json_file:
            data = json.load(json_file)

            for element in data: # delete all file content to make sure it is an empty file
                del element
        critical_stations = ["Hillerød", "Lyngby", "Gentofte", "Køge", "Herlev"]
        today = datetime.now()
        tomorrow = datetime.now() + timedelta(days=1)
        time = {'start': today, 'end': tomorrow}
        create_passengers(critical_stations, datetime(2018, 10, 22, 6, 0, 0), datetime(2018, 10, 22, 23, 59, 59), 100)
        with open(os.path.join(dirname, '../assets/passengers.json'),  encoding="utf-8") as json_file:
            data = json.load(json_file)
        self.assertEqual(len(data), 100)


if __name__ == '__main__':
    unittest.main()