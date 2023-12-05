# Using Hexiwear with Python
import pexpect
import time
import datetime

def writeFile(filename,msg,mode) :
    f = open(filename,mode)
    f.write(msg)
    f.close()

####  Change Param ####
DEVICE = "A5:C2:37:04:EB:FF" # Bluetooth Address
BMSNAME= "liion48-1"         # BMS Name

FILENAME= str("/mnt/data/%s.json" % BMSNAME)  # File Location
#####################3#

print("Hexiwear address:"),
print(DEVICE)

# Run gatttool interactively.
print("Run jbdbms-8-socket...")
child = pexpect.spawn("sudo /usr/bin/python3 /home/pi/jbdbms-8-socket-2temps.py -b %s -i 5 -m %s" % (DEVICE,BMSNAME))

# Connect to the device.
print("Connecting to {0}".format(DEVICE))
child.expect("connected", timeout=10)

oldsum = ""
while True:
  try:
    child.expect("meter,cell1",timeout=10)
    child.expect("\r\n", timeout=5)
    child.expect("\r\n", timeout=5)
    r1 = child.before.decode('unicode-escape')
    print('r1 : %s' % (r1))
  except pexpect.TIMEOUT:
    continue
 
  try:
    child.expect("meter,cellmin",timeout=5)
    child.expect("\r\n", timeout=5)
    child.expect("\r\n", timeout=5)
    r2 = child.before.decode('unicode-escape')
    print('r2 : %s' % (r2))
  except pexpect.TIMEOUT:
    continue
  try:
    child.expect("meter,volts",timeout=5)
    child.expect("\r\n", timeout=5)
    child.expect("\r\n", timeout=5)
    r3 = child.before.decode('unicode-escape')
    print('r3 : %s' % (r3))
  except pexpect.TIMEOUT:
    continue

  dt_now  = datetime.datetime.now()
  dt      = dt_now.strftime('%Y%m%d%H%M%S')
  r1t=False
  r2t=False
  r3t=False
  meter=""

  if len(r1) > 0 :
    r1array = r1.split(',')
    meter = r1array[0]
    c1 = int(r1array[1])/1000
    c2 = int(r1array[2])/1000
    c3 = int(r1array[3])/1000
    c4 = int(r1array[4])/1000
    c5 = int(r1array[5])/1000
    c6 = int(r1array[6])/1000
    c7 = int(r1array[7])/1000
    c8 = int(r1array[8])/1000
    r1t=True
  if len(r2) > 0 :
    r2array = r2.split(',')
    meter = r2array[0]
    cmin = int(r2array[1])/1000
    cmax = int(r2array[2])/1000
    delta = int(r2array[3])
    r2t=True
  if len(r3) > 0 :
    r3array = r3.split(',')
    meter = r3array[0]
    volts = float(r3array[1])
    amps  = float(r3array[2])
    watts = float(r3array[3])
    remain= int(r3array[4])
    capa  = int(r3array[5])
    cycles= int(r3array[6])
    r3t=True

  if r1t and r2t and r3t :
    msgstr = str(r'{"device": "%s","voltage": %.2f,"amp": %.2f,"watt": %.2f,"remain": %d,"capacity": %.2f,"cycles": %d,"cellmin": %.3f,"cellmax": %.3f,"delta": %d,"cell1": %.3f,"cell2": %.3f,"cell3": %.3f,"cell4": %.3f,"cell5": %.3f,"cell6": %.3f,"cell7": %.3f,"cell8": %.3f,"datetime": "%s"}' % (meter,volts,amps,watts,remain,capa,cycles,cmin,cmax,delta,c1,c2,c3,c4,c5,c6,c7,c8,dt))

  if r1t and r2t and r3t == False :
    msgstr = str(r'{"device": "%s","cellmin": %.3f,"cellmax": %.3f,"delta": %d,"cell1": %.3f,"cell2": %.3f,"cell3": %.3f,"cell4": %.3f,"cell5": %.3f,"cell6": %.3f,"cell7": %.3f,"cell8": %.3f,"datetime": "%s"}' % (meter,cmin,cmax,delta,c1,c2,c3,c4,c5,c6,c7,c8,dt))

  if r1t==False and r2t and r3t :
    msgstr = str(r'{"device": "%s","voltage": %.2f,"amp": %.2f,"watt": %.2f,"remain": %d,"capacity": %.2f,"cycles": %d,"cellmin": %.3f,"cellmax": %.3f,"delta": %d,"datetime": "%s"}' % (meter,volts,amps,watts,remain,capa,cycles,cmin,cmax,delta,dt))

  writeFile(FILENAME,msgstr,'w')
