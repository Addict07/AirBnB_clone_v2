#!/usr/bin/python3
# Fabfile to generates a .tgz archive from the contents of web_static.

from datetime import datetime
from fabric.api import local


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""
    local("mkdir -p ./versions")

    time_now = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "web_static_{}.tgz".format(time_now)

    result = local("tar -czvf ./versions/{} web_static/".format(file_name))
    if result and result.succeeded:
        return "versions/{}".format(file_name)
    else:
        return None
