nginx2f5
========

This is a python script to translate nginx configuration to F5 syntax

Install using pip:

`pip install nginx2f5`

Usage: nginx2f5 <filename> [partition]

In v1.0 this only works for the stream loadbalancing configuration.

Output is to stdout so redirect to a file, remove warnings and non-commented lines and copy to BIG-IP in /var/tmp directory. Load output configuration with `tmsh load sys config merge file /var/tmp/<output file>`. Use `verify` extension to test the configuration syntax but not load into running configuration.

Example:
Config file:

```
worker_processes auto;

error_log /var/log/nginx/error.log info;

events {
    worker_connections  1024;
}

stream {
    upstream backend {
        hash $remote_addr consistent;
        server backend1.example.com:12345 weight=5;
        server 127.0.0.1:12345            max_fails=3 fail_timeout=30s;
        server unix:/tmp/backend3;
    }

    upstream dns {
       server 192.168.0.1:53535 down;
       server dns.example.com:53 backup down;
    }

    server {
        listen 12345;
        proxy_connect_timeout 1s;
        proxy_timeout 3s;
        proxy_pass backend;
    }

    server {
        listen 127.0.0.1:53 udp reuseport;
        proxy_timeout 20s;
        proxy_pass dns;
    }

    server {
        listen [::1]:12345;
        proxy_pass unix:/tmp/stream.socket;
    }
}
```


Output:
```
$ nginx2f5 config
# -- Running with Python v2.7.16 (default, Mar 20 2019, 12:15:19)
[GCC 7.4.0]
#--- Pools ---
ltm pool pool-dns {
        monitor /Common/udp
        load-balancing-mode round-robin
        min-active-members 1
                192.168.0.1:53535 {
                state user-disabled
                }
                dns.example.com:53 {
                 priority 1
                }
        }
}
ltm pool pool-backend {
        monitor /Common/tcp
        load-balancing-mode round-robin
        members {
                backend1.example.com:12345 {
                }
                127.0.0.1:12345 {
                }
        }
}
#--- /Pools ---
#--- VS ---
ltm virtual vs-1 {
        destination 0.0.0.0:12345
        profiles {
                /Common/tcp { }
        }
        pool pool-backend
}
ltm virtual vs-2 {
        destination 127.0.0.1:53
        profiles {
                /Common/udp { }
        }
        pool pool-dns
}
ltm virtual vs-3 {
        destination ::1:12345
        profiles {
                /Common/tcp { }
        }
        pool pool-unix:/tmp/stream.socket
}
#--------------
WARNING! Pool unix:/tmp/backend3 has a unix socket as pool member
```
