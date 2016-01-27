from fabric.api import *

# What if you have a large number of hosts and you want to use the FQDN of the host
# instead of listing a bunch of IP addresses? I'm not sure if there is a "Fabric" way
# to do this but this is how I've accomplished this using command arguments
# fab sethosts:{host1,host2} uptime

def sethosts(hosts):
    env.user = 'luckner'
    for host in enumerate(hosts.split(' ')):
        fqdn = host[1] + '.vagrant';    # .vagrant is the extension for all my vagrant boxes
        env.hosts.append(fqdn);

def uptime():
    run('uptime');
