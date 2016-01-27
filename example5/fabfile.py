from fabric.api import *

# Passing arguments to a command is quite easy really
# Note that arguments should be escaped if they contain special characters such as spaces or ampersands, etc...
# This means that running: fab hello:Marco Polo => would result in an error as fabric thinks you are running the hello
# command with the argument "Marco" followed by the Polo command.
#
# fab hello:"Marco Polo"

def hello(name):
    print("Hello %s" % name);
