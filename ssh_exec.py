#Run user-selected command on many servers (user provided as param) with ssh in parallel,
# collect output from all nodes. Script should print collected output from all
#  nodes on stdout, w/o using temp files.

import paramiko

class SshProc:
    ssh = None
    stdout = None
    sdterr = None
    id     = None

    def __init__(self, sshp, stdoutp, stderrp, id):
        self.ssh    = sshp
        self.stdout = stdoutp
        self.stderr = stderrp
        self.id     = id


nodes = ["127.0.0.1", "127.0.0.1"]

username = 'tomcat'
password = 'tomcat'

cmd = "ls -la /"

#cmd =  "ping 8.8.8.8  -c 20 -i 5"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

sshs = []

for n in nodes:
    ssh.connect(hostname=n,
            password=password,
            username=username)
    sshs.append(ssh)
print("Connected")

sps=[]
id = 0;
for ssh in sshs:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    sp =  SshProc( ssh, stdout, stderr, id)
    sps.append(sp);
    id += 1

print("Started")

print("Observing")
completed = False
while not completed:
    read_done = False
    for sshproc in sps:
        stdout_line = sshproc.stdout.readline()
        if(stdout_line):
            print(str(sshproc.id) +"stdout:" + stdout_line)
            read_done = True

        stderr_line = sshproc.stderr.readline()
        if(stderr_line):
            print(str(sshproc.id) +"stderr:" + stderr_line)
            read_done = True

    if not read_done:
        completed = True





