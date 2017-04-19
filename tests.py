from lime import LiMeApi
import unittest
import json

class ApiTest(unittest.TestCase):
    base_node = "thisnode.info"
    user = r"admin"
    password = r"admin"

    @classmethod
    def setUpClass(cls):
        cls.ws = LiMeApi(base_node=cls.base_node, user=cls.user, password=cls.password)
        cls.ws.list_methods()
        challenge_res = cls.ws.challenge()
        cls.ws.login(challenge_res)

    @classmethod
    def tearDownClass(cls):
        cls.ws.close()

    def test_list_methods(self):
        res = self.ws.list_methods()

    def test_get_hostname(self):
        res = self.ws.get_hostname()
        self.assertEqual(res["status"], "ok")

    def test_get_location(self):
        res = self.ws.get_location()
        self.assertEqual(res["status"], "ok")

    def test_set_location(self):
        res = self.ws.get_location()
        lat = res["lat"]
        lon = res["lon"]
        self.ws.set_location(lat, lon)

    def test_get_neighbors(self):
        res = self.ws.get_neighbors()
        self.assertEqual(res["status"], "ok")
        
    def test_get_interfaces(self):
        res = self.ws.get_interfaces()
        self.assertEqual(res["status"], "ok")

    def test_get_assoclist(self):
        res = self.ws.get_interfaces()
        iface = res["interfaces"][0]
        res = self.ws.get_assoclist(iface)
        self.assertEqual(res["status"], "ok")
    
    def test_get_iface_stations(self):
        res = self.ws.get_interfaces()
        iface = res["interfaces"][0]
        res = self.ws.get_iface_stations(iface)
        self.assertEqual(res["status"], "ok")

    def test_get_station_signal(self):
        res = self.ws.get_interfaces()
        iface = res["interfaces"][0]
        res = self.ws.get_iface_stations(iface)
        station = res["stations"].popitem()[1]["mac"]
        res = self.ws.get_station_signal(iface, station)
        
        self.assertEqual(res["status"], "ok")

    def test_get_stations(self):
        res = self.ws.get_stations()
        self.assertEqual(res["status"], "ok")

    def test_get_gateway(self):
        res = self.ws.get_gateway()
        self.assertEqual(res["status"], "ok")

    def test_get_path(self):
        res = self.ws.get_gateway()
        gateway = res["gateway"]
        res = self.ws.get_path(gateway)
        self.assertEqual(res["status"], "ok")
        path = res["path"]

    def test_get_metrics(self):
        res = self.ws.get_gateway()
        gateway = res["gateway"]
        res = self.ws.get_metrics(gateway)
        self.assertEqual(res["status"], "ok")

    def test_get_internet_path_metrics(self):
        res = self.ws.get_internet_path_metrics()
        self.assertEqual(res["status"], "ok")

if __name__ == '__main__':
    unittest.main()
