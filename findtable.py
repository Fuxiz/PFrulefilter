import re

# test = 'test2="10.2.0.1"'
# hostname = 'test2'
# regex = rf'(?<={hostname}\=\")\d.{{7}}'
# for match in re.finditer(regex,test):
    # s = match.start()
    # e = match.end()
# # result = re.finditer(regex,test,re.M|re.I )
    # print('string is',test,'start is',s,'end is',e,'and result is',match.group(0))
# print(test)
with open('hosts.txt','r') as hostline:
    for line in hostline:
        hostname = 'test2'
        regex = rf'(?<={hostname}\=\")\d.{{7}}'
        for match in re.finditer(regex,line):
            s = match.start()
            e = match.end()
        # result = re.finditer(regex,test,re.M|re.I )
            print(match.group(0))

print(line)