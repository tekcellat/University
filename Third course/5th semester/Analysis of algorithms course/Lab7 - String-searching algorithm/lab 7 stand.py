from time import perf_counter
#Naive Pattern Searching algorithm 
def search(pat, txt): 
    M = len(pat) 
    N = len(txt) 
 
    for i in range (N-M+1 ): 
        j = 0 
         
        while (j < M): 
            if (txt[i+j] != pat[j]): 
                break 
            j+=1 
 
        if (j == M): 
            print ( "Pattern found at index " , i) 
    print("End of search")

if __name__ == '__main__' : 
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
    Trishank
    abs[()] '''
    pat = input("Word please: ")
    start = perf_counter()
    search(pat, txt)
    stop = perf_counter()
    time = stop - start
    print("Elapsed time:", time)
    f= open("time.txt","a+")
    f.write("Time with Standart %f\n" % time)
    f.close()
 
