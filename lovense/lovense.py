import http.client
import ssl
import json
import time
import command 

class lovense:
    def __init__(self, address, port, timeout = 10):
        self.address = address
        self.port    = port
        self.timeout = timeout
        self.headers = {'Content-type': 'application/json'}

    def connect(self):
        try:
            self.conn = http.client.HTTPSConnection(self.address, self.port, timeout = self.timeout, context = ssl._create_unverified_context())
            return True
        except:
            print("[lovense] Error: Cannot connect to the server")
            return False

    def execute(self, myrequest):
        self.conn.request('POST', '/command', myrequest, self.headers)
        
        json_res = self.conn.getresponse()
        res = json.load(json_res)
        code = res["code"]
        
        if(code == 200):
            return res
        elif(code == 500):
            print("[lovense] Error: HTTP server not started or disabled")
        elif(code == 400):
            print("[lovense] Error: Invalid command")
        elif(code == 401):
            print("[lovense] Error: Toy not found")
        elif(code == 402):
            print("[lovense] Error: Toy not connected")
        elif(code == 403):
            print("[lovense] Error: Toy doesn't support this command")
        elif(code == 404):
            print("[lovense] Error: Invalid parameter")
        elif(code == 506):
            print("[lovense] Error: Server error. Restart Lovense connect")

        return False


    def response(self):
        return self.conn.getresponse()

    def get_toys(self):
        cmd = command.GetToys()
        return self.execute(cmd.to_json())
    
    def get_toy_name(self):
        cmd = command.GetToyName()
        return self.execute(cmd.to_json())

    def start_vibration(self, strength):
        req = command.Vibrate(strength)
        self.execute(req.to_json())
    
    def stop(self):
        req = command.Stop() 
        self.execute(req.to_json())

#toy = lovense("192.168.1.7", 30010)   
#
#info = toy.get_toys()
#print("Toys info:")
#print(info)
#
#name = toy.get_toy_name()
#print("Toys name:")
#print(name)
#
#print("Start vibration")
#toy.start_vibration(10)
#
#time.sleep(3)
#
#print("Stop vibration")
#toy.stop()
#
#time.sleep(1)
