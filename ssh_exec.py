#Run user-selected command on many servers (user provided as param) with ssh in parallel,
# collect output from all nodes. Script should print collected output from all
#  nodes on stdout, w/o using temp files.

import paramiko
import select
import time

class SshProc:
    ssh = None
    channel = None
    stdout = None
    sdterr = None
    id     = None

    def __init__(self, sshp, channelp, id):
        self.ssh    = sshp
        self.channel = channelp
        self.id     = id


nodes = ["127.0.0.1", "127.0.0.1"]

username = 'tomcat'
password = 'tomcat'

#cmd = "ls -la /"

cmd =  "ping 8.8.8.8  -c 20 -i 5"



sshs = []

for n in nodes:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=n,
            password=password,
            username=username)
    sshs.append(ssh)
print("Connected")

sps=[]
id = 0;
for ssh in sshs:
    channel = ssh.get_transport().open_session()
    channel.exec_command(cmd)
    sp = SshProc(ssh, channel, id)
    sps.append(sp);
    id += 1

print("Started")

print("Observing")
completed = False
while not completed:
    read_done = False
    for sshproc in sps:

        if not sshproc.channel.exit_status_ready():
            completed = False

        rl, wl, xl = select.select([channel], [], [], 0.0)

        if len(rl) > 0:
            print( str(sshproc.id) +" stdout:" + channel.recv(1024).decode('utf8'))
            read_done = True

#    if not read_done:
#        time.sleep(1)

#        if sshproc.channel.recv_ready():
#            stdout = channel.makefile()
#            stdout_line = stdout.readline()
#            print(str(sshproc.id) +"stdout:" + stdout_line)

#        if sshproc.channel.recv_stderr_ready():
#            stderr = channel.makefile_stderr()
#            stderr_line = stderr.readline()
#            print(str(sshproc.id) +"stderr:" + stderr_line)







