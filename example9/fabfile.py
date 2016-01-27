from fabric.api import *

# Dealing with an outage? Trying to figure out why your server is being sluggish?
# Well, grab some stats - but forget SSHing into that server!

@task
def memory():
    run('free -mh --total');

@task
def disk_space(dir = ''):
    if dir:
        # Using sudo here in case we want to grab the disk space of /etc.
        # You could have sudo be an option that gets passed into the command instead
        sudo('du -sh %s' % dir);
    else:
        run('df -hP --total');

@task
def process(proc):
    run('ps aux | grep %s' % proc);

# This setup function basically does what sethosts() did in the previous examples except that we call
# it automatically every time we execute a fab task. This is a great way to bootstrap your fabfile.
def setup():
    env.user = 'luckner';
    envHosts = env.hosts;
    env.hosts = [];
    for host in enumerate(envHosts):
        fqdn = host[1] + '.vagrant';    # .vagrant is the extension for all my vagrant boxes
        env.hosts.append(fqdn);

setup();
