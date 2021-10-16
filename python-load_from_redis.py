import redis
import json
import datetime

r = redis.StrictRedis(host='localhost', port=6379, db=0)

#The key to data is their time for now, however, I have to see how the date is handled in structure from plc
json_data = r.get(datetime.datetime.now)