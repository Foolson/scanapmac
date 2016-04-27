#!/usr/bin/python3

import wifi, colorama
from wifi import Cell
from colorama import init, Fore, Back, Style

interface = 'wlp3s0'
ssidFilter = 'eduroam'
logName = ssidFilter + '-mac.log'

init(autoreset=True)

try:
  f = open(logName, 'x')
  f.write('# MAC log for ' + ssidFilter + "\n")
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
            print(Style.BRIGHT + Fore.GREEN + 'INFO: ' + ap.address + ' added to ' + logName)
            f.write(ap.address+"\n")
except KeyboardInterrupt:
  print('')
