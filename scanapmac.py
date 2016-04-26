#!/usr/bin/python3

import wifi
from wifi import Cell, Scheme

logName = "mac.log"
interface = "wlp3s0"
ssidFilter = "eduroam"

try:
  f = open(logName, 'x')
  f.write("# mac log for "+ssidFilter+"\n")
  f.close()
except FileExistsError:
  pass
  
try:
  while True:
    apScan = Cell.where(interface, lambda c: c.ssid == ssidFilter)
    for ap in apScan:
      with open(logName, "r") as f:
        macLog =  f.read()
        if not ap.address in macLog:
          with open(logName, "a") as f:
            print(ap.address+" "+"added to "+logName)
            f.write(ap.address+"\n")
except KeyboardInterrupt:
  pass   
