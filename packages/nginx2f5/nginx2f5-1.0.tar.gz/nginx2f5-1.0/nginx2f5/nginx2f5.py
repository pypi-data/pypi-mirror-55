#!/usr/bin/env python
# This is a script to take nginx configuration and translate it into F5 syntax
# Config guide taken from https://docs.nginx.com/nginx/admin-guide/
# v1.0 PW 20/2/2019

import sys
import re
warnings = []

print "# -- Running with Python v" + sys.version

debug = False

# Check there is an argument given
if not len(sys.argv) > 1:
    exit("Usage: nginx2f5 <filename> [partition]")
if len(sys.argv) == 3:
    # Second command-line variable is the partition
    partition = "/" + sys.argv[2] + "/"
    print ("Using partition " + partition)
else:
    partition = "/Common/"
    
# Check input file
try:
    fh = open(sys.argv[1],"r")
except IOError: 
    exit("Fatal ERROR! Cannot open file " + sys.argv[1])

def getsection (config,sectionName,bracket = True):
    # This is a function to retrieve a single section of config startng with text { and
    # ending with } but there may be opened and closed parentheses in between
    # eg http {
    #   newsection {
    #   }
    # }
    # Input: 
    # config is a blob of text ( such as shown above )
    # sectionName is the name of the section without bracket eg 'backend server'

    r = []
    index = -1
    cnt = 0
    o = False
    if bracket:
        sectionName += ' {'
    for line in config.split("\n"):
        if sectionName in line:
            o = True
            cnt += 1
            r.append("")
            index += 1
        else:
            if '{' in line:
                cnt += 1
            if '}' in line:
                cnt -= 1
            if cnt < 1:
                o = False
            if o:
                r[index] += line.strip() + "\n"

    if len(r) > 0:
        return r
    else:
        return False

def getsubstr(string,part):
    # This function will take a space-separated string and return a part of it
    # eg first second third fourth. part of 0 will return 'first'
    strArray = string.split(' ')
    if len(strArray) > part:
        return strArray[part].rstrip(';')
    else:
        return False
def getvalue(string):
    # This function takes a string of format index=value and returns the value
    strArray = string.split('=')
    if len(strArray) > 1:
        return strArray[1]
    else:
        return False

def parse_vs(vsConfig):
    global warnings
    # This function retrieves the virtual server config and outputs it into a dictionary
    # input would be the section from a server block eg server = getsection(http,'server')

    output = {"destination": [],"profiles":[]}
    for line in vsConfig.split("\n"):
        #Manage Destinations
        if line.startswith('listen'):
            # Listen could be 'listen <IPv4 or IPv6>:<port> <udp>|<ssl> All entities are optional
            if ' udp' in line:
                # This is a UDP protocol
                output['profiles'].append("/Common/udp { }")
                output['protocol'] = 'udp'
            else:
                output['profiles'].append("/Common/tcp { }")
                output['protocol'] = 'tcp'
            if ' ssl' in line:
                # This is SSL protocol
                output['profiles'].append("/Common/clientssl { }")
            # Manage destination by looking for listen 
            # https://nginx.org/en/docs/http/ngx_http_core_module.html#listen
            if '[' in line:
                # Contains an IPv6 address inside the brackets eg [fe80::abcd]:8080
                m = re.search(r'\[(.+?)\]:(.+)[ ;]',line)
                if m:
                    output['destination'].append(m.group(1) + ":" + m.group(2))
                else:
                    warnings.append('WARNING! Line ' + line + ' contains an IPv6 address but it can\'t be translated.' )
            elif ':' in line:
                # The line contains an IP address
                output['destination'].append(getsubstr(line,1))
            else:
                # There is no IP address, grab the port
                output['destination'].append("0.0.0.0:" + getsubstr(line,1))
        # Manage pools
        if line.startswith('proxy_pass'):
            output['pool'] = getsubstr(line,1)
        # Monitor
        if line.startswith('health_check'):
            output['monitor'] = getsubstr(line,1)
    return output

def parse_pool (poolConfig):
    # This is a function to take a pool stanza eg upstream example and return a dict of the features
    output = {"members": [], "load-balancing-mode": "round-robin", "persistence": "source_addr", "monitor": "/Common/http", "ratio":[],"backup":[],"disabled":[] }
    for line in poolConfig.split("\n"):
        if line.startswith('server '):
            # This is a pool member
            poolMemberName = getsubstr(line,1)
            if not poolMemberName in output["members"]:
                output["members"].append(poolMemberName)
                port = poolMemberName.split(':')[1]
                # Set the monitor based on the port
                if port == '80':
                    output['monitor'] = "/Common/http"
                elif port == '443':
                    output['monitor'] = "/Common/https"
                elif port == '53':
                    output['monitor'] = "/Common/udp"
                else:
                    output['monitor'] = "/Common/tcp"
            # Manage second parameter
            if getsubstr(line,2):
                # Server weight
                if getsubstr(line,2).startswith('weight'):
                    output["ratio"].append(poolMemberName + ":" + getvalue(getsubstr(line,2)))
                # Backup
                if getsubstr(line,2).startswith('backup'):
                    output["backup"].append(poolMemberName)
                # Disabled
                if getsubstr(line,2).startswith('down'):
                    output["disabled"].append(poolMemberName)
        # LB mode
        if line.startswith('least_conn'):
            output["load-balancing-mode"] = "least-connections-member"
        
    return output
        
# Read in the config file as nginxConfig variable
nginxConfig = fh.read()
    
# Create pools
f5PoolsConfig = {}
f5VsConfig = []
f5SslConfig = {}

# Retrieve stream configuration
stream = getsection(nginxConfig,'stream')[0]
servers = getsection(stream,'server')
    
# Output pools
for pools in re.finditer(r'upstream (\S+) \{',stream):
    poolName = pools.group(1)
    f5PoolsConfig[poolName] = parse_pool(getsection(stream,"upstream " + poolName)[0] )
    
print "#--- Pools ---"
for pool in f5PoolsConfig:
    print "ltm pool pool-" + pool + " {"
    print "\tmonitor " + f5PoolsConfig[pool]['monitor']
    print "\tload-balancing-mode " + f5PoolsConfig[pool]['load-balancing-mode']
    if len(f5PoolsConfig[pool]):
        if len(f5PoolsConfig[pool]['backup']):
            priority = ' priority 3 '
            print "\tmin-active-members 1"
        else:
            priority = ''
            print "\tmembers {"
        for m in f5PoolsConfig[pool]['members']:
            if m.startswith('unix:'):
                warnings.append('WARNING! Pool ' + m + ' has a unix socket as pool member')
                continue
            s = ""
            if m in f5PoolsConfig[pool]['disabled']:
                s += "\n\t\tstate user-disabled"
            if m in f5PoolsConfig[pool]['backup']:
                s += "\n\t\t priority 1"
            print "\t\t" + m + " { " + s + "\n\t\t}"    
        print "\t}"
    print "}"
        
print "#--- /Pools ---"
    
# Output VSs
for vs in servers:
    f5VsConfig.append(parse_vs(vs))
    
vsid = 1
print "#--- VS ---"
for vs in f5VsConfig:
    for v in vs['destination']:
        print "ltm virtual vs-" + str(vsid) + " {"
        print "\tdestination " + v
        # Profiles
        if 'profiles' in vs:
            print "\tprofiles {"
            for profile in vs['profiles']:
                print "\t\t" + profile
            print "\t}"
        # Pool
        if 'pool' in vs:
            print "\tpool pool-" + vs['pool']
        print "}"
        vsid += 1
print "#--------------"
 

for w in warnings:
    print w
