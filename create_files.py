#Detect local mounted disk (make sure it is local) with at least X MB free space, create Z files of size Y,
# run Z “dd” processes which where each process will fill selected file
# with Data and print time took to complete the work.
import subprocess
import re
import time



z = 2
y = 10000000
c = 20 #dd count
x = 100000
timeout = 10
ddif = "/dev/urandom"
wd='/tmp'

#search disk with X free


cp = subprocess.run(["df", "-l", "/dev/null"], stdout=subprocess.PIPE, shell=True)
#print (cp.stdout)
#dev                 8366874624             0   8366874624   0% /dev
#/dev/sda2          41149652992   20627255296  18408468480  53% /

mount_point=''
p = re.compile('(/dev/.*)\s+\d+\s+\d+\s+(\d+)\s+\d+%\s+(.*)', re.IGNORECASE)
for line in cp.stdout.splitlines():
    string = line.decode("utf8")
#    print("str:"+str)
    res = p.search(string)
    if res:
        if int(res.group(2)) > x:
            print("Found appropriate mount:"+res.group(3))
            mount_point = res.group(3)

            break
processes=[]
for i in range(z):
    cmd = "dd if=" + ddif + " of=" + mount_point + wd + "/file_" + str(i) + " bs=" + str(y) + " count=" + str(c)
    print("Run cmd:"+cmd)
    p = subprocess.Popen(cmd, shell=True)
              #stdin=PIPE,
              #stdout=PIPE,
              #stderr=PIPE,
              #close_fds=True)
    processes.append(p)
    print("Started")

starttime = time.time()

active_processes = 100

print("Observing status")
while active_processes > 0:
    for p in processes:
        active_processes = 0
        if p.poll() is None:
            active_processes += 1
    print("Active processes:"+ str(active_processes))
    if active_processes > 0:
        time.sleep(1)
endtime = time.time()
print("Completed in (with 1-2 sec precision error):" + str(endtime - starttime))





