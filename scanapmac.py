#!/usr/bin/python3

# Import modules
import wifi, colorama, argparse, time, csv, re
from wifi import Cell
from colorama import init, Fore, Style

init(autoreset=True)

# Parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interface', help='Wireless interface to use, ex. wlp3s0')
parser.add_argument('-q', '--query', help='Queries seperated by comma, ex. eduroam,2.4,11')
parser.add_argument('-o', '--output', help='Where to save the logfile, ex. /root/eduroam.csv')
args = parser.parse_args()

# Function for user input
def userInput(question):
  while True:
    userInput = input(question)
    if not userInput:
      print(Style.BRIGHT + Fore.YELLOW + 'WARNING: ' + Style.RESET_ALL + 'Please enter something more than NULL.')
    else:
      return userInput
      break

# User input
if args.interface:
  interface = args.interface
else:
  interface = userInput('Interface (wlp3s0): ')
if args.query:
  query = args.query.split(',')
else:
  query = input('Queries seperated by comma, press ENTER to skip (eduroam,2.4,11): ').split(',')
if args.output:
  csvName = args.output
else:
  csvName = userInput('Output (/root/eduroam.csv): ')

# Print info in start of script
print(Style.BRIGHT + Fore.GREEN + 'INFO: ' + Style.RESET_ALL + 'Logging AP info by filter ' + str(query) + ' to ' + csvName)

# Init .csv-file
fieldnames = ['SSID',
              'Signal',
              'Quality',
              'Frequency',
              'Bitrates',
              'Encrypted',
              'Encryption Type',
              'Channel',
              'MAC address',
              'Mode'
              ]
try:
  with open(csvName, 'x') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
except FileExistsError:
  pass

try:
  while True:
    try:
      # Scan WiFi
      apScan = Cell.all(interface)
    except wifi.exceptions.InterfaceError:
      pass
    # Go thorugh and filter info
    for ap in apScan:
      apMac = ap.address.lower()
      regex = re.search('(\d)\.',ap.frequency)
      if regex.group(1) == '2':
        apFreq = 2.4
      else:
        apFreq = 5
      # Compare query with info about AP
      apInfo = [ap.ssid,str(apFreq),str(ap.encrypted),str(ap.channel),apMac,ap.mode]
      if set(query).issubset(apInfo) or query == ['']:
        with open(csvName, 'r') as csvfile:
          csvRead =  csvfile.read()
          if not apMac in csvRead:
            # Write info to .csv-file
            with open(csvName, 'a') as csvfile:
              print(Style.BRIGHT + Fore.GREEN + 'INFO: ' + Style.RESET_ALL + apMac + ' added to ' + csvName)
              writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
              writer.writerow({'SSID' : ap.ssid,
                               'Signal' : ap.signal,
                               'Quality' : ap.quality,
                               'Frequency' : apFreq,
                               'Bitrates' : ap.bitrates,
                               'Encrypted' : ap.encrypted,
                               'Encryption Type' : ap.encryption_type,
                               'Channel' : ap.channel,
                               'MAC address' : apMac,
                               'Mode' : ap.mode
                               })
except KeyboardInterrupt:
  print('')
