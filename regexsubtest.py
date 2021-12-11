#!/usr/bin/python3
import re
import sys
import argparse
import os
import ipaddress

matchhostlist = []
matchtablelist = []

parser = argparse.ArgumentParser()
parser.add_argument('firewall', type=str,default="False",help="Specify the firewall to resolve from",metavar=('anchor'),nargs=1)
parser.add_argument("-s", "--source", default="False", help="Source address")
parser.add_argument("-d", "--destination", default="False",help="destination address")
parser.add_argument("-r", "--resolve",default="False",action="store_false",help="resolve all rules")

args = parser.parse_args()
firewallfiles = args.firewall[0]

def findhost(hostname):
    for hostfiles in os.listdir(f"/home/filipst/git/firewalls/roles/pf/files/pf/{firewallfiles}/firewall/macros"):
        with open(f"/home/filipst/git/firewalls/roles/pf/files/pf/{firewallfiles}/firewall/macros/{hostfiles}",'r') as hostline:
            if type(hostname) == str:
                hostname = hostname.strip("$()")
            else:
                hostname = hostname.group().strip("$()")
            result = 'none'
            try:
                result = re.search(rf'(?<={hostname}\=\").+', hostline.read())
                result = result.group().strip('"')
                return(str(result))
            except AttributeError:
                continue
    return(hostname)

def findtable(tablename):
    tablename = tablename.strip("<>()")
    hostlist = []
    with open(f"/home/filipst/git/firewalls/roles/pf/files/pf/{firewallfiles}/firewall/tables",'r') as hostline:
        try:
            m = re.search(rf'.+\<{tablename}\>.+', hostline.read())
            temp = str(m.group())
     
        except AttributeError:
            #print(tablename,"error")         
            return("table not found")
        m2 = re.findall(r'\$[\w\d]+',temp)
        for i in m2:
            host = findhost(i)
            hostlist.append(host)
        return(hostlist)

def findipinnetwork(ip,network):
    try: 
        if ipaddress.ip_address(ip) in ipaddress.ip_network(network):
            return(ip)
        else:
            return(network)
    except ValueError:
        return(network)


def findhostrule(line,source,destination):
    sourcelistraw = []
    destlistraw = []
    resolvedsource = [""]
    resolveddest = [""]
    sourcelistraw = re.findall(r'(?<=from).+(?=to)',line)
    try:
        sourcelistclean = sourcelistraw[0].split()
    except IndexError:
        return
    destlistraw = re.findall(r'(?<= to ).+(?=keep|no|port)',line)
    destlistclean = destlistraw[0].split()
    for i in sourcelistclean:
        if i.startswith("<"):
            sourcetablelist = findtable(i)
            resolvedsource.extend(sourcetablelist)
        else:
            sourcehost = findhost(i)
            if "/" in sourcehost:
                resolvedsource.append(findipinnetwork(source,sourcehost))
            else:
                resolvedsource.append(sourcehost)
    for p in destlistclean:
        if p.startswith("<"):
            desttablelist = findtable(p)
            resolveddest.extend(desttablelist)
        else:        
            desthost = findhost(p)
            if "/" in desthost:
                resolveddest.append(findipinnetwork(destination,desthost))
            else:
                resolveddest.append(desthost)
    
    if source in resolvedsource and destination in resolveddest:
        print(line)

def main():
    for anchorfiles in os.listdir(f"/home/filipst/git/firewalls/roles/pf/files/pf/{firewallfiles}/firewall/anchors"):
        with open(f"/home/filipst/git/firewalls/roles/pf/files/pf/{firewallfiles}/firewall/anchors/{anchorfiles}",'r') as hostline:
            for line in hostline:
                if line.startswith("pass"):
                    if args.source is not "False":
                        findhostrule(line,str(args.source).strip(" "),str(args.destination).strip(" "))
                    else: 
                        try:
                            matchhost = re.sub(r'\$[\S]+',findhost,line)
                            line = matchhost
                        except AttributeError:
                            print("no host found")
                        try:
                            matchtable = re.sub(r'\<\S+\>',findtable,line)
                            print(matchtable)
                        except AttributeError:
                            print(line)
                else:
                    continue
 
main()
