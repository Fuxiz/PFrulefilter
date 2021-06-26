import re
with open('table','r') as hostline:
    tablename = 'table2'
    regexfilter2 = rf'(?<={tablename})'
    
    try:
        m = re.search(rf'.+\<{tablename}\>.+', hostline.read())
        temp = str(m.group())
        print(temp)
    except AttributeError:
        print(tablename)         
    try:
        m2 = re.findall(r'\$[\w\d]+',temp)
        print(m2)
    except AttributeError:
        print("host not found")
        #regex = rf'(?<=\<{tablename}\=\")\d.{{7}}'
        #for match in re.finditer(regex,line):
        #    s = match.start()
        #    e = match.end()
        

    
