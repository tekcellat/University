import re
from time import perf_counter

code_to_search = '''
from math import sin
sin(m)+
sin
asin(db)+
acos(rnrf)+
tan()+
prosto stroka tang()
just string but in english sqrt(1)+
sadece bir xett cos()+
cos
sqrt()+
sqrt
abs!
abs()+
abs)
abs[()]
'''



start = perf_counter()
pattern = re.compile(r'[asin|acos|sin|cos|sqrt|abs|tan|sqr]+\(')
matches = pattern.finditer(code_to_search)
count = 0

for match in matches:
    count+=1

print('Count',count)
stop = perf_counter()
time = stop - start
print("Elapsed time:", time)

f= open("time.txt","a+")
f.write("Time with re %f\n" % time)
f.close()

