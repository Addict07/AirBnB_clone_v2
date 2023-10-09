#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

apt-get update -y
apt-get install nginx -y
ufw allow 'Nginx HTTP'

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
touch /data/web_static/releases/test/index.html
echo "<html>
    <head>
    </head>
    <body>
        <h2>Hello From ~AirBnB~</h2>
    </body>
</html>" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/

CONFIGs=\
"server {
    listen 80 default_server;

    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;

    root /etc/nginx/html;
    index index.html index.htm;

    location /redirect_me {
        return 301 https://github.com/Y-Baker;
    }

    error_page 404 /error_404.html;
    location /404 {
        root /etc/nginx/html;
        internal;
    }

    location /hbnb_static {
        alias /data/web_static/current/;
    }
}"
bash -c "echo -e '$CONFIGs' > /etc/nginx/sites-available/default"

service nginx restart
