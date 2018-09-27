#! /usr/bin/env python

import sys
from collections import defaultdict

def help():
    print("active-atc.py airband.csv")
    print("Gives usage summary for 25khz ATC channels from an rtl_power csv, run in the air band.\n - Example: rtl_power -f 118M:137M:8k -g 50 -i 10 -e 1h airband.csv")
    sys.exit()

if len(sys.argv) <= 1:
    help()

if len(sys.argv) > 2:
    help()

path = sys.argv[1]

sums = defaultdict(float)
counts = defaultdict(int)
maxdb = defaultdict(lambda: float("-120.0"))

def frange(start, stop, step):
    i = 0
    f = start
    while f <= stop:
        f = start + step*i
        yield f
        i += 1

def atcround(freq):
    # Chop off significant digits to get our frequency
    freq = float(str(freq)[:6])

    # Clamp to 25khz baseband frequency band is closest to
    if (freq % 25) > 12.5:
        freq = freq + (25 - (freq % 25))
    else:
        freq = freq - (freq % 25)
    freq_decimal = str(freq)[0:3] + "." + str(freq)[3:6]
    return(freq_decimal)

for line in open(path):
    line = line.strip().split(', ')
    low = int(line[2])
    high = int(line[3])
    step = float(line[4])
    weight = int(line[5])
    dbm = [float(d) for d in line[6:]]
    for f,d in zip(frange(low, high, step), dbm):
        freq = atcround(f)
        sums[freq] += d*weight
        counts[freq] += weight
        if float(d) > maxdb[freq]:
            maxdb[freq] = d

ave = defaultdict(float)
for f in sums:
    ave[f] = sums[f] / counts[f]

print("Freqency,MaxDB,AvgDB,DiffDB")
for f in sorted(maxdb):
    print(','.join([str(f), str(maxdb[f]), str(ave[f]), str(maxdb[f] - ave[f])]))   

