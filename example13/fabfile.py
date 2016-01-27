from fabric.api import *

# This is a quick example of how we can use fabric to automate keeping a system up to date
# and ensuring that packages are installed on a server or set of servers. Note, a true
# production setup would be a lot more detailed.

env.user = 'luckner';
env.hosts = ['c7-1.vagrant']

def outputHeaders():
    print '';
    print env.host;
    print '==============================';

@task
def update():
    """
    Update the server
    """
    sudo('yum -y update');

@task
def install_vim():
    """
    Ensure that vim is installed
    """
    sudo('yum -y install vim');

@task
def install_httpd():
    """
    Ensure that httpd is installed
    """
    sudo('yum -y install httpd');

@task
def update_install():
    # Update
    update();

    # Install vim
    install_vim();

    # Install httpd
    install_httpd();
