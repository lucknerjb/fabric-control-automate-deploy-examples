from fabric.api import *

# In this example, we're going to create a user on the remote server and force them to
# change their password on first login

env.user = 'luckner';
env.hosts = ['c7-1.vagrant']
default_password = 'change-me'

@task
def create_user(username, shell='/bin/bash'):
    """
    Create a user with or without a login shell and password
    """

    opts = dict(
        username=username or env.get('username') or err('env.username must be set'),
        shell=shell or env.get('shell') or err('env.shell must be set'),
    )
    sudo('useradd -s %(shell)s -m -c "Created by fab" %(username)s' % opts);

    # Read the user's password from the command line
    password = prompt('Please supply a password for this user: ')

    # Optional validation. Note: With validation, the input MUST match the regex. No pressing ENTER to "cancel"
    # password = prompt('Please supply a password for this user: ', validate=r'^\w{2,16}?$'))

    # Change the password
    if password:
        sudo('echo "%s:%s" | chpasswd' % (username, password));
    # Force the user to change their password on first login
    else:
        sudo('echo "%s:%s" | chpasswd' % (username, default_password));
        sudo('chage -d 0 %s' % username);
