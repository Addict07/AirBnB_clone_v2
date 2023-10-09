#!/usr/bin/python3
# Deletes out-of-date archives

from fabric.api import local, run, env

env.hosts = ['54.237.3.221', '54.162.78.235']


def do_clean(number=0):
    """deletes out-of-date archives"""
    number = 1 if int(number) == 0 else int(number)

    # remove local
    total = local("ls -l versions/*.tgz | wc -l", capture=True).stdout.strip()
    total = int(total)
    c = "find {} -type f -exec ls -t1 {{}} + | tail -{} | xargs rm -rf"
    local(c.format('versions/*.tgz', total - number))

    # remove Host
    path = "/data/web_static/releases/"
    total = run("find {} -type d -name 'web_static*' | wc -l"
                .format(path)).stdout.strip()
    total = int(total)
    c = "ls -dt {}web_static_* | tail -{} | xargs rm -rf"
    run(c.format(path, total - number))
