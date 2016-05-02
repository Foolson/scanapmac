#!/usr/bin/python3

import csv,re

input='output.csv'
regex=re.search('(.+)\.csv',input)
output=regex.group(1)+'.txt'

with open(output,'w') as outFile:
  with open(input,'r') as inFile:
    csvRead = csv.DictReader(inFile)
    for row in csvRead:
      outFile.write(row['address']+'/')
