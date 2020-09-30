import re 

syntaxlist = [['pass','block'],['in','out'],['log'],['quick'],['egress','vmx0'],['inet','inet6'],['tcp','udp','icmp','icmp6','http','https'],['from'],['to'],['port'],['flags S/SA'],['no state','keep state','modulate state','synproxy state']]
macrohost = ""
islist = False
filteredRules = []
with open('pfrule.txt','r') as f:
    for line in f:
        result = re.search(r"(?<=$)\w+",line)
        print('result it',result.group(0))
        rules = line.split()
        rulelen = len(rules)
        for s in range(rulelen):
            if rules[s] == '{':
                islist = True
            elif rules[s] == '}':
                islist = False
                print(macrohost.strip('{'))
                s += 1
                macrohost = ''
            if islist == True:
                macrohost += rules[s]
                macrohost += ' '
            else:
                for rulecount in range(len(syntaxlist)):   
                        print(rules[s])
                        rulecount += 1
                        break
                        for listitem in range(len(syntaxlist[rulecount])):
                                if rules[s] == syntaxlist[rulecount][listitem]:
                                   print(rules[s])
        print("\n")
