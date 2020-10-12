import re 

def main():
    syntaxlist = [['pass','block'],['in','out'],['log'],['quick'],['egress','vmx0'],['inet','inet6'],['tcp','udp','icmp','icmp6','http','https'],['from'],['to'],['port'],['flags S/SA'],['no state','keep state','modulate state','synproxy state']]
    macrohost = ""
    islist = False
    filteredRules = []
    with open('pfrule.txt','r') as f:
        for line in f:
            # result = re.search(r"(?<=$)\w+",line)
            # print('result it',result.group(0))
            rules = line.split()
            rulelen = len(rules)
            for s in range(rulelen):
                if rules[s] == '{':
                    islist = True
                    continue
                elif rules[s] == '}':
                    islist = False
                    s += 1
                    macrohost = ''
                elif re.search('\$.+', rules[s]):
                    print(findhost(rules[s].strip('$')))
                    continue 
                if islist == True:
                    if re.search('\$.+', rules[s]) is None:
                        print(rules[s])
                        continue 
                    onehost = findhost(rules[s])
                    macrohost += onehost
                    macrohost += ' '
                else:
                    for rulecount in range(len(syntaxlist)):   
                            print(rules[s])
                            rulecount += 1
                            break
                            for listitem in range(len(syntaxlist[rulecount])):
                                    if rules[s] == syntaxlist[rulecount][listitem]:
                                       print(rules[s])
            print(",")

def findhost(hostname):
    with open('hosts.txt','r') as hostline:
        for line in hostline:
            # hostname = 'test2'
            result = 'none'
            regex = rf'(?<={hostname}\=\")\d.{{7}}'
            for match in re.finditer(regex,line):
                result = match.group(0)
                return(result)            
    return(result)
main()
