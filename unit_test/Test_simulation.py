from unittest.mock import MagicMock
import os, sys, unittest
import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
from train_simulation.Central_Communication import Simulation, CarrierSimulation
from train_simulation.Railway import Stations

class Test_simulation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sim = Simulation(5000, datetime.datetime(2022, 9, 24, 0, 0, 0), True)

        sim.plt.show = MagicMock()
        sim.animator.FuncAnimation = MagicMock()
        sim.run_simulation_with_animation(10, 10, output_fig=False)

    def test_animation_rendering(self):
        sim = Simulation(5000, datetime.datetime(2022, 9, 24, 0, 0, 0), True)
        sim.animator.FuncAnimation()

    def test_visualization_showing(self):
        sim = Simulation(5000, datetime.datetime(2022, 9, 24, 0, 0, 0), True)
        sim.plt.show.assert_called()
    
    def test_loadbalancer(self):
        sim = CarrierSimulation(0, ['Køge'], datetime.datetime.now(), True)
        time = 0
        
        sim.loadbalanceGenerator(time)
        old = len((sim.stations["Køge"].carriers))
        sim.loadbalance(time)
        new = len((sim.stations["Køge"].carriers))
        self.assertTrue(new < old)


unittest.main()