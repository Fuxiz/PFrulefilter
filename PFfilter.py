import re 
from collections import defaultdict

ruledict = defaultdict(list)
#                action         dicrection    log     quick       interface       af                   protocol                               from_src  rule   to_dest   port     flags           state
syntaxlist = [['pass','block'],['in','out'],['log'],['quick'],['egress','vmx0'],['inet','inet6'],['tcp','udp','icmp','icmp6','http','https'],['from'],["{","}"],['to'],['port'],['flags S/SA'],['no state','keep state','modulate state','synproxy state']]
keys_list = ["src","dest","port"]
itemindex = 0
with open('pfrule.txt','r') as f:
    for line in f:
        splitrawrule = line.split()
        for item in splitrawrule:
            if item == "from":
                sourceindex = splitrawrule.index(item)
                if splitrawrule[sourceindex+1] == '{':
                    ruleindex = sourceindex+2
                    while splitrawrule[ruleindex] != '}':
                        ruledict[keys_list[keys_list.index("src")]].append(splitrawrule[ruleindex])
                        ruleindex += 1
            elif item == "to":
                destindex = splitrawrule.index(item)
                if splitrawrule[destindex+1] == '{':
                    ruleindex = destindex+2
                    while splitrawrule[ruleindex] != '}':
                        ruledict[keys_list[keys_list.index("dest")]].append(splitrawrule[ruleindex])
                        ruleindex += 1
                else:
                    ruledict[keys_list[keys_list.index("dest")]].append(splitrawrule[destindex+1])

            elif item == "port":
                portindex = splitrawrule.index(item)
                if splitrawrule[portindex+1] == '{':
                    ruleindex = portindex+2
                    while splitrawrule[ruleindex] != '}':
                        ruledict[keys_list[keys_list.index("port")]].append(splitrawrule[ruleindex])
                        ruleindex += 1
                else:
                    ruledict[keys_list[keys_list.index("port")]].append(splitrawrule[portindex+1])
        print(ruledict)
        ruledict.clear()


    #        for row in syntaxlist:
     #           for elem in row:
      #              if elem == item:
       #                 ruledict[keys_list[syntaxlist.index(row)]].append(elem)
        #                print(ruledict