import argparse

import command
import lovense

parser = argparse.ArgumentParser(description='Send commands to lovense toy')
parser.add_argument('address', metavar='ADDRESS', nargs=1,
                    help='the IP address of the toy')
parser.add_argument('port', metavar='PORT', type=int, nargs=1,
                    help='the port of the toy', default=30010)

args = parser.parse_args()
address = args.address[0]
port = args.port[0]

toy = lovense.lovense(address, port)
print("[lovense] Connecting to the toy at {}:{} ... ".format(address, port), end='')
if( toy.connect() is True):
    print("connected.")
else:
    print("NOT connected")
    quit()

status = True

while status:
    print("[lovense] Start the vibration by typying 'start X', where X is the strength (between 0 and 20)")
    print("          You can stop the vibration by typing 'stop'")
    print("          Type 'q' or 'quit' to exit.")
    prompt = input(">> ")
    
    text = prompt.split(" ")
    
    if ( (len(text) == 1) and (text[0] == "stop") ):
        toy.stop()
    elif ( (len(text) == 2) and (text[0] == "start") ):
        toy.start_vibration(int(text[1]))
    elif ( (len(text) == 1) and ( (text[0] == "q") or (text[0] == "quit") ) ):
        status = False
    else:
        pass





