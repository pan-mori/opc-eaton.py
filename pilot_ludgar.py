import OpenOPC
import time
import datetime
import json
import csv
import redis
import struct

#*******************************************************************
num_machine = 2
num_dosing_point = 20
tags_WasherState = []
tags_PcState = []
tags_aBLB = []
OPC_name = 'CoDeSys.OPC.DA'
OPC_list = 'DF01_WE01'
OPC_list = 'DF02_CL01'
OPC_Connection_status = False;

BOOL = True

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

        for m in range(num_dosing_point):
            PcState = OPC_list + ".." + "aBLCfgWasher[" + str(n + 1) + "].aDosingPoint["+str(m+1)+"]"
            tags_PcState.append(PcState)
        PcState = OPC_list + ".." + "aBLBatchData[" + str(n + 1) + "]"
        tags_PcState.append(PcState)

    for m in range(1,3):
        for x in range(1,21):
            PcState = OPC_list + ".." + "aBLDosageData["+str(m)+","+str(x)+"]"
            tags_PcState.append(PcState)

def ieee_754_conversion(n, sgn_len=1, exp_len=8, mant_len=23):
    """
    Converts an arbitrary precision Floating Point number.
    Note: Since the calculations made by python inherently use floats, the accuracy is poor at high precision.
    :param n: An unsigned integer of length `sgn_len` + `exp_len` + `mant_len` to be decoded as a float
    :param sgn_len: number of sign bits
    :param exp_len: number of exponent bits
    :param mant_len: number of mantissa bits
    :return: IEEE 754 Floating Point representation of the number `n`
    """
    if n >= 2 ** (sgn_len + exp_len + mant_len):
        raise ValueError("Number n is longer than prescribed parameters allows")

    sign = (n & (2 ** sgn_len - 1) * (2 ** (exp_len + mant_len))) >> (exp_len + mant_len)
    exponent_raw = (n & ((2 ** exp_len - 1) * (2 ** mant_len))) >> mant_len
    mantissa = n & (2 ** mant_len - 1)

    sign_mult = 1
    if sign == 1:
        sign_mult = -1

    if exponent_raw == 2 ** exp_len - 1:  # Could be Inf or NaN
        if mantissa == 2 ** mant_len - 1:
            return float('nan')  # NaN

        return sign_mult * float('inf')  # Inf

    exponent = exponent_raw - (2 ** (exp_len - 1) - 1)

    if exponent_raw == 0:
        mant_mult = 0  # Gradual Underflow
    else:
        mant_mult = 1

    for b in range(mant_len - 1, -1, -1):
        if mantissa & (2 ** b):
            mant_mult += 1 / (2 ** (mant_len - b))

    return sign_mult * (2 ** exponent) * mant_mult


def OPC_connection():
    opc.close()
    try:
        opc.connect(OPC_name)
    except:
        print("fail to connect")
        return 1
    try:
        None
        global lst
        lst = opc.list(OPC_list)
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

def merge_byte(byteA):

    lengt = len(byteA)
    total = 0
    for e, byte in enumerate(byteA):
        if lengt == e + 1:
            total = total + byte
        else:
            total = total + byte * 256 ** (lengt - e - 1)
    return (total)

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

    for tag in tags_PcState:
        print("tag: ",tag)
        da_promena = opc.properties(str(tag), id=2)

        whod_is = type(da_promena)
        if whod_is == memoryview:
                    # print((bytearray(da_promena)))
                    # print((bytes(da_promena)))
                    # print(list(bytes(da_promena)))
                    list_tag = list(bytes(da_promena))
                    # print("xXOOOOOOOOOOOOOOOOOX memori view")

                    print("krátky tag: ",tag[0:23])

                    if tag[0:23] == "DF02_CL01..aBLBatchData":
                        print("done")
                        # byProgBYTE = list(bytes(da_promena))[0]
                        # print(byProgBYTE)
                        #
                        # byStepBYTE = list(bytes(da_promena))[1]
                        # print(byStepBYTE)
                        #
                        # dwCustomerDWORD = list(bytes(da_promena))[4:8]
                        # print(merge_byte(dwCustomerDWORD))
                        #
                        # wBatchSizeWORD= list(bytes(da_promena))[8:10]
                        # print(merge_byte(wBatchSizeWORD))

                    if tag[0:23] == "DF02_CL01..aBLCfgWasher":
                        print("done")
                        # aBLCfgWasheraDosingPointbyLowLevelAlarmBYTE = list_tag[0]
                        # aBLCfgWasheraDosingPointbyTargetBYTE = list_tag[1]
                        # aBLCfgWasheraDosingPointxEnabledBOOL = list_tag[2]


                    if tag[0:24] == "DF02_CL01..aBLDosageData":
                        print("done")
                        # aBLDosageDatarSetPoint= list_tag[0:4]
                        # print("merge_byte",( merge_byte(aBLDosageDatarSetPoint)))
                        # xx = merge_byte(aBLDosageDatarSetPoint)
                        #
                        # f = int(str(xx), 10)
                        # print(struct.unpack('f', struct.pack('I', f))[0])
                        #
                        # aBLDosageDatarActualValue= list_tag[4:8]
                        # print(merge_byte(aBLDosageDatarActualValue))
                        #
                        # aBLDosageDatadtTimeStamp= list_tag[8:12]
                        # print(merge_byte(aBLDosageDatadtTimeStamp))
                        #
                        # aBLDosageDatabyErrorState= list_tag[12]
                        # print((aBLDosageDatabyErrorState))
                        #
                        # aBLDosageDatabyVisuState = list_tag[14:16]
                        # print(merge_byte(aBLDosageDatabyVisuState))

        ###todo automaticé obnovování když to spadne
        #muže othle vubec nasatat
        else:
            pass
            # nevím k čemu tohle je


            # # print("da_promena: ",da_promena)
            # # print(str(tag), da_promena)
            # x = (da_promena)
            # # print("data type ",type(da_promena))
            # by = bytearray(struct.pack("f", da_promena))
            # b = ((bin(int.from_bytes(by, byteorder="little"))).strip("0b"))
            # x = 32 - len(b)
            # b = x * "0" + str(b)
            # watch_dog = b[-2]
            # # print(b)
            # # print("watch dog  : ",watch_dog)
            # if watch_dog == 1:
            #     test = opc.properties(str(tag), id=2)



        # print(list(bytes(da_promena)))

        # a = memoryview(da_promena)
        # print(((a)))

        # by = bytearray(struct.pack("f", da_promena))
        # b = ((bin(int.from_bytes(by, byteorder="little"))).strip("0b"))
        # x = 32 - len(b)
        # b = x * "0" + str(b)
        # print(str(tag), b, da_promena)
        # watch_dog = b[-2]
        # if watch_dog == 1:
        #     test = opc.properties(str(tag), id=2)

    # print("XOXOXOXOXOXOXOXO")

    BOOL = not BOOL

    # if BOOL:
    #     print(opc.read("DF02_CL01..byPCHeartbeat"))
    #     opc.write(("DF02_CL01..byPCHeartbeat", 1))
    # else:
    #     print(opc.read("DF02_CL01..byPCHeartbeat"))
    #     opc.write(("DF02_CL01..byPCHeartbeat", 0))
    quit()
    time.sleep(1)
