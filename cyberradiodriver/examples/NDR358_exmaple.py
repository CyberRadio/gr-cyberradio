import CyberRadioDriver as crd
import sys


radio = crd.getRadioObject("ndr358", host=sys.argv[1] ,verbose=False)

cfgDict = radio.getConfiguration()

# setup a tuner:
cfgDict['tunerConfiguration'][0]['frequency'] = 3000e6
print cfgDict['tunerConfiguration'][0]

# inspect tuners
for tuner in radio.getTunerIndexRange():
    print cfgDict['tunerConfiguration'][tuner]

# IP configuration information
for link in radio.getGigEIndexRange():
    cfgDict['ipConfiguration'][link]['sourceIP']['sourcePort'] = 4991
    cfgDict['ipConfiguration'][link]['sourceIP']['ipAddr'] = "192.168.%d.10" % (int(link)+10)
    print cfgDict['ipConfiguration'][link]['sourceIP']

radio.setConfiguration(cfgDict)

for link in radio.getGigEIndexRange():
    # setup a destination
    for dest in  radio.getGigEDipEntryIndexRange():
        cfgDict['ipConfiguration'][link]['destIP'][dest]['arp'] = True
        cfgDict['ipConfiguration'][link]['destIP'][dest]['destPort'] = (10000 + (link*1000)) + dest

radio.setConfiguration(cfgDict)
print radio.getTunerIndexRange()
print radio.getWbddcIndexRange()
print radio.getNbddcIndexRange()

#help(radio) for more information

#print cfgDict
