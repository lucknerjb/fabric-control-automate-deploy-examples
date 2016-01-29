from fabric.api import *

# Running commands on a remote host are as easy as running them on a local host.
# On the command line, passing in the -H argument allows you to list the hosts that you want to run the command(s) against
# You can also pass in the -u argument to set the user to connect as
# fab sethosts uptime

def sethosts():
    # host c7-1
    env.hosts = ['c7-1.vagrant'];
    env.user = 'luckner';

def uptime():
    run('uptime');
