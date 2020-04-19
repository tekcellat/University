from time import perf_counter

NO_OF_CHARS = 256
  
def badCharHeuristic(string, size): 
    badChar = [-1]*NO_OF_CHARS 
    for i in range(size): 
        badChar[ord(string[i])] = i; 
    return badChar 
  
def search(txt, pat): 
    ''' 
    A pattern searching function that uses Bad Character 
    Heuristic of Boyer Moore Algorithm 
    '''
    m = len(pat) 
    n = len(txt) 
    badChar = badCharHeuristic(pat, m)  
    s = 0
    while(s <= n-m): 
        j = m-1

        while j>=0 and pat[j] == txt[s+j]: 
            j -= 1
        if j<0: 
            print("Pattern occur at shift = {}".format(s)) 
            s += (m-badChar[ord(txt[s+m])] if s+m<n else 1)
        else:
            s += max(1, j-badChar[ord(txt[s+j])]) 
    print("End of search")
# Driver program to test above function 
def main(): 
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
    pat = input("Which word you wanna: ")
    start = perf_counter()
    search(txt, pat)
    stop = perf_counter()
    time = stop - start
    print("Elapsed time:", time)
    f= open("time.txt","a+")
    f.write("Time with Boyer %f\n" % time)
    f.close()

if __name__ == '__main__':
    main()
    
