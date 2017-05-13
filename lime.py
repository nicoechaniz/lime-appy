#!/usr/bin/python3

from websocket import create_connection
import json
import hashlib

class LiMeApi(object):
    def __init__(self, base_node="thisnode.info", user="admin", password="admin"):
        self.user = user
        self.password = password
        url = "ws://%s/websocket/" % base_node
        self.connection = create_connection(url)
        self.call_id = 0
        self.session_token = None
        self.verbosity = 0

    def _send(self, method, params):
        self.call_id += 1
        call = {"jsonrpc": "2.0", "id":self.call_id, "method": method, "params": params}
        if self.verbosity:
            print("\nSending", call)
        self.connection.send(json.dumps(call))
        if self.verbosity:
            print("Sent")
            print("Receiving...")
        result =  self.connection.recv()
        if self.verbosity:
            print("Received '%s'" % result)
        return result

    def _list_methods(self):
        return self._send(method="list", params=["","*"])

    def _challenge(self):
        return self._send(method="challenge", params=[])

    def _login(self, challenge_result):
        shapass = hashlib.new("sha1")
        shatok = hashlib.new("sha1")
        r = json.loads(challenge_result)
        token = r["result"]["token"]
        shapass.update(str.encode(self.password))
        shatok.update(str.encode(token))
        shatok.update(str.encode(shapass.hexdigest()))
        passtok = shatok.hexdigest()

        # login
        res = self._send(method="login", params=[self.user, passtok])
        json_res = json.loads(res)
        self.session_token = json_res["result"]["success"]
        return self.session_token

    def get_hostname(self):
        res = self._send(method="call",
                         params=[self.session_token, "/lime/api",
                                 "get_hostname",{}])
        return json.loads(res)["result"]

    def get_location(self):
        res = self._send(method="call", params=[self.session_token,"/lime/api",
                                                "get_location",{}])
        return json.loads(res)["result"]

    def get_cloud_nodes(self):
        res = self._send(method="call", params=[self.session_token,"/lime/api",
                                                "get_cloud_nodes",{}])
        return json.loads(res)["result"]

    def set_location(self, lat, lon):
        res = self._send(method="call",
                         params=[self.session_token,"/lime/api",
                                 "set_location", {"lat":lat,"lon":lon}])
        return json.loads(res)["result"]

    def get_interfaces(self):
        res = self._send(method="call", params=[self.session_token,"/lime/api",
                                                "get_interfaces",{}])
        return json.loads(res)["result"]

    def get_iface_stations(self, iface):
        res = self._send(method="call",
                         params=[self.session_token,"/lime/api",
                                 "get_iface_stations", {"iface": iface}])
        return json.loads(res)["result"]

    def get_stations(self):
        res = self._send(method="call", params=[self.session_token,"/lime/api",
                                                 "get_stations", {}])
        return json.loads(res)["result"]

    def get_station_signal(self, iface, station_mac):
        res = self._send(method="call",
                         params=[self.session_token,"/lime/api",
                                 "get_station_signal",
                                 {"iface": iface, "station_mac": station_mac}])
        return json.loads(res)["result"]

    def get_station_traffic(self, iface, station_mac):
        res = self._send(method="call",
                         params=[self.session_token,"/lime/api",
                                 "get_station_traffic",
                                 {"iface": iface, "station_mac": station_mac}])
        return json.loads(res)["result"]

    def get_assoclist(self, iface):
        res = self._send(method="call",
                         params=[self.session_token,"/lime/api",
                                 "get_assoclist", {"iface": iface}])
        return json.loads(res)["result"]

    def get_gateway(self):
        res = self._send(method="call",
                         params=[self.session_token,"/lime/api",
                                 "get_gateway", {}])
        return json.loads(res)["result"]

    def get_path(self, target):
        res = self._send(method="call",
                         params=[self.session_token,"/lime/api",
                                 "get_path", {"target":target}])

        return json.loads(res)["result"]

    def get_metrics(self, target):
        res = self._send(method="call",
                         params=[self.session_token,"/lime/api",
                                 "get_metrics", {"target":target}])
        return json.loads(res)["result"]

    def get_gateway_metrics(self):
        res = self._send(method="call", params=[self.session_token,"/lime/api",
                                                 "get_gateway_metrics", {}])
        return json.loads(res)["result"]

    def get_internet_path_metrics(self):
        res = self._send(method="call",
                         params=[self.session_token,"/lime/api",
                                 "get_internet_path_metrics", {}])
        return json.loads(res)["result"]

    def get_last_internet_path(self):
        res = self._send(method="call",
                         params=[self.session_token,"/lime/api",
                                 "get_last_internet_path", {}])
        return json.loads(res)["result"]

    def get_internet_status(self):
        res = self._send(method="call",
                         params=[self.session_token,"/lime/api",
                                 "get_internet_status", {}])
        return json.loads(res)["result"]

    def get_node_status(self):
        res = self._send(method="call",
                         params=[self.session_token,"/lime/api",
                                 "get_node_status", {}])
        return json.loads(res)["result"]

    def get_path_metrics(self, target):
        path = json.loads(self.get_path(target))
        res = path["result"]
        for i in range(1, len(res)+1):
            self.get_metrics(res[str(i)])

    def get_notes(self):
        res = self._send(method="call",
                         params=[self.session_token,"/lime/api",
                                 "get_notes", {}])
        return json.loads(res)["result"]

    def set_notes(self, text):
        res = self._send(method="call",
                         params=[self.session_token,"/lime/api",
                                 "set_notes", {"text":text}])
        return json.loads(res)["result"]

    def _close(self):
        self.connection.close()

if __name__ == "__main__":
    import inspect
    import argparse
    parser = argparse.ArgumentParser()
    method_choices = [method[0] for method in inspect.getmembers(LiMeApi, predicate=inspect.isfunction)
                      if method[0].startswith("get_") or method[0].startswith("set_")]
    parser.add_argument("-b", "--base_node", help="node hostname to use for your api call", default="thisnode.info")
    parser.add_argument("--user", help="orangerpc username to use", default="admin")
    parser.add_argument("--password", help="orangerpc password to use", default="admin")
    parser.add_argument("-v", "--verbosity", help="verbosity level of command output", default=0)
    parser.add_argument("method", help="api method to call", choices=method_choices)
    parser.add_argument("method_params", nargs="*", help="method parameters")
    args = parser.parse_args()

    ws = LiMeApi(base_node=args.base_node, user=args.user, password=args.password)
    ws.verbosity = args.verbosity
    ws._list_methods()
    challenge_res = ws._challenge()
    ws._login(challenge_res)

    if not args.method.startswith("_"):
        method = getattr(ws, args.method)
        res = method(*args.method_params)
        print(res)

    ws._close()
