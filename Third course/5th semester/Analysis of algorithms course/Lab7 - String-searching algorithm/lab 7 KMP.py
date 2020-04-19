from time import perf_counter

def KMPSearch(pat, txt): 
    M = len(pat) 
    N = len(txt) 
  
    lps = [0]*M 
    j = 0 # index for pat[] 
    computeLPSArray(pat, M, lps) 
    i = 0 # index for txt[] 
    while i < N: 
        if pat[j] == txt[i]: 
            i += 1
            j += 1
  
        if j == M: 
            print("Found pattern at index " + str(i-j) )
            j = lps[j-1] 
  
        elif i < N and pat[j] != txt[i]:  
            if j != 0: 
                j = lps[j-1] 
            else: 
                i += 1

    print("End of search")
  
def computeLPSArray(pat, M, lps): 
    len = 0   
    lps[0] 
    i = 1

    while i < M: 
        if pat[i]== pat[len]: 
            len += 1
            lps[i] = len
            i += 1
        else: 
            if len != 0: 
                len = lps[len-1] 
            else: 
                lps[i] = 0
                i += 1
  
txt = '''
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
abs[()] '''

pat = input("Just kill me please: ")

start = perf_counter()
KMPSearch(pat, txt)
stop = perf_counter()

time = stop - start
print("Elapsed time:", time)
f= open("time.txt","a+")
f.write("Time with KMP %f\n" % time)
f.close()

