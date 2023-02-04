import unittest
import os, sys, json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
from train_simulation.Algorithms import Algorithms
from train_simulation.Railway import Station, Connection, Stations, Connections, Lines



class Test_algorithms(unittest.TestCase):
    def test_get_path(self):
        stations_file = open(
            os.path.join(dirname, "../assets/new_stations.json"),
            mode="r",
            encoding="utf-8",
        )
        json.load(stations_file, object_hook=Station.from_json)

        new_connections_file = open(
            os.path.join(dirname, "../assets/new_connections.json"),
            mode="r",
            encoding="utf-8",
        )
        json.load(new_connections_file, object_hook=Connection.from_json)

        algo = Algorithms(Connections, Stations, Lines)
        self.assertEqual(
            algo.get_path("Lyngby", "Malmparken").nodes,
            [
                "Lyngby",
                "Jærgersborg",
                "Gentofte",
                "Bernstorffsvej",
                "Hellerup",
                "Ryparken",
                "Bispebjerg",
                "Nørrebro",
                "Fuglebakken",
                "Grøndal",
                "Flintholm",
                "Vanløse",
                "Jyllingevej",
                "Islev",
                "Husum",
                "Herlev",
                "Skovlunde",
                "Malmparken",
            ],
        )
        self.assertEqual(
            algo.get_path("Bispebjerg", "Hillerød").nodes,
            [
                "Bispebjerg",
                "Ryparken",
                "Hellerup",
                "Bernstorffsvej",
                "Gentofte",
                "Jærgersborg",
                "Lyngby",
                "Sorgenfri",
                "Virum",
                "Holte",
                "Birkerød",
                "Allerød",
                "Hillerød",
            ],
        )

    def test_get_path_trains(self):
        stations_file = open(
            os.path.join(dirname, "../assets/new_stations.json"),
            mode="r",
            encoding="utf-8",
        )
        json.load(stations_file, object_hook=Station.from_json)

        new_connections_file = open(
            os.path.join(dirname, "../assets/new_connections.json"),
            mode="r",
            encoding="utf-8",
        )
        json.load(new_connections_file, object_hook=Connection.from_json)

        algo = Algorithms(Connections, Stations, Lines)
        self.assertEqual(
            algo.get_path_trains("Lyngby", "Malmparken"),
            [
                {
                    "line": "a",
                    "path": [
                        "Lyngby",
                        "Jærgersborg",
                        "Gentofte",
                        "Bernstorffsvej",
                        "Hellerup",
                    ],
                },
                {
                    "line": "f",
                    "path": [
                        "Hellerup",
                        "Ryparken",
                        "Bispebjerg",
                        "Nørrebro",
                        "Fuglebakken",
                        "Grøndal",
                        "Flintholm",
                    ],
                },
                {
                    "line": "c",
                    "path": [
                        "Flintholm",
                        "Vanløse",
                        "Jyllingevej",
                        "Islev",
                        "Husum",
                        "Herlev",
                        "Skovlunde",
                        "Malmparken",
                    ],
                },
            ],
        )
        self.assertEqual(
            algo.get_path_trains("Bispebjerg", "Hillerød"),
            [
                {"line": "f", "path": ["Bispebjerg", "Ryparken", "Hellerup"]},
                {
                    "line": "a",
                    "path": [
                        "Hellerup",
                        "Bernstorffsvej",
                        "Gentofte",
                        "Jærgersborg",
                        "Lyngby",
                        "Sorgenfri",
                        "Virum",
                        "Holte",
                        "Birkerød",
                        "Allerød",
                        "Hillerød",
                    ],
                },
            ],
        )



if __name__ == "__main__":
    unittest.main()
