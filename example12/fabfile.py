import sys  # Sys provides functions such as exit()
from fabric.api import *

# Some of the key changes in this example:
# 1 - All output has been quieted. This allows us to grab the output of the command and display it
#     Perfect for when we need to return the data to be used by another program or just want it to be
#     more readable.
# 2 - outputHeaders is a small utility function which makes it easy to see which server the output is coming from.
#     Useful when running tasks against multiple servers
# 3 - Creating a dictionary of the values we want to pass into our command makes it easier to 1) reference the value
#     by a name instead of its position and 2) we can do some minimal validation :-)

output['running'] = False;
output['stdout'] = False;
output['status'] = False;

env.user = 'luckner';
env.hosts = ['c7-1.vagrant'];

process_name = '';

def outputHeaders():
    print '';
    print env.host;
    print '==============================';

def err(error = ''):
    opts = dict(error=error);
    print "Error: %(error)s" % opts;
    sys.exit();

@task
def find_process(proc = ''):
    opts = dict(
        proc=proc or process_name or err('proc must be set'),
    );
    output = run('ps aux | grep %(proc)s' % opts);
    outputHeaders();
    print output;
