from fabric.api import local, run, env, put, task, sudo, cd, lcd
import timeit

# This example fabfile will setup a basic server with the following:
# Packages: wget, vim, apache(httpd), php and mysql
# Users: user1 (some employee), deployer (a deploy user)

env.user = 'luckner';
env.hosts = ['c7-1.vagrant'];

config_dict = {
    'base_path': '/Users/lucknerjb/workspace/Talks/03_02_2016_fabric_control_automate_deploy/example19',
    'remote_rpm_path': '/root/rpms',
    'bootstrap_file_path': '/root/bootstrapped',
    'apache_webroot': '/var/www/html/example19',
    'apache_conf_path': '/etc/httpd/conf.d',
    'is_bootstrapped': False,
    'users': ['user1', 'deployer'],
    'default_password': 'change-me',
    'user_shell': '/bin/bash',
    'packages': [
        'wget',
        'vim',
        'httpd',
        'php'
    ],
    'mysql_rpm': 'mysql-community-release-el7-5.noarch.rpm',
    'ssh_key': 'PLACE_SSH_KEY_HERE'
};

@task
def install_server():
    """
    Our install process for initial setup and continuous integrity checks
    """

    start = timeit.default_timer();

    # Check if the server is bootstrapped
    check_if_bootstrapped();

    # Update the server
    update_server();

    # Install packages
    install_packages();

    # Setup RPM for mysql
    install_mysql_rpm();

    # Setup mysql
    if config_dict['is_bootstrapped'] == False:
        setup_mysql();

    # Create users
    create_users();

    # Setup our SSH Key for password-less auth
    setup_ssh_keys();

    # Setup Apache
    setup_apache();

    # Deploy
    deploy_webroot();

    # Make sure all services are started
    start_services();

    stop = timeit.default_timer();
    total_time = stop - start;
    print 'Total Execution Time: ' + "{:.3f}".format(total_time)  + ' seconds';

def check_if_bootstrapped():
    """
    Certain actions should not be performed if we are already bootstrapped, so let's check if we are
    """

    outputHeaders('check_if_bootstrapped');

    exists = file_exists(config_dict['bootstrap_file_path'], True);
    config_dict['is_bootstrapped'] = True if exists else False;

def update_server():
    """
    Run yum update on the server
    """

    outputHeaders('update_server');

    sudo('yum -y update');

def install_packages():
    """
    Install some basic packages
    """

    outputHeaders('install_packages');

    sudo('yum install -y %s' % ' '.join(config_dict['packages']));

def install_mysql_rpm():
    """
    Upload the mysql rpm and install it
    """

    outputHeaders('install_mysql_rpm');

    # Create the path where we will store our RPMs
    sudo('mkdir -p %s' % config_dict['remote_rpm_path']);

    # Build the local rpm path
    rpm_path = [
        config_dict['base_path'],
        'rpms',
        config_dict['mysql_rpm']
    ]

    # Upload
    with cd(config_dict['remote_rpm_path']):
        put('%s' % '/'.join(rpm_path), config_dict['mysql_rpm'], mode=644, use_sudo=True);

        # Install RPM if it is not already installed
        installed = check_rpm_installed(config_dict['mysql_rpm']);
        if installed == False:
            sudo('rpm -ivh %s' % config_dict['mysql_rpm']);

    # Run yum update
    update_server();

    # Install mysql
    sudo('yum install -y mysql-server');

def setup_mysql():
    """
    Run the equivalent of mysql_secure_installation
    """

    outputHeaders('setup_mysql');

    mysql_secure_install_cmd = [
        'mysql -u root <<-EOF',
        'UPDATE mysql.user SET Password=PASSWORD("%s") WHERE User="root";' % 'beefcake123',
        'DELETE FROM mysql.user WHERE User="root" AND Host NOT IN ("localhost", "127.0.0.1", "::1");',
        'DELETE FROM mysql.user WHERE User="";',
        'DELETE FROM mysql.db WHERE Db="test" OR Db="test\_%";',
        'FLUSH PRIVILEGES;',
        'EOF'
    ];

    sudo("\n".join(mysql_secure_install_cmd));

