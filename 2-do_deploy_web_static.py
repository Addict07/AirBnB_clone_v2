#!/usr/bin/python3
# distributes an archive to your web servers, using the function do_deploy:

from os.path import exists
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ['54.237.3.221', '54.162.78.235']


def do_deploy(archive_path):
    """distributes an archive to your web servers, using the fun do_deploy"""

    if not exists(archive_path):
        return False

    try:
        # upload the file to the server
        put(archive_path, '/tmp/')

        file_name = archive_path.split('/')[-1].split('.')
        del file_name[-1]  # remove extension
        file_name = ' '.join(file_name)
        file_path = "/data/web_static/releases/{}".format(file_name)

        run("mkdir -p {}".format(file_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_path.split('/')[-1],
                                            file_path))
        run("rm /tmp/{}".format(archive_path.split('/')[-1]))

        run("mv {0}/web_static/* {0}".format(file_path))
        run("rm -rf {}/web_static".format(file_path))

        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(file_path, ))

        print("New version deployed!")
    except Exception:
        return False

    return True
