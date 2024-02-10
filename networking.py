import _thread
import network
import socket
import ure
import time
import machine
import ubinascii
import btree

# constants
BOARD_ID = str(ubinascii.hexlify(machine.unique_id()).decode("utf-8"))
AP_AUTHMODE = 3 #WPA2
#globals
client_ssid = ""
client_password = ""

wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)
server_socket = None

# using DB to store stuff
def initialize():
    try:
        f = open("mydb", "r+b")
        db = btree.open(f)
        client_ssid = db["cl_ssid"].decode("utf-8")
        client_password = db["cl_password"].decode("utf-8")
        f.close()
    except OSError:
        f = open("mydb", "w+b")
        db = btree.open(f)
        db["ap_ssid"] = "Object_"+BOARD_ID
        db["ap_hostname"] = "Object_"+BOARD_ID
        db["ap_password"] = "1234567890"
        db["cl_ssid"] = "VesnaR_3"
        db["cl_password"] = "25Bojana12"
        db.flush()
        f.close()
    return client_ssid, client_password

def send_header(client, status_code=200, content_length=None ):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
      client.sendall("Content-Length: {}\r\n".format(content_length))
    client.sendall("\r\n")

def send_response(client, payload, status_code=200):
    content_length = len(payload)
    send_header(client, status_code, content_length)
    if content_length > 0:
        client.sendall(payload)
    client.close()

def connect(ssid, password):
    connected = False
    print("client_ssid",client_ssid)
    if client_ssid != "":
        wlan_sta.active(True)
        wlan_sta.connect(client_ssid, client_password)
        for retry in range(50):
            connected = wlan_sta.isconnected()
            if connected:
                print('\nConnected. Network config: ', wlan_sta.ifconfig())
                break
            else:
                print('\nFailed. Not Connected to: ' + client_ssid)  
            time.sleep(1.0)
    else:
        print("Tu sam!")
        #tu treba da inicijalizujem web server i AP mod
        pass

client_ssid, client_password = initialize()
connect(client_ssid, client_password)







#_thread.start_new_thread(testThread, ())