def create_users():
    """
    Create a set of users
    """

    outputHeaders('create_users');

    for user in enumerate(config_dict['users']):
        # Do not attempt to create the user if they already exist
        user_exists = check_if_user_exists(user[1]);
        if (user_exists):
            continue;

        opts = {
            'shell': config_dict['user_shell'],
            'username': user[1]
        };
        sudo('useradd -s %(shell)s -m  -c "Created by fab" %(username)s' % opts);
        sudo('echo "%s:%s" | chpasswd' % (user[1], config_dict['default_password']));

def setup_ssh_keys():
    """
    Add our SSH keys so we can login as the various users we setup
    """

    outputHeaders('setup_ssh_keys');

    # Get SSH key
    ssh_key = config_dict['ssh_key'];
    opts = {'ssh_key': ssh_key};

    for user in enumerate(config_dict['users']):
        opts['user'] = user[1];
        sudo('mkdir -p /home/%(user)s/.ssh' % opts);
        sudo('touch /home/%(user)s/.ssh/authorized_keys' % opts);

        # Only append the SSH key if it does not exist
        ssh_key_exists = check_if_ssh_key_present(ssh_key, '/home/%(user)s/.ssh/authorized_keys' % opts);
        if ssh_key_exists == False:
            sudo('echo %(ssh_key)s >> /home/%(user)s/.ssh/authorized_keys' % opts);

        sudo('chown -R %(user)s:%(user)s /home/%(user)s/.ssh' % opts);
        sudo('chmod 700 /home/%(user)s/.ssh' % opts);
        sudo('chmod 600 /home/%(user)s/.ssh/authorized_keys' % opts);

def setup_apache():
    """
    Create the webroot and upload the vhost config
    """

    outputHeaders('setup_apache');

    opts = {
        'webroot': config_dict['apache_webroot'],
        'user': 'deployer',
    };

    # Create webroot
    sudo('mkdir -p %(webroot)s' % opts);
    sudo('chown %(user)s:%(user)s %(webroot)s' % opts);

    # Copy over the config
    conf_path = config_dict['base_path'] + '/apache_configs/example19.conf';
    with cd(config_dict['apache_conf_path']):
        put('%s' % conf_path, 'example19.conf', mode=0644, use_sudo=True);
        sudo('chown root:root example19.conf'); # This needs to owned by root

        # Still trying to figure out why this happens but for some reason, when PUTing files through Fab,
        # it seems as though the improper security context is set on the file. Bypassing the following line
        # would result in httpd not being able to restart as it would not be allowed to access the config file
        sudo('chcon -t httpd_config_t -u system_u example19.conf');

def deploy_webroot():
    """
    Deploy our initial code to the server
    """

    opts = {
        'source_path': config_dict['base_path'] + '/webroot',
        'dest_path': config_dict['apache_webroot'],
        'user': 'deployer'
    };

    # Loop through our hosts and deploy the code
    for host in enumerate(env.hosts):
        opts['host'] = host[1];
        local('rsync -rlptoDvz --no-p --no-g --chmod=u=rwx,go=rx --delete %(source_path)s/* %(user)s@%(host)s:%(dest_path)s' % opts);

def start_services():
    """
    Make sure that apache and mysql are started
    Normally, you would also use chkconfig to make sure these services start on boot
    """

    outputHeaders('start_services');

    sudo('service httpd restart');
    sudo('service mysql restart');

def check_if_ssh_key_present(ssh_key, file):
    """
    Check to see if a SSH key is already added to a user's authorized_keys
    """

    opts = {'ssh_key': ssh_key, 'file': file};

    output = sudo('cat %(file)s | grep "%(ssh_key)s" | wc -l' % opts);
    return True if (output == '1') else False;

def check_if_user_exists(username):
    """
    Check to see if a user has already been created
    """

    # getent will return 0 if the user exists or 2 if they do not
    output = sudo('getent passwd %s > /dev/null 2&>1; echo $?' % username);
    return True if (output == '0') else False;

def check_rpm_installed(rpm):
    """
    Check to see if an rpm is already installed
    """
    rpm = rpm.replace('.rpm', '');
    output = sudo('rpm -qa | grep "%s" | wc -l' % rpm);
    return True if (output == '1') else False;

def file_exists(file, use_sudo = False):
    """
    Check to see if a file exists.
    """
    if use_sudo:
        output = sudo('ls -l %s | wc -l' % file);
    else:
        output = run('ls -l %s | wc -l' % file);
    return True if (output == '1') else False;

def outputHeaders(command = ''):
    print '';
    print env.host + '[ ' + command + ' ]';
    print '==============================';
