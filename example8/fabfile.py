from fabric.api import *

# This example may seem trivial but it's a good starting point in showing how easy it is to
# start taking control of your infrastructure. How often do we find ourselves logging into
# servers to check on the status of a particular service?

@task
def service_start(service):
    sudo('service %s start' % service);

@task
def service_restart(service):
    sudo('service %s restart' % service);

@task
def service_status(service):
    sudo('service %s status' % service);

@task
def service_stop(service):
    sudo('service %s stop' % service);

@task
def service(service, command):
    sudo('service %s %s' % (service, command));

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
