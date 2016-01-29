from fabric.api import *

# We've all done rsync deployments before right? Well let's get it done via fab now.

env.user = 'luckner';
env.hosts = ['test.nonexistent.com'];

host_dict = dict(
    production = ['c7-1.vagrant'],
    staging = ['c7-2.vagrant']  # Does not exist for the purpose of this example
);

source_path = '/tmp/secret-project-deploy';
dest_path = '/tmp/example17';

@task
def deploy(branch='', tag='', environment='production'):
    """
    Deploy our super top-secret project
    """

    opts = dict(
        source_path=source_path or err('env.source_path must be set'),
        dest_path=dest_path or err('env.dest_path must be set'),
        user=env.user,
    );

    # Get the hosts that we are supposed to deploy to
    env.hosts = host_dict[environment];

    # Update the project dir
    # warn_only=True ensures that if there is an error, we continue execution
    # It's not optimal but is necessary if the branch or tag already exists and we try and create it
    # In a production scenario, you would want to ensure that the branch does not exist before trying to create it
    with settings(warn_only=True):
        with lcd(source_path):
            local('git fetch --all');
            if branch:
                local('git checkout -b origin/%s %s' % (branch, branch));
            elif tag:
                local('git checkout -b %s tags/%s' % (tag, tag));

            # Loop through our hosts and deploy the code
            for host in enumerate(env.hosts):
                opts['host'] = host[1];
                local('rsync -rlptoDvz --no-p --no-g --chmod=u=rwx,go=rx --delete %(source_path)s/* %(user)s@%(host)s:%(dest_path)s' % opts);
