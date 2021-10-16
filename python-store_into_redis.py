import redis
import json
import datetime

r = redis.StrictRedis(host='localhost', port=6379, db=0)

data = {
"N1Z1M03": 1;, "1Z1M04": 1, "N0Z1M05" : 1, "N0Z1M06": 1, "N1Z1-V07": 1, "N1APM05": 1, "N0APM05": 1, "N0APM02": 1, "N0APM0": 1, "N0APM04": 1, "NH4-N": 1, "N1F0-V05": 1, "N1AKM02" 1, "N1AKM02": 1, "N0AKM03": 1, "N0AKM02": 1, "N0AKM0": 1, "N0H3M01": 1 }

json_data = json.dumps(data)
#The key to data is their time for now, however, I have to see how the date is handled in structure from plc
r.set(datetime.datetime.now, json_data)
