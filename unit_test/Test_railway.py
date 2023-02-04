import unittest
import os, sys, json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)

from train_simulation.Railway import Station, Connection, Stations, Connections, Lines

dummy_stations = """[
    {
        "name": "station a",
        "x": 0,
        "y": 0,
        "idle_time": 0,
        "passengers": 0,
        "is_last_station": true,
        "lines": ["a"]
    },
    {
        "name": "station b",
        "x": 0,
        "y": 0,
        "idle_time": 0,
        "passengers": 0,
        "is_last_station": true,
        "lines": ["a"]
    },
    {
        "name": "station c",
        "x": 0,
        "y": 0,
        "idle_time": 0,
        "passengers": 0,
        "is_last_station": true,
        "lines": ["b"]
    }
]"""

dummy_connections = """[
    {"station A": "station a", "station B": "station b", "distance": 0},
    {"station A": "station c", "station B": "station a", "distance": 0}
]"""


class Test_railway(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        json.loads(dummy_stations, object_hook=Station.from_json)
        json.loads(dummy_connections, object_hook=Connection.from_json)

    def test_stations(self):
        self.assertEqual(list(Stations.keys()), ['station a', 'station b', 'station c'])

    def test_connections(self):
        self.assertIn(('station a', 'station b'), Connections)
        self.assertIn(('station b', 'station a'), Connections)
        self.assertIn(('station a', 'station c'), Connections)
        self.assertNotIn(('station b', 'station c'), Connections)
        self.assertNotIn(('station c', 'station c'), Connections)

    def test_lines(self):
        self.assertEqual(Lines["a"],['station a', 'station b'])
        self.assertEqual(Lines["b"],['station c'])
        self.assertEqual(Lines["c"],[])

unittest.main()
