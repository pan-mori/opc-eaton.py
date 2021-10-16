import snap7.client as c
from snap7.util import *
from snap7.snap7types import *
import snap7
import time
import struct
from random import randint
import redis
import json
import datetime


class DBObject(object):
    pass

def daTObyteArray(data,size=2):
       return (data).to_bytes(size, byteorder="big")

def binaryarraytodec(arr):
    arr = "".join(map(str,arr))
    arr = int(arr,4)
    return arr

def bytetobin(bytes):
    return ''.join(format(byte, '08b') for byte in bytes)

def plcdatotobinarr(dato):

    dato = (int.from_bytes(dato, "little"))
    dato = daTObyteArray(dato, 4)
    return list(map(int, bytetobin(dato)))




def store_to_redis(data):

    r.set(str(datetime.datetime.now()), json.dumps(data))

if __name__=="__main__":
    plc = snap7.client.Client()
        
    data_key = ["Füllstand_Vorlage",
                        "pH_Wert_Vorlage",
                        "Temperatur_Vorlage",
                        "Füllstand_Arbeitsbehälter",
                        "pH_Wert_Arbeitsbehälter",
                        "Temperatur_Arbeitsbehälter",
                        "Durchfluss_Arbeitsbehälter",
                        "Füllstand_UF_Vorlage",
                        "Druck_Zulauf_UF",
                        "Temperatur_UF_Loop",
                        "Druck_UF_Loop_1",
                        "Druck_UF_Loop_2",
                        "Durchfluss_UF_Loop",
                        "Durchfluss_UF_Ablauf",
                        "Füllstand_Spülbehälter",
                        "Temperatur_Spülbehälter",
                        "Durchfluss_Permeat",
                        "pH_Wert_Permeat",
                        "Temperatur_Permeat",
                        "Füllstand",]
    data= {}

    r = redis.StrictRedis(host='192.168.123.65', port=6379, db=0)

    for y in range(2000):
        try:
            if not(plc.get_connected()):
                plc.connect('192.168.123.40', 0, 2)
            print("coccenction: ",plc.get_connected())                     #connect to plc
            for x in range(0,20):
                databerait = plc.db_read(100,10+(x*4) , 4)
                arr = struct.unpack('>f', databerait)
                arr = float(arr[0])
                data[data_key[x]]=arr

            print("range: "+str(y))

            store_to_redis(data)
            time.sleep(1)
        except :
            time.sleep(3)
            try:
                plc.disconnect()
                plc.connect('192.168.123.40', 0, 2)
            except:
                print("reset conenct fail")
            print("error :",y)
            time.sleep(1)

    plc.disconnect()


