
#!/usr/bin/env python
import argparse
import redis
import datetime
import json
import time
def redis_connenction(host,port,db):
    try:
        r_pump = redis.StrictRedis(host=host, port=port, db=db)
        # print (r_pump)

        r_pump.ping()
        # print('Connected!')
        return r_pump
    except Exception as ex:
        print
        'Error:', ex
        exit('Failed to connect, terminating.')

def store_to_redis(data):
    r_pump = redis_connenction()
    r_pump.set(str(datetime.datetime.now()), json.dumps(data))

if __name__ == '__main__':
    while 1:
        try:
            redis_local = redis_connenction("127.0.0.1",6379,2)
            redis_server = redis_connenction("192.168.123.65", 6379, 5)

            for key in redis_local.scan_iter("*"):
                # delete the key
                key_l = key.decode("utf-8")
                print(key_l)
                r_migrate = redis_local.get(key_l)
                print(r_migrate)
                redis_server.set(key_l,r_migrate)
                redis_local.delete(key)
        except Exception as ex:
            print
            'Error:', ex
            exit('Failed to connect, next try in 30s.')

        time.sleep(30)
