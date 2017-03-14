from websocket import create_connection
import json
import hashlib

USER = r"admin"
PASSWORD = r"admin"

def ws_send(call):
    print("Sending", call)

    ws.send(call)
    print("Sent")
    print("Receiving...")
    result =  ws.recv()
    return result

if __name__ == "__main__":
    shapass = hashlib.new("sha1")
    shatok = hashlib.new("sha1")

    ws = create_connection("ws://10.5.1.200/websocket/")

    # list
    call = '{"jsonrpc":"2.0","id":1,"method":"list","params":["","*"]}'
    res = ws_send(call)

    # challenge
    call = '{"jsonrpc":"2.0","id":2,"method":"challenge","params":[]}'
    res = ws_send(call)
    r = json.loads(res)
    token = r["result"]["token"]
    shapass.update(str.encode(PASSWORD))
    shatok.update(str.encode(token))
    shatok.update(str.encode(shapass.hexdigest()))

    passtok = shatok.hexdigest()

    # login
    call = '{"jsonrpc":"2.0","id":3,"method":"login","params":["%s","%s"]}' % (USER, passtok)
    res = ws_send(call)
    r = json.loads(res)
    success = r["result"]["success"]

    # hostname
    call = '{"jsonrpc":"2.0","id":5,"method":"call",'\
           '"params":["%s","/lime/api", "get_hostname",{}]}' % success

    res = ws_send(call)
    print("Received '%s'" % res)
    ws.close()
