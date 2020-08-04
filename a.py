import os, subprocess
import time



num_proc = 5
num_thread = 8
time_length = 30000
trials = 10
run = 0

os.environ["OMP_NUM_THREADS"] = str(num_thread)
while run < trials:
  subprocess.run(["cd /anna && ./scripts/stop-anna-local.sh remove_logs"], stdout=open('/log.txt', 'a'), stderr=open('/log_err.txt', 'a'), shell=True)
  time.sleep(1)
  subprocess.run(["cd /anna && ./scripts/start-anna-local.sh build"], stdout=open('/log.txt', 'a'), stderr=open('/log_err.txt', 'a'), shell=True)
  time.sleep(1)
  print("Trial " + str(run) )
  p = []

  for i in range(num_proc):
    filename = '/log_run_' + str(run) + '_nthread_'+ str(num_thread) + '_lambda_' + str(i)
    execution_command = '/mplambda/build/mpl_lambda_pseudo --scenario fetch --algorithm cforest --coordinator "$COORDINATOR" --jobs 10 --env AUTOLAB.dae --env-frame=0.38,-0.90,0.00,0,0,-1.570796326794897 --goal=-1.07,0.16,0.88,0,0,0 --goal-radius=0.01,0.01,0.01,0.01,0.01,3.141592653589793 --start=0.1,1.570796326794897,1.570796326794897,0,1.570796326794897,0,1.570796326794897,0 --time-limit '+ str(time_length) +' --check-resolution 0.01 --anna_address 127.0.0.1 --local_ip  127.0.0.1 --execution_id solution_key_1595284680.778267 --thread_id ' + str(i) 
    p.append(subprocess.Popen([execution_command], stdout=open(filename, 'a'), stderr=subprocess.STDOUT, shell=True))
  time.sleep(time_length)

  subprocess.Popen(["pkill -f my_pattern"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True) 
  run += 1 
