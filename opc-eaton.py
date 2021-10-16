import OpenOPC
import time
import datetime
import json
import csv
import  redis
import struct

#*******************************************************************
num_machine = 2
tags_WasherState = []
tags_PcState = []
tags_aBLB = []
OPC_name = 'CoDeSys.OPC.DA'
OPC_list = 'DF02_CL01'
OPC_Connection_status = False;

lst = []
data = []

opc = OpenOPC.client()

#*******************************************************************

def give_me_tags():
    for n in range(num_machine):
        WasherState = OPC_list+".."+"adwWasherState["+str(n+1)+"]"
        tags_WasherState.append(WasherState)
        PcState = OPC_list+".."+"adwPCState["+str(n+1)+"]"
        tags_PcState.append(PcState)
        PcState = OPC_list + ".." + "aBLBatchData[" + str(n + 1) + "]"
        tags_PcState.append(PcState)


def OPC_connection():
    opc.close()
    try:
        opc.connect(OPC_name)
    except:
        print("fail to connect")
        return 1
    try:
        None
        #global lst
        #lst = opc.list(OPC_list)
    except:
        print("list not accesible")
        return 2
    print("successfully connected")
    return 0

def OPC_read_data():
    try:
        global data

        data = opc.read(lst, group=data)
    except:
        print("timeout waiting for data")
        return 1
    return 0

def redis_connenction():
    try:
        r_pump = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)
        print (r_pump)

        r_pump.ping()
        print('Connected!')
        return r_pump
    except Exception as ex:
        print
        'Error:', ex
        exit('Failed to connect, terminating.')

def store_to_redis(data):
    r_pump = redis_connenction()
    r_pump.set(str(datetime.datetime.now()), json.dumps(data))

#*******************************************************************

#*************TAGY
give_me_tags()

while(1):

    while(OPC_Connection_status != True):
        if OPC_connection() == 0:
            OPC_Connection_status = True
        else:
            OPC_Connection_status = False
            print("next try after 3s")
            time.sleep(3)

    #try:
    #    status = opc.info()
    #except:
    #    print("server not accesible")
    #    OPC_Connection_status = False


    # ### redis prepare
    # data_json = []
    # if not data:
    #     print("empty data")
    # else:
    #     for item in data:
    #         data_json.append(item)
    #
    #
    # store_to_redis(data_json)
    #test = opcA.properties("DF01_WE01..aBLBatchData[10]",id=2)
    datas_to_redis = []
    for tag in tags_PcState:
        # test = opc.properties("DF01_WE01..adwWasherState[1]", id=2)
        print(tag)
        test = opc.properties(str(tag), id=2)
        whod_is = type(test)
        if whod_is == memoryview:
                    print(list(bytes(test)))
        else:
            by = bytearray(struct.pack("f",test))
            b = ((bin(int.from_bytes(by,byteorder="little"))).strip("0b"))
            x = 32 - len(b)
            b = x*"0"+str(b)
            print(str(tag), b, test)

    #     datas_to_redis.append([tag,b,test])
    #
    # store_to_redis(datas_to_redis)
    time.sleep(50)



    for item in lst:
        #print(str(item))
        fail = False
        try:
            test = opc.properties(OPC_list+"."+item, id=2)
        except:
            # print("posral jsem to ***"+ item + "***jo tohle ")
            fail = True

        #if not fail:
            #print(item)
            #print((bytes(test)))
            #print(list(bytes(test)))

        fail = False

    # data co jsou v memoryview mužeme převest na pole BYTU pomoci BYTES, pokud chceme hodnoty co vrací codesis je potřeba ještě zlistovat pomoci LIST

    # data_json =json.dumps(data_json)

    # print(data_json)


#*******************************************************************

# writing to csv file
    #filename = 'data_list.csv'
    #with open(filename, 'w') as csvfile:
    #    writer = csv.writer(csvfile)
    #    for item in data:
    #        writer.writerow(item)

#*******************************************************************