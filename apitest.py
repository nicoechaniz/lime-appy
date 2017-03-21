from websocket import create_connection
import json
import hashlib

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

    def get_stations(self, iface):
        return self._send(method="call", params=[session_token,"/lime/api",
                                                 "get_stations", {"iface": iface}])
    def get_station_signal(self, iface, station_mac):
        return self._send(method="call", params=[session_token,"/lime/api", "get_station_signal",
                                                 {"iface": iface, "station_mac": station_mac}])
    def get_assoclist(self, iface):
        return self._send(method="call", params=[session_token,"/lime/api",
                                                 "get_assoclist", {"iface": iface}])
    def close(self):
        self.connection.close()

if __name__ == "__main__":
    user = r"admin"
    password = r"admin"

    ws = LiMeApi("ws://10.13.207.235/websocket/")

    ws.list_methods()
    challenge_res = ws.challenge()
    session_token = ws.login(challenge_res)

    ws.get_hostname()
    ws.get_location()
    ws.get_neighbors()
    ws.get_bmx6()
    ws.set_location(-31,-64)

    res = ws.get_interfaces()
    iface = json.loads(res)["result"]["interfaces"][0]
    ws.get_assoclist(iface)

    res = ws.get_stations(iface)
    station = json.loads(res)["result"].popitem()[0]
    res = ws.get_station_signal(iface, station)
 
    ws.close()

