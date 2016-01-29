from fabric.api import *

# Fabric's heart lies in its env dictionary. Keys defined in this dictionary are typically
# referred to as env variables. Here are some of the most common and important ones.

env.user = 'some_user'; # Current user by default. Controlled by -u on the command line
env.hosts = ['host@example.com'];   # Empty by default, controlled by -H on the command line
env.colorize_errors = True  # False by default
env.command_timeout = 2; # Remote command timeout period
env.eagerly_disconnect = False  # Default False, causes Fabric to close connections after every command rather than at the end of execution
env.forward_agent = True # Used to forward your local SSH Agent to the remote end
env.parallel = False # When True, forces all tasks to run in parallel
env.password = '';  # If not using ssh keys, a password can be specified for the user
env.pool_size = 2; # Number of processes to run at once when in parallel mode
env.roledefs = {};  # Dictionary mappings roles to host names
env.sudo_user = ''; # The user to run sudo commands with if different from sudo's user argument
env.warn_only = False; # If errors occur and this is True, execution continues with a simple warning.
