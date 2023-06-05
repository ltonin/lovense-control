import json

class Command:
    def __init__(self, command, api):
        self.command = dict(command = command, apiVer = api)

    def set_command(self, command):
        self.command["command"] = command

    def set_toy(self, toy):
        self.command["toy"] = toy

    def set_api(self, api):
        self.command["apiVer"] = api

    def to_json(self):
        return json.dumps(self.command)

    def dump(self):
        print("Command object '", self.command["command"], "':", sep="")
        for x, y in self.command.items():
            print("   |- ", x, ": ", y, sep="")

class GetToys(Command):
    def __init__(self, api=1):
        super().__init__("GetToys", api)

class GetToyName(Command):
    def __init__(self, api=1):
        super().__init__("GetToyName", api)

class Vibrate(Command):
    def __init__(self, strength, api=1):
        strength = int(strength)
        super().__init__("Function", api)

        if(strength > 20):
            print("[warning] Maximum strength allowed is 20. Stength set to 20")
            strength = 20

        if(strength < 0):
            print("[warning] Minimum strength allowed is 0. Stength set to 0")
            strength = 0

        if(strength == 0):
            print("[warning] Strength is set to 0")

        self.command["action"] = "Vibrate:"+str(strength)
        self.command["timeSec"] = 0

    def set_loop(self, runtime, stoptime):
        self.command['loopRunningSec'] = int(runtime)
        self.command['loopPauseSec'] = int(stoptime)

    def unset_loop(self):
        self.commad.pop('loopRunningSec', None)
        self.commad.pop('loopPauseSec', None)

    def set_duration(self, duration):
        self.command["timeSec"] = duration

    def unset_duration(self):
        self.command["timeSec"] = 0

class Stop(Command):
    def __init__(self, api=1):
        super().__init__("Function", api)
        self.command["action"] = "Stop"
        self.command["timeSec"] = 0


#x = Vibrate("16")
#x.dump()
#
#y = x.to_json()
#print("\njson serialization:")
#print(y)
#
#x.set_toy("sss")
#x.dump()
#y = x.to_json()
#print("\njson serialization:")
#print(y)


