#!/usr/bin/python3

import wifi, colorama, argparse, time
from wifi import Cell
from colorama import init, Fore, Style

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interface', help='Wireless interface to use, ex. wlp3s0')
parser.add_argument('-s', '--ssid', help='SSID to filter out, ex. eduroam')
parser.add_argument('-o', '--output', help='Where to save the logfile, ex. /root/eduroam.log')
args = parser.parse_args()

def userInput():
  while True:
    interface = input('Interface (wlp3s0): ')
    if not interface:
      print(Style.BRIGHT + Fore.YELLOW + 'WARNING: ' + Style.RESET_ALL + 'Please enter something more than NULL.')
    else:
      break

if args.interface:
  interface = args.interface
else:
  while True:
    interface = input('Interface (wlp3s0): ')
    if not interface:
      print(Style.BRIGHT + Fore.YELLOW + 'WARNING: ' + Style.RESET_ALL + 'Please enter something more than NULL.')
    else:
      break
if args.ssid:
  ssidFilter = args.ssid
else:
  while True:
    ssidFilter = input('SSID (eduroam): ')
    if not ssidFilter:
      print(Style.BRIGHT + Fore.YELLOW + 'WARNING: ' + Style.RESET_ALL + 'Please enter something more than NULL.')
    else:
      break
if args.output:
  logName = args.output
else:
  while True:
    logName = input('Output (/root/eduroam.log): ')
    if not logName:
      print(Style.BRIGHT + Fore.YELLOW + 'WARNING: ' + Style.RESET_ALL + 'Please enter something more than NULL.')
    else:
      break

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
      print(Style.BRIGHT + Fore.RED + 'ERROR: ' + Style.RESET_ALL + 'Wierd stuff is going on, probably safe to continue, I guess...')
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
