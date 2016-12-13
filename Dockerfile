server{
      listen 80;
      server_name blog.joway.wang;

      location / {
          rewrite (.*) https://blog.joway.wang$1 permanent;
      }
}

server  {

    listen 443 ssl;
    server_name blog.joway.wang;

    include pagespeed/ngx_pagespeed.conf;


    ssl on;
    ssl_certificate $NGINX_PREFIX/certs/blog.joway.wang.crt;
    ssl_certificate_key $NGINX_PREFIX/certs/blog.joway.wang.key;

    ssl_prefer_server_ciphers on;
    # ssl_dhparam /etc/ssl/certs/dhparam.pem;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS !RC4";
    keepalive_timeout 70;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    add_header Strict-Transport-Security max-age=63072000;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;

    index index.html index.htm index.php;

    location / {
        proxy_pass         http://inter.qc.joway.wang:8008;
        #proxy_redirect    off;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP  $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   Referer http://$host;
        # proxy_set_header X-Forwarded-Proto https;

        # 允许超过频率限制的请求数不多于50个 超过的请求不被延迟处理
        limit_req zone=limited burst=50 nodelay;
    }
}

