from fabric.api import *

# We've all done rsync deployments before right? Well let's get it done via fab now.

env.user = 'luckner';
env.hosts = ['c7-1.vagrant'];

source_path = '/tmp/secret-project';
dest_path = '/tmp/example17';
user='luckner';

@task
def deploy(source_path = '', dest_path = '', user = '', host = ''):
    """
    Deploy our super top-secret project to production
    """

    opts = dict(
        source_path=source_path or source_path or err('env.source_path must be set'),
        dest_path=dest_path or dest_path or err('env.dest_path must be set'),
        user=user or env.get('user') or err('env.user must be set'),
    );

    # Loop through our hosts and deploy the code
    for host in enumerate(env.hosts):
        opts['host'] = host[1];
        local('rsync -rlptoDvz --no-p --no-g --chmod=u=rwx,go=rx --delete %(source_path)s/* %(user)s@%(host)s:%(dest_path)s' % opts);
