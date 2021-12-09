#!/usr/bin/python3
import re
import sys
import argparse

matchhostlist = []
matchtablelist = []

parser = argparse.ArgumentParser()
parser.add_argument('files', type=str,default="-r",metavar=('host file', 'tables'),nargs=2)
parser.add_argument("-s", "--source", default="-r", help="Source address")
parser.add_argument("-d", "--destination", default="-r",help="destination address")
parser.add_argument("-r", "--resolve",default="-r",action="store_false",help="resolve all rules")

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
        hostlist = []
        hostlistraw = re.findall(r'\$[\S]+',line)
        for i in hostlistraw:
            host = findhost(i)
            if source == host:
                print('found it') 



def main():
    with open('pfrule.txt','r') as hostline:

        if args.source is not False:
            foundrule = findhostrule(hostline,args.source,args.destination)
            print(foundrule)
        else: 
            for line in hostline:
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
