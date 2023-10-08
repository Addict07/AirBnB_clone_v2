#!/usr/bin/python3
# Deletes out-of-date archives

from fabric.api import local, run, env

env.hosts = ['54.237.3.221', '54.162.78.235']


def do_clean(number=0):
    """deletes out-of-date archives"""
    number = 2 if number == 0 else number + 1

    c = "find {} -type f -exec ls -t1 {{}} + | tail -{} | xargs rm -rf"
    local(c.format('versions/', number))
    path = '/data/web_static/releases'
    run(c.format(path, number))
