from fabric.api import *

# Using the @task notation above a function definition tells fabric that the following function
# is a task. As soon as you insert an @task notation, any function without it is no longer
# accessible from the command line. Perfect for "private" commands

@task
def public():
    print("This is a public command");

@task
def call_private():
    private();

def private():
    print("This is a private command");
