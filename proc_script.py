import os 
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import re
import numpy as np
from operator import itemgetter


for log in os.listdir("."):
    if not log.startswith("fetch"):
        continue
    with open(log) as f:
        print(log)
        readed = f.read()
        experiments = []
        for line in readed.split("printing waypoints"):
            experiments.append(re.findall(r'\n[0-9]+.[0-9]+, [0-9]+.[0-9]+\n', line))
        s = ""
        total_trial_number = len(experiments)
        l = []
        for trial_number in range(total_trial_number):
            s += ("T" + str(trial_number) + "\n")
            costs = []
            times = []
            for i in (experiments[trial_number]):
                if not i:
                    continue
                splitted = i.split(", ")
                costs.append(float(splitted[1]))
                times.append(float(splitted[0]))
                s+=(i.strip() + "\n")
        print(s)
        with open("exp_" + log, "w") as f:
            f.write(s[:-5])
