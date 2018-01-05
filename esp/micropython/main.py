import urequests
import dht
import time
import machine
import network
import ubinascii

#setup connection to the network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("badwolf", "17162968")
wlan.ifconfig()

#define the name of the board
sensID = "SENSOR" + str(int(ubinascii.hexlify(machine.unique_id()), 16))
#which pin is the dht attached to?
d = dht.DHT11(machine.Pin(2))

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

    print(url)
    urequests.get(url)

#main loop
while(True):
    print("starting..")

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
