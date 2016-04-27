#!/usr/bin/python3

import wifi, colorama, argparse, time
from wifi import Cell
from colorama import init, Fore, Style

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interface', help='Wireless interface to use, ex. wlp3s0')
parser.add_argument('-s', '--ssid', help='SSID to filter out, ex. eduroam')
parser.add_argument('-o', '--output', help='Where to save the logfile, ex. /root/eduroam.log')
args = parser.parse_args() 

if args.interface:
  interface = args.interface
else:
  interface = input('Interface (Wireless interface to use, ex. wlp3s0): ')
if args.ssid:
  ssidFilter = args.ssid
else:
  ssidFilter = input('SSID (SSID to filter out, ex. eduroam): ')
if args.output:
  logName = args.output
else:
  logName = input('Output (Where to save the logfile, ex. /root/eduroam.log): ')

init(autoreset=True)

print(Style.BRIGHT + Fore.GREEN + 'INFO: ' + Style.RESET_ALL + 'Logging MAC from ' + ssidFilter + ' to ' + logName)

try:
  f = open(logName, 'x')
  f.close()
except FileExistsError:
  pass
  
try:
  while True:
    try:
      apScan = Cell.all(interface)
    except wifi.exceptions.InterfaceError:
      print(Style.BRIGHT + Fore.YELLOW + 'WARNING: ' + Style.RESET_ALL + 'Wierd error, probably safe to continue, I guess...')
    for ap in apScan:
      apMac = ap.address.lower()
      if ap.ssid == ssidFilter:
        with open(logName, 'r') as f:
          macLog =  f.read()
          if not apMac in macLog:
            with open(logName, 'a') as f:
              print(Style.BRIGHT + Fore.GREEN + 'INFO: ' + Style.RESET_ALL + apMac + ' added to ' + logName)
              f.write(apMac + "/")
    time.sleep(2)
except KeyboardInterrupt:
  print('')
