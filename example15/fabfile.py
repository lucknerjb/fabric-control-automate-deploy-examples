from fabric.api import *

# Performing backups can be quite a simple task as well
# This script coule be extended to place the backups on a remote server
# Throw a cron in front of this set of fab commands and you have an automated backup strategy

env.user = 'luckner';
env.hosts = ['c7-1.vagrant']

def create_mysql_backup():
    """
    Backup mysql schema and data
    """
    run('mysqldump -u root -proot main_db > /tmp/main_db.sql');

def tar_mysql_backup():
    """
    Backup some files
    """
    run('cd /tmp && tar cvf main_db.sql main_db.tar ');

@task
def backup_mysql():
    create_mysql_backup();
    tar_mysql_backup();
