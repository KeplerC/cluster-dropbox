import os
import csv
import sys
import argparse
import statistics
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t",
    "--timeout",
    default=60,
    type=int,
    help="timeout limit (in seconds)")

parser.add_argument(
    "-f",
    "--filename",
    nargs='+',
    help="file names of result data")

parser.add_argument(
    "-l",
    "--lambdas",
    nargs='+',
    help="number of lambdas used in files")
args = parser.parse_args()

if (len(args.filename) != len(args.lambdas)):
    assert False, "lambdas length doesn't match with filename length"

experiment_dir = os.getcwd()
max_time = args.timeout * 1000
cost_per_ms = 0.34 / 3600000

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
            else:
                data  = line.split(', ')
                try: 
                    cost = float(data[1])
                    time = int(float(data[0]) * 1000)
                except Exception:
                    print("failure to parse")
                    continue
                local_min_time = min(local_min_time, time)
                min_time = min(time, min_time)
                
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
        
def create_dat(x_y_costs, filename, num_lambdas):
    csv_file = experiment_dir + "/" + filename
    with open(csv_file, 'w') as csvfile:
        for pair in x_y_costs:
            x, y = pair
            x = x * cost_per_ms * int(num_lambdas)
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

for i in range(len(args.filename)):
    file_name = args.filename[i]
    all_costs = []
    min_time = float('inf')
    fill_cost_dicts(file_name)
    x_y_costs_mean, x_y_costs_median, x_y_costs_std = combine_dicts()
    print("x_y_costs_median:", x_y_costs_median, "||")
    save_filename = file_name.split(".")[0]
    num_lambdas = args.lambdas[i]
    #create_dat(x_y_costs_mean, save_filename + "_merged_result_mean.csv")
    create_dat(x_y_costs_median, save_filename + "_merged_result_med.csv", num_lambdas)
    #create_std_dat(x_y_costs_mean, x_y_costs_std)

# fig, ax = plt.subplots()
# for file_name in file_names:
#     save_filename = file_name.split(".")[0]
#     mean = pd.read_csv(save_filename + "_merged_result_mean.csv", sep = "\t", names = ["time", "cost"])
#     mean.plot(kind='line',x='time',y='cost', ax=ax, label=save_filename)
# plt.savefig('merged_result_mean.png')

fig, ax = plt.subplots()
for file_name in args.filename:
    save_filename = file_name.split(".")[0]
    med = pd.read_csv(save_filename + "_merged_result_med.csv", sep = "\t", names = ["dollar_cost", "path_cost"])
    med.plot(kind='line',x='dollar_cost',y='path_cost', ax=ax, label=save_filename)
ax.set_xlabel("dollar cost")
ax.set_ylabel("path cost")
plt.savefig('merged_result_med.png')
