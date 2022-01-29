#!/usr/bin/python3
import re
import sys
import argparse
import os
import ipaddress
from collections import defaultdict


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
            m = re.search(rf'.+\<{tablename}\>\s+persist\s+{{([^}}]*)\}}', hostline.read(),re.MULTILINE | re.DOTALL)
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

    ruledict = defaultdict(list)
    keys_list = ["src","dest","port"]
    sourcelist= []
    destlist= []
    portlist= []
    resolvedsource = [""]
    resolveddest = [""]
    tmptablesrc = [""]
    tmptabledest = [""]
    splitrawrule = line.split()
   # print(line)
    for item in splitrawrule:
        if item == "from":
            sourceindex = splitrawrule.index(item)
            if splitrawrule[sourceindex+1] == '{':
                ruleindex = sourceindex+2
                try:
                    while splitrawrule[ruleindex] != '}':
                        sourcelist.append(splitrawrule[ruleindex])
                        ruleindex += 1
                except IndexError:
                    print(f'Curly bracket is to close to a macro, for example {{ $macro}} \n {line}')
            else:
                sourcelist.append(splitrawrule[sourceindex+1])
        elif item == "to":
            destindex = splitrawrule.index(item)
            if splitrawrule[destindex+1] == '{':
                ruleindex = destindex+2
                try:
                    while splitrawrule[ruleindex] != '}':
                        destlist.append(splitrawrule[ruleindex])
                        ruleindex += 1
                except IndexError:
                    print(f'Curly bracket is to close to a macro, for example {{ $macro}} \n {line}')                
            else:
                destlist.append(splitrawrule[destindex+1])
        
        elif item == "port":
            portindex = splitrawrule.index(item)
            if splitrawrule[portindex+1] == '{':
                ruleindex = portindex+2
                try:
                    while splitrawrule[ruleindex] != '}':
                        portlist.append(splitrawrule[ruleindex])
                        ruleindex += 1
                except IndexError:
                    print(f'Curly bracket is to close to a macro, for example {{ $macro}} \n {line}')
            else:
                portlist.append(splitrawrule[portindex+1])

    for i in sourcelist:
        if i.startswith("$"):
            resolvedsource.append(findhost(i))
        elif i.startswith("<"):
            tmptablesrc.extend(findtable(i))
            for p in tmptablesrc:
                if "/" in p:
                    resolvedsource.append(findipinnetwork(source,p))
        else:
            resolvedsource.extend(i)

    for i in destlist:
        if i.startswith("$"):
            tmphostdest = findhost(i)
            if "/" in tmphostdest:
                resolveddest.append(findipinnetwork(destination,tmphostdest))
        elif i.startswith("<"):
            tmptabledest = findtable(i)
            for p in tmptabledest:
                if "/" in p:
                     resolveddest.extend(findipinnetwork(destination,p))
                else:
                    resolveddest.append(p)
        else:
            resolveddest.append(i)

    if source in resolvedsource and destination in resolveddest:
        print(f'result: {line}')

def main():
    for anchorfiles in os.listdir(f"/home/filipst/git/firewalls/roles/pf/files/pf/{firewallfiles}/firewall/anchors"):
        with open(f"/home/filipst/git/firewalls/roles/pf/files/pf/{firewallfiles}/firewall/anchors/{anchorfiles}",'r') as hostline:
            for line in hostline:
                if line.startswith("pass"):
                    #print(line)
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
