#!/usr/bin/python3
# creates and distributes an archive to your web servers
# using the function deploy

from datetime import datetime
from fabric.api import local, env, run, put
from fabric.api import runs_once
from os.path import exists

env.hosts = ['54.237.3.221', '54.162.78.235']


@runs_once
def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""
    local("mkdir -p ./versions")

    time_now = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "web_static_{}.tgz".format(time_now)

    result = local("tar -czvf ./versions/{} web_static/".format(file_name))
    if result.succeeded:
        return "versions/{}".format(file_name)
    else:
        return None


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


def deploy():
    """creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    return False
