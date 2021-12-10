#!/usr/bin/python3
import re
import sys
import argparse

matchhostlist = []
matchtablelist = []

parser = argparse.ArgumentParser()
parser.add_argument('anchor', type=str,default="False",help="anchor to resolve from",metavar=('anchor'),nargs=1)
parser.add_argument("-s", "--source", default="False", help="Source address")
parser.add_argument("-d", "--destination", default="False",help="destination address")
parser.add_argument("-r", "--resolve",default="False",action="store_false",help="resolve all rules")

args = parser.parse_args()

def findhost(hostname):
    hostfile = sys.argv[1]
    with open(hostfile,'r') as hostline:
        if type(hostname) == str:
            hostname = hostname.strip("$")
        else:
            hostname = hostname.group().strip("$")
        result = 'none'
        regex = rf'(?<={hostname}\=\").+'
        try:
            result = re.search(regex,hostline.read())
            result = result.group().strip('"')
            return(str(result))
        except AttributeError:
            return(hostname)

def findtable(tablename):
    tablename = tablename.group().strip("<>")
    hostlist = []
    tablesfile = sys.argv[2] 
    with open(tablesfile,'r') as hostline:
        try:
            m = re.search(rf'.+\<{tablename}\>.+', hostline.read())
            temp = str(m.group())
        except AttributeError:
            print(tablename,"error")         
            return("table not found")
        m2 = re.findall(r'\$[\w\d]+',temp)
        for i in m2:
            host = findhost(i)
            hostlist.append(host)
        matchtablelist = hostlist.copy()
        return(str(hostlist))

def findhostrule(line,source,destination):
    sourcelistraw = []
    destlistraw = []
    resolvedsource = []
    resloveddest = []
    sourcelistraw = re.findall(r'(?<=from).+(?= to)',line)
    sourcelistclean = sourcelistraw[0].split()
    destlistraw = re.findall(r'(?<= to ).+(?= port)',line)
    destlistclean = destlistraw[0].split()
    for i in sourcelistclean:
        if i.startswith("<"):
            sourcetablelist = findtable(i).split
            resolvedsource.extend(sourcetablelist)
        else:
            sourcehost = findhost(i)
            resolvedsource.append(sourcehost)
    for p in destlistclean:
        if i.startswith("<"):
            desttablelist = findtable(i).split
            resolvedsource.extend(desttablelist)
        else:        
            desthost = findhost(p)
            resloveddest.append(desthost)
    if source in resolvedsource and destination in resloveddest:
        print(line)


def main():
    with open('pfrule.txt','r') as hostline:

        for line in hostline:
            if args.source is not "False":
                findhostrule(line,args.source,args.destination)
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
            
            
            
            
 
main()
