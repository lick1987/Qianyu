import re
s2='asdfads.f.png'
s1=re.sub(r'[\s\S]*\.','3.',s2)
print(s1)