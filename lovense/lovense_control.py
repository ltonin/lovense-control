#!/usr/bin/python

import os
import sys
import time
import argparse
import yaml
from pylsl import StreamInfo, StreamOutlet
import command
import lovense

def main():
    parser = argparse.ArgumentParser(description='Remote protocol control for lovense')
    parser.add_argument('config', metavar='CONFIG', nargs=1,
                        help='the YAML configuration file')
    
    args = parser.parse_args()
    configfile = args.config[0]
    
    # Importing YAML configuration
    try:
        with open(configfile, 'r') as f:
            contents = f.read()
    except IOError:
        print("[lovense] - Error: could not open the file " + configfile)
    cfg = yaml.safe_load(contents)
   
    print(cfg)

    # Initialize parameters
    global lsl_events
    toy_ip        = cfg['lovense']['toy']['address']
    toy_port      = cfg['lovense']['toy']['port']
    toy_strength  = cfg['lovense']['toy']['strength']
    lsl_streamid  = cfg['lsl']['streamid']
    lsl_events    = cfg['lsl']['events']
    timings_begin = cfg['protocol']['timings']['begin']
    timings_end   = cfg['protocol']['timings']['end']
    blocks        = cfg['protocol']['blocks']
    
    # Connection to the toy
    global toy
    toy = lovense.lovense(toy_ip, toy_port)
    print("[lovense] Connecting to the toy at {}:{} ... ".format(toy_ip, toy_port), end='')
    if( toy.connect() is True):
        print("connected.")
    else:
        print("NOT connected")
        quit()
    
    # Connection to LSL stream
    global outlet
    info   = StreamInfo('lovenseMarker', 'Markers', 1, 0, 'int32', lsl_streamid)
    outlet = StreamOutlet(info)
    
    # Main loop
    print("[lovense] + Protocol starts (event:{})".format(lsl_events['begin']))
    outlet.push_sample([lsl_events['begin']])
    time.sleep(timings_begin)
    blkId = 1
    
    for iblk in blocks:
        print("[lovense] + Block number {} (event:{}):".format(blkId, lsl_events['trialstart']))
        outlet.push_sample([lsl_events['trialstart']])
        runtime   = iblk['block']['run']
        pausetime = iblk['block']['pause']
        print("          |- Running for {} seconds (events:{}-{})".format(runtime, lsl_events['runstart'], lsl_events['runstop']))
        outlet.push_sample([lsl_events['runstart']])
        toy.start_vibration(toy_strength)
        time.sleep(runtime)
        outlet.push_sample([lsl_events['runstop']])
        print("          |- Pausing for {} seconds (events:{}-{})".format(pausetime, lsl_events['pausestart'], lsl_events['pausestop']))
        outlet.push_sample([lsl_events['pausestart']])
        toy.stop()
        time.sleep(pausetime)
        outlet.push_sample([lsl_events['runstop']])
        blkId = blkId + 1
        outlet.push_sample([lsl_events['trialstop']])
        print("          |- Block ends (event:{})".format(lsl_events['trialstop']))
    
    time.sleep(timings_end)
    outlet.push_sample([lsl_events['end']])
    print("[lovense] + Protocol ends (event:{})".format(lsl_events['end']))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("[lovense] - Operator asked to quit (event:{})".format(lsl_events['interrupt']))
        outlet.push_sample([lsl_events['interrupt']])
        toy.stop()
        sys.exit(130)



