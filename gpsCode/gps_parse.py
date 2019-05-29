import serial
 
port = "/dev/ttyS0" #the rpisink uses ttyAMA0 AND serial0 for UART, it DOES NOT USE ttyS0
 
def parseGPS(data):
#    print "raw:", data #prints raw data

    try:
        data = data.decode().split(",")
        print(data)
        if data[0] == "$GPRMC":
            #sdata = data.split(",")
            if data[2] == 'V':
                print ("no satellite data available")
                return
        
            print ("---Parsing GPRMC---"),
        
            lat = decode(data[3]) #latitude
            dirLat = data[4]      #latitude direction N/S
            lon = decode(data[5]) #longitute
            dirLon = data[6]      #longitude direction E/W
            speed = data[7]       #Speed in knots
        
            print ("latitude : %s(%s), longitude : %s(%s), speed : %s," %  (lat,dirLat,lon,dirLon,speed))
    except UnicodeDecodeError:
        print("Exception")
    #print(type(data[0:6]))
 
def decode(coord):
    #Converts DDDMM.MMMMM > DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"
 
 
print ("Receiving GPS data")
ser = serial.Serial(port, baudrate = 57600, timeout = 0.5)
while True:
   data = ser.readline()
   #print(data)
   parseGPS(data)