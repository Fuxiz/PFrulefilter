import re

test = 'test2="10.2.0.1"'
hostname = 'test2'
regex = rf'\(?<=%hostname\=\")\d.{7}'
result = re.sub(regex, "worked", test)
print(result)