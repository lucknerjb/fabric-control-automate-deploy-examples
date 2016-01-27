from fabric.api import *

# What if you're unsure if a process is running on a server?

@task
def find_process(proc):
    run('ps aux | grep %s' % proc);

@task
def watch_process(proc):
    run('watch "ps aux | grep %s"' % proc);

def setup():
    env.user = 'luckner';
    envHosts = env.hosts;
    env.hosts = [];
    for host in enumerate(envHosts):
        fqdn = host[1] + '.vagrant';
        env.hosts.append(fqdn);

setup();
