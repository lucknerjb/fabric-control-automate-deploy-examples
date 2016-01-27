from fabric.api import *

# There are going to be times when you want to run some tasks against
# certain hosts and other tasks against other hosts. That's when being able
# to set the hosts on the command line comes in handy.
# fab -H {hosts} uptime

env.user = 'luckner'

def uptime():
    run('uptime');
