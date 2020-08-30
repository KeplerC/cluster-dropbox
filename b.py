import os 
import re
from datetime import datetime

def get_timestamp(s):
    return datetime.strptime(s.split(" ")[0], '%H:%M:%S.%f')


def parse_log_file(dir_name, log_name):
    log_file = dir_name+ log_name
    with open(log_file) as f:
        content = f.read()
    lines = [l for l in content.split("\n") if l.find("solution") != -1]
    start = get_timestamp(content.split("\n")[0])
    time = []
    costs = []
    for i in range(len(lines)):
        line = lines[i]
        cost = re.findall(r' [0-9][0-9].[0-9][0-9][0-9][0-9]', line)
        if not cost:
            continue
        try:
            get_timestamp(line)
        except:
            continue
        if (get_timestamp(line) -start).total_seconds() < 0:
            time.append((get_timestamp(line) -start + timedelta(days=1)).total_seconds())
        else:
            time.append((get_timestamp(line) -start).total_seconds())
        costs.append(float(cost[0].strip()))
    return costs, time 

import sys
counter = 1
dir_name = sys.argv[1]
for log in os.listdir(dir_name):
    s = ("T{}\n".format(counter))
    st = ""
    costs, times = parse_log_file(dir_name, log)
    for j in range(len(costs)):
        st += ("{}, {}\n".format(times[j], costs[j]))
    counter += 1
    if st:
        print(s + st)
