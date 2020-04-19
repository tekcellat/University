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
text = code_to_search.split("\n")

k = 0
for i in range(len(text)):
    if 'acos('  in text[i]:
        k += 1
    elif 'asin(' in text[i]:
        k += 1
    elif 'sin(' in text[i]:
        k += 1
    elif 'cos(' in text[i]:
        k += 1
    elif 'tan(' in text[i]:
        k += 1
    elif 'atan(' in text[i]:
        k += 1
    elif 'abs(' in text[i]:
        k += 1
    elif 'sqrt(' in text[i]:
        k += 1


print('Count', k)
stop = perf_counter()
time = stop - start
print("Elapsed time:", stop-start)

f= open("time.txt","a+")
f.write("Time with at %f\n" % time)
f.close()
