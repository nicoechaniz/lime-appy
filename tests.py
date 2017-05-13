from lime import LiMeApi
import unittest
import json
from jsonschema import validate

class ApiTest(unittest.TestCase):
    base_node = "thisnode.info"
    user = r"admin"
    password = r"admin"

    @classmethod
    def setUpClass(cls):
        cls.ws = LiMeApi(base_node=cls.base_node, user=cls.user, password=cls.password)
        cls.ws.verbosity = 0
        cls.ws._list_methods()
        challenge_res = cls.ws._challenge()
        cls.ws._login(challenge_res)

    @classmethod
    def tearDownClass(cls):
        cls.ws._close()

    def test_list_methods(self):
        res = self.ws._list_methods()

    def test_get_hostname(self):
        res = self.ws.get_hostname()
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "hostname": {"type": "string"},
            },
            "required": ["status","hostname"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_location(self):
        res = self.ws.get_location()
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "lon": {"type": "string"},
                "lat": {"type": "string"},
            },
            "required": ["status", "lon", "lat"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_set_location(self):
        res = self.ws.get_location()
        lat = res["lat"]
        lon = res["lon"]
        self.ws.set_location(lat, lon)

    def test_get_cloud_nodes(self):
        res = self.ws.get_cloud_nodes()
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "nodes": {"type": "array"},
            },
            "required": ["status", "nodes"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_interfaces(self):
        res = self.ws.get_interfaces()
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "interfaces": {"type": "array"},
            },
            "required": ["status", "interfaces"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_assoclist(self):
        res = self.ws.get_interfaces()
        iface = res["interfaces"][0]
        res = self.ws.get_assoclist(iface)
        schema = {
            "definitions": {
                "stations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "link_type": {"type": "string"},
                            "station_hostname": {"type": "string"},
                            "station_mac": {"type": "string"},
                            "attributes": {"$ref": "#/definitions/station_attributes"},
                        },
                        "required": ["link_type", "station_hostname", "station_mac", "attributes"]
                    },
                },
                "station_attributes": {
                    "type": "object",
                    "properties": {
                        "inactive": {"type": "number"},
                        "channel": {"type": "number"},
                        "signal": {"type": "string"}
                    },
                    "required": ["inactive", "channel", "signal"]
                },
            },
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "stations": {"$ref": "#/definitions/stations"},
            },
            "required": ["status", "stations"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_iface_stations(self):
        res = self.ws.get_interfaces()
        iface = res["interfaces"][0]
        res = self.ws.get_iface_stations(iface)
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "stations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "mac": {"type": "string"},
                            "iface": {"type": "string"},
                            "signal": {"type": "string"},
                            "hostname": {"type": "string"},
                            "rx_packets": {"type": "number"},
                            "tx_packets": {"type": "number"}
                        },
                        "required": ["mac", "iface", "signal", "hostname",
                                     "rx_packets", "tx_packets"]
                    }
                }
            },
            "required": ["status", "stations"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_station_signal(self):
        res = self.ws.get_interfaces()
        iface = res["interfaces"][0]
        res = self.ws.get_iface_stations(iface)
        station = res["stations"][0]["mac"]
        res = self.ws.get_station_signal(iface, station)
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "station": {"type": "string"},
                "signal": {"type": "string"}
            },
            "required": ["status", "station", "signal"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_station_traffic(self):
        res = self.ws.get_interfaces()
        iface = res["interfaces"][0]
        res = self.ws.get_iface_stations(iface)
        station = res["stations"][0]["mac"]
        res = self.ws.get_station_traffic(iface, station)
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "station": {"type": "string"},
                "rx_bytes": {"type": "number"},
                "tx_bytes": {"type": "number"},
            },
            "required": ["status", "station", "rx_bytes", "tx_bytes"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_stations(self):
        res = self.ws.get_stations()
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "stations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "mac": {"type": "string"},
                            "iface": {"type": "string"},
                            "signal": {"type": "string"},
                            "hostname": {"type": "string"},
                            "rx_packets": {"type": "number"},
                            "tx_packets": {"type": "number"}
                        },
                        "required": ["mac", "iface", "signal", "hostname",
                                     "rx_packets", "tx_packets"]
                    }
                }
            },
            "required": ["status", "stations"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_gateway(self):
        res = self.ws.get_gateway()
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "gateway": {"type": "string"},
            },
            "required": ["status","gateway"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_path(self):
        res = self.ws.get_gateway()
        gateway = res["gateway"]
        res = self.ws.get_path(gateway)
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "path": {"type": "array"},
            },
            "required": ["status","path"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_metrics(self):
        res = self.ws.get_gateway()
        gateway = res["gateway"]
        res = self.ws.get_metrics(gateway)
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "bandwidth": {"type": "string"},
                "loss": {"type": "string"}
            },
            "required": ["status","bandwidth","loss"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_internet_path_metrics(self):
        res = self.ws.get_internet_path_metrics()
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "metrics": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "hop": {"type": "number"},
                            "bandwidth": {"type": "string"},
                            "loss": {"type": "string"},
                            "hostname": {"type": "string"},
                        },
                        "required": ["hop", "bandwidth", "loss", "hostname"]
                    }
                }
            },
            "required": ["status", "metrics"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_last_internet_path(self):
        res = self.ws.get_last_internet_path()
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "path": {"type": "array"},
            },
            "required": ["status","path"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_internet_status(self):
        res = self.ws.get_internet_status()
        # orangerpc casts true and false to 1 and 0 respectively so types here is number instead of boolean
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "IPv4": {
                    "type": "object",
                    "properties": {
                        "working": {"type": "number"}
                    },
                    "required": ["working"]
                },
                "IPv6": {
                    "type": "object",
                    "properties": {
                        "working": {"type": "number"}
                    },
                    "required": ["working"]
                },
                "DNS": {
                    "type": "object",
                    "properties": {
                        "working": {"type": "number"}
                    },
                    "required": ["working"]
                },
            },
            "required": ["status", "IPv4", "IPv6", "DNS"]
            }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_node_status(self):
        res = self.ws.get_node_status()
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "hostname": {"type": "string"},
                "ips": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "version": {"type": "string"},
                            "address": {"type": "string"},
                        },
                        "required": ["version", "address"]
                    },
                },
                "most_active": {
                        "type": "object",
                        "properties": {
                            "mac": {"type": "string"},
                            "iface": {"type": "string"},
                            "signal": {"type": "string"},
                            "hostname": {"type": "string"},
                            "rx_packets": {"type": "number"},
                            "tx_packets": {"type": "number"},
                            "rx_bytes": {"type": "number"},
                            "tx_bytes": {"type": "number"},
                        },
                        "required": ["mac", "iface", "signal", "hostname",
                                     "rx_packets", "tx_packets", "rx_bytes", "tx_bytes"]
                }
            },
            "required": ["status","hostname","ips"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_get_notes(self):
        res = self.ws.get_notes()
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "notes": {"type": "string"},
            },
            "required": ["status","notes"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

    def test_set_notes(self):
        current_notes = self.ws.get_notes()["notes"]
        res = self.ws.set_notes(current_notes)
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "notes": {"type": "string"},
            },
            "required": ["status","notes"]
        }
        validate(res, schema)
        self.assertEqual(res["status"], "ok")

if __name__ == '__main__':
    unittest.main()
