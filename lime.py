from websocket import create_connection
import json
import hashlib
import sys

class LiMeApi(object):
    def __init__(self, url):
        self.connection = create_connection(url)
        self.call_id = 0

    def _send(self, method, params):
        self.call_id += 1
        call = {"jsonrpc": "2.0", "id":self.call_id, "method": method, "params": params}
        print("\nSending", call)
        self.connection.send(json.dumps(call))
        print("Sent")
        print("Receiving...")
        result =  self.connection.recv()
        print("Received '%s'" % result)
        return result

    def list_methods(self):
        return self._send(method="list", params=["","*"])

    def challenge(self):
        return self._send(method="challenge", params=[])

    def login(self, challenge_result):
        shapass = hashlib.new("sha1")
        shatok = hashlib.new("sha1")
        r = json.loads(challenge_result)
        token = r["result"]["token"]
        shapass.update(str.encode(password))
        shatok.update(str.encode(token))
        shatok.update(str.encode(shapass.hexdigest()))
        passtok = shatok.hexdigest()

        # login
        res = self._send(method="login", params=[user, passtok])
        r = json.loads(res)
        success = r["result"]["success"]
        return success

    def get_hostname(self):
        return self._send(method="call", params=[session_token,"/lime/api", "get_hostname",{}])

    def get_location(self):
        return self._send(method="call", params=[session_token,"/lime/api", "get_location",{}])

    def get_neighbors(self):
        return self._send(method="call", params=[session_token,"/lime/api", "get_neighbors",{}])

    def get_bmx6(self):
        return self._send(method="call", params=[session_token,"/lime/api", "get_bmx6",{}])

    def set_location(self, lat, lon):
        return self._send(method="call", params=[session_token,"/lime/api",
                                                 "set_location", {"lat":lat,"lon":lon}])
    def get_interfaces(self):
        return self._send(method="call", params=[session_token,"/lime/api", "get_interfaces",{}])
    def get_iface_stations(self, iface):
        return self._send(method="call", params=[session_token,"/lime/api",
                                                 "get_iface_stations", {"iface": iface}])
    def get_stations(self):
        return self._send(method="call", params=[session_token,"/lime/api",
                                                 "get_stations", {}])
    def get_station_signal(self, iface, station_mac):
        return self._send(method="call", params=[session_token,"/lime/api", "get_station_signal",
                                                 {"iface": iface, "station_mac": station_mac}])
    def get_assoclist(self, iface):
        return self._send(method="call", params=[session_token,"/lime/api",
                                                 "get_assoclist", {"iface": iface}])
    def get_gateway(self):
        return self._send(method="call", params=[session_token,"/lime/api",
                                                 "get_gateway", {}])
    def get_path(self, target):
        return self._send(method="call", params=[session_token,"/lime/api",
                                                 "get_path", {"target":target}])
    def get_metrics(self, target):
        return self._send(method="call", params=[session_token,"/lime/api",
                                                 "get_metrics", {"target":target}])
    def get_gateway_metrics(self):
        return self._send(method="call", params=[session_token,"/lime/api",
                                                 "get_gateway_metrics", {}])
    def get_internet_path_metrics(self):
        return self._send(method="call", params=[session_token,"/lime/api",
                                                 "get_internet_path_metrics", {}])
    def close(self):
        self.connection.close()

def run_tests(ws):
    ws.get_hostname()
    ws.get_location()
    ws.get_neighbors()
    ws.get_bmx6()
#    ws.set_location(-31,-64)
    
    res = ws.get_interfaces()
    iface = json.loads(res)["result"]["interfaces"][0]
    ws.get_assoclist(iface)
    
    res = ws.get_iface_stations(iface)
    station = json.loads(res)["result"].popitem()[1]["mac"]
    res = ws.get_station_signal(iface, station)
    
    res = ws.get_stations()
    
    res = ws.get_gateway()
    gateway = json.loads(res)["result"]["gateway"]
    path = json.loads(ws.get_path(gateway))
    res = path["result"]
    for i in range(1, len(res)+1):
        ws.get_metrics(res[str(i)])

    ws.get_internet_path_metrics()
    
if __name__ == "__main__":
    user = r"admin"
    password = r"admin"
    ws = LiMeApi("ws://thisnode.info/websocket/")
    ws.list_methods()
    challenge_res = ws.challenge()
    session_token = ws.login(challenge_res)
    args_count = len(sys.argv)
    if args_count==1:
        run_tests(ws)
    else:
        method_name = sys.argv[1]
        method = getattr(ws, method_name)
        params=[]
        if args_count>2:
            for arg in sys.argv[2:]:
                params.append(arg)
        method(*params)

    ws.close()
