import os
import csv
import sys
import statistics
import pandas as pd
import matplotlib.pyplot as plt

experiment_dir = os.getcwd()
num_args = len(sys.argv)
file_names = sys.argv[1:num_args-1]
timeout = sys.argv[num_args-1]
max_time = int(timeout) * 1000

def fill_cost_dicts(file_name):
    global min_time
    result_path = os.path.join (experiment_dir, file_name)
    with open(result_path, 'r') as infile:
        local_min_time = float('inf')
        cost_dict = {}
        for line in infile:
            if 'T' in line:
                if cost_dict:
                    min_val_so_far = float('inf')
                    for t in range(local_min_time, max_time):
                        if t in cost_dict:
                            min_val_so_far = min(min_val_so_far, cost_dict[t])
                        if min_val_so_far > 100000000:
                            print("uh oh")
                        cost_dict[t] = min_val_so_far
                    all_costs.append(cost_dict)
                local_min_time = float('inf')
                cost_dict = {}
                print("found T")
            else:
                data  = line.split(', ')
                print(data)
                try: 
                    cost = float(data[1])
                    time = int(float(data[0]) * 1000)
                    print(time)
                except Exception:
                    print("failure to parse")
                    continue
                local_min_time = min(local_min_time, time)
                min_time = min(time, min_time)
                print(min_time)
                if time in cost_dict:
                    cost_dict[time] = min(cost_dict[time], cost)
                else:
                    cost_dict[time] = cost

    if cost_dict:
                    min_val_so_far = float('inf')
                    for t in range(local_min_time, max_time):
                        if t in cost_dict:
                            min_val_so_far = min(min_val_so_far, cost_dict[t])
                        if min_val_so_far > 100000000:
                            print("uh oh")
                        cost_dict[t] = min_val_so_far
                    all_costs.append(cost_dict)

    if min_time > max_time:
        assert False, "unable to find experiment."

def combine_dicts():
    global min_time
    avgs = []
    meds = []
    sds = []
    for t in range(min_time, max_time):
        costs = []
        for d in all_costs:
            if t in d:
                costs.append(d[t])
            else:
                costs.append(float('inf'))
        try:
            avgs.append([t, statistics.mean(costs)])
            meds.append([t, statistics.median(costs)])
        except Exception:
            print("No data point at time", t)
        #sds.append([t, statistics.pstdev(costs)])
    return avgs, meds, sds      
        
def create_dat(x_y_costs, filename):
    csv_file = experiment_dir + "/" + filename
    with open(csv_file, 'w') as csvfile:
        for pair in x_y_costs:
            x, y = pair
            to_write = str(x) + "\t" + str(y) + "\n"
            csvfile.write(to_write)
    print(".dat file generated: " + csv_file)


# def create_std_dat(x_y_costs_mean, x_y_costs_std):
#     dat_file = experiment_dir + '/merged_result_sd.csv'
#     with open(dat_file, 'w') as datfile:
#         for mean, std in zip(x_y_costs_mean, x_y_costs_std):
#             x_mean, y_mean = mean
#             x_std, y_std = std
            
#             to_write_upper = str(x_mean) + "\t" + str(y_mean + y_std) + "\n"
#             to_write_lower = str(x_mean) + "\t" + str(y_mean - y_std) + "\n"
#             datfile.write(to_write_upper)
#             datfile.write(to_write_lower)

for file_name in file_names:
    all_costs = []
    min_time = float('inf')
    fill_cost_dicts(file_name)
    x_y_costs_mean, x_y_costs_median, x_y_costs_std = combine_dicts()
    save_filename = file_name.split(".")[0]
    #create_dat(x_y_costs_mean, save_filename + "_merged_result_mean.csv")
    create_dat(x_y_costs_median, save_filename + "_merged_result_med.csv")
    #create_std_dat(x_y_costs_mean, x_y_costs_std)

# fig, ax = plt.subplots()
# for file_name in file_names:
#     save_filename = file_name.split(".")[0]
#     mean = pd.read_csv(save_filename + "_merged_result_mean.csv", sep = "\t", names = ["time", "cost"])
#     mean.plot(kind='line',x='time',y='cost', ax=ax, label=save_filename)
# plt.savefig('merged_result_mean.png')

fig, ax = plt.subplots()
for file_name in file_names:
    save_filename = file_name.split(".")[0]
    med = pd.read_csv(save_filename + "_merged_result_med.csv", sep = "\t", names = ["time", "cost"])
    med.plot(kind='line',x='time',y='cost', ax=ax, label=save_filename)
plt.savefig('merged_result_med.png')
