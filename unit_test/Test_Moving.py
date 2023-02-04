import unittest
import os, sys, json
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
from train_simulation.Rail_Transport import Train, Carrier
from train_simulation.Simulation import Simulation
from train_simulation.Person import Person
from train_simulation.Algorithms import Algorithms
from datetime import datetime


class Test_moving(unittest.TestCase):

    def test_move_to_over_capacity(self):
        sim = Simulation(52,datetime(2018, 10, 22, 0, 0, 0), True)
        algo = Algorithms(sim.connections, sim.stations, sim.lines)

        train = sim.trains['0']
        train.arriveAt(sim.stations['Hillerød'],10,0)

        passengers = []
        for i in range(750):
            passenger = Person('Hillerød','København H',datetime.now(), i)
            passengers.append(passenger)
            path = algo.get_path_trains(passenger.start_station,passenger.destination)      
            passenger.setPath(path)

        sim.stations['Hillerød'].add_passengers(passengers)
        
        
        time = 30
        totalTime = 0
        train.moveTo(sim.stations['Allerød'],sim.connections[('Hillerød','Allerød')].distance, time, datetime.now(),False)

        print(len(train._passengers),len(sim.stations['Hillerød'].get_passengers()))
        self.assertTrue(len(train._passengers) == 700 and len(sim.stations['Hillerød'].get_passengers()) == 50)

        for i in range(10):
            if train._moving:
                train.keepMoving(time, totalTime)

        self.assertTrue(train._moving == False, train._atStation == sim.stations['Allerød'] and len(train._passengers) == 0)

    def test_move_to(self):

        sim = Simulation(52,datetime(2018, 10, 22, 0, 0, 0), True)
        algo = Algorithms(sim.connections, sim.stations, sim.lines)

        train = sim.trains['0']
        train.arriveAt(sim.stations['Hillerød'],10,0)


        passengers = []
        for i in range(699):
            passenger = Person('Hillerød','Allerød',datetime.now(), i)
            passengers.append(passenger)
            path = algo.get_path_trains(passenger.start_station,passenger.destination)      
            passenger.setPath(path)

        sim.stations['Hillerød'].add_passengers(passengers)
        

        time = 30
        totalTime = 0

        train.moveTo(sim.stations['Allerød'],sim.connections[('Hillerød','Allerød')].distance, time, datetime.now(), False)
        
        self.assertTrue(len(train._passengers) == 699 and len(sim.stations['Hillerød'].get_passengers()) == 0)

        for i in range(10):
            if train._moving:
                train.keepMoving(time, totalTime)
        
        print(train._moving == False,train._atStation.name,len(train._passengers))
        self.assertTrue(train._moving == False and train._atStation == sim.stations['Allerød'] and len(train._passengers) == 0)



    def test_carrier_move_to_over_capacity(self):
        sim = CarrierSimulation(100,['København H'],datetime(2018, 10, 22, 0, 0, 0), True)
        algo = Algorithms(sim.connections, sim.stations, sim.lines)

        carrier = sim.stations['Hillerød'].carriers[0]

        passengers = []
        for i in range(10):
            passenger = Person('Hillerød','Allerød',datetime.now(), i)
            passengers.append(passenger)
            path = algo.get_path(passenger.start_station,passenger.destination)      

        sim.stations['Hillerød'].add_passengers(passengers)
        

        time = 30
        totalTime = 0

        carrier.moveTo(sim.stations['Allerød'],sim.connections[('Hillerød','Allerød')].distance, time, datetime.now(), False)

        self.assertTrue(len(carrier._passengers) == 5 and len(Stations['Hillerød'].get_passengers()) == 5)

        for i in range(10):
            if carrier._moving:
                carrier.keepMoving(time, totalTime)

        self.assertTrue(
            carrier._moving == False and carrier._atStation == sim.stations['Allerød'] and len(carrier._passengers) == 0)

    def test_carrier_move_to(self):

        sim = CarrierSimulation(100,['København H'],datetime(2018, 10, 22, 0, 0, 0), True)
        algo = Algorithms(sim.connections, sim.stations, sim.lines)

        carrier = sim.stations['Hillerød'].carriers[0]

        passengers = []
        for i in range(4):
            passenger = Person('Hillerød','Allerød',datetime.now(), i)
            passengers.append(passenger)
            path = algo.get_path(passenger.start_station,passenger.destination)      

        sim.stations['Hillerød'].add_passengers(passengers)
        

        time = 30
        totalTime = 0

        carrier.moveTo(sim.stations['Allerød'],sim.connections[('Hillerød','Allerød')].distance, time, datetime.now(), False)

        self.assertTrue(len(carrier._passengers) == 4 and len(Stations['Hillerød'].get_passengers()) == 0)

        for i in range(10):
            if carrier._moving:
                carrier.keepMoving(time, totalTime)

        self.assertTrue(
            carrier._moving == False and carrier._atStation == sim.stations['Allerød'] and len(carrier._passengers) == 0
            )

    def test_accelerate(self):
        sim = Simulation(52,datetime(2018, 10, 22, 0, 0, 0), True)
        train = sim.trains['0']
        train._accelerateTo = 100
        train.accelerate(1)
        self.assertTrue(train._speed == 1.3)   
    
    def test_decelerate(self):
        sim = Simulation(52,datetime(2018, 10, 22, 0, 0, 0), True)
        train = sim.trains['0']
        train._speed = 100
        train.decelerate(1)
        self.assertTrue(train._speed == 98.8)

    def test_calcAccelerate(self):
        sim = Simulation(52,datetime(2018, 10, 22, 0, 0, 0), True)
        sim.trains['0']
        train = sim.trains['0']
        self.assertTrue(train.calculateAccelerateTo(100) < 11)
        

if __name__ == "__main__":
    unittest.main()