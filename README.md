# Active ATC

Gives a summary of ATC channels from a CSV rtl_power scan of the band.  Based on the flatten.py script from https://github.com/keenerd/rtl-sdr-misc

## Create CSV

Create the CSV with rtl_power: `rtl_power -f 118M:137M:8k -g 50 -i 10 -e 1h airband.csv`

## Generate summary

Generate the summary CSV: `./active-atc.py airband.csv`