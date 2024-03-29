#!/usr/bin/python3
import re
import sys


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
        return(str(hostlist))


def main():
    with open('pfrule.txt','r') as hostline:

        tablename = 'table2'
        regexfilter2 = rf'(?<={tablename})'
        for line in hostline:
            try:
                matchhost = re.sub(r'\$[\w\d]+',findhost,line)
                line = matchhost
            except AttributeError:
                print("no host found")
            try:
                matchtable = re.sub(r'\<\S+\>',findtable,line)
                print(matchtable)
            except AttributeError:
                print(line)
 
main()
