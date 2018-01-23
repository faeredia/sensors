#to push code to esp, use:
#sudo ampy -p /dev/ttyUSB0 put main.py main.py

import urequests
import dht
import time
import machine
import network
import ubinascii

#how many times should we try to connect before giving up?
conn_tries = 2

#setup connection to the network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("badwolf", "17162968")
wlan.ifconfig()

#define the name of the board
sensID = "SENSOR" + str(int(ubinascii.hexlify(machine.unique_id()), 16))
#which pin is the dht attached to?
d = dht.DHT22(machine.Pin(2))

#setup the alarm so that we can deepsleep the device
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
# minutes (x) * seconds (60) * microseconds (1000)
rtc.alarm(rtc.ALARM0, 3*60*1000)

#generic method for uploading data
def uploadGenericSensorData(valType, val, unit):
    url = "http://faeredia.asuscomm.com/sensors/collectorGenericSensorData.php"
    url = url + "?sensorid=" + sensID
    url = url + "&valuetype=" + valType
    url = url + "&value=" + val
    url = url + "&units=" + unit

    try_num = 1
    #try a few times to connect to the server. if we fail, give up. 
    while(try_num <= conn_tries):
        print("Try", try_num, ":")
        print(url)
        try:
            urequests.get(url)
            break
        except:
            print("Failed")
        try_num += 1
    if(try_num > conn_tries):
        print("Giving up after", try_num -1, "tries.")

#main loop
while(True):
    print("starting..")
    #wait half a second to let the DHT sort itself out.
    time.sleep(0.5)
    try:
        print("measure")
        d.measure()
    except:
        #we threw an error trying to use the dht sensor.
        #let the server know, we may need maintenance
        #go to sleep, if it happens again, we may need to do something.
        print("measure error")
    
    
    print("upload")
    uploadGenericSensorData("TEMPERATURE", str(d.temperature()), "C")
    uploadGenericSensorData("HUMIDITY", str(d.humidity()), "%")
    #except:
        #we threw an error trying to tell the server something
        #try to tell the server what happened, then go to sleep, we can try again later
    #    print("upload error")
    #    pass

    print("giving one second for you to interupt")
    time.sleep(1)
    
    print("rest...")
    machine.deepsleep()
