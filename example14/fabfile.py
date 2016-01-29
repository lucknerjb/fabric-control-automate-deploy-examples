from fabric.api import *

# This example makes use of the get() and put() commands to place and retrieve files from a server.
# You'll notice that the upload() task also introduces context managers. You would think that if you did:
# cd('some/path')
# run('some command')
# run('another command')
# that the last two commands would be run from within the path you CD'd into.... wrong. Using context managers
# such as "with cd()" allows you to get the expected behavior

env.user = 'luckner';
env.hosts = ['c7-1.vagrant']

@task
def upload(file, destination_path):
    """
    Upload a file to the server
    """
    with cd(destination_path):
        put('%s' % file, 'some_file', use_sudo=True);

@task
def download(file):
    """
    Download a file from the server
    """
    get(remote_path='%s' % file, local_path='/tmp', use_sudo=True);
