from time import perf_counter
#from memory_profiler import profile

def levensteinRec(str1, str2):
    size1 = len(str1)
    if (size1 == 0):
        return len(str2)

    size2 = len(str2)
    if (size2 == 0):
        return size1

    symbIdent = 0
    if (str1[0] != str2[0]):
        symbIdent = 1

    return min((levensteinRec(str1[1:], str2) + 1),
               (levensteinRec(str1, str2[1:]) + 1),
               (levensteinRec(str1[1:], str2[1:]) + symbIdent))

def levens(word1, word2):
    size1, size2 = len(word1), len(word2)
    if size1 > size2:
        word1, word2 = word2, word1
        size1, size2 = size2, size1

    current_row = range(size1 + 1) 
    for i in range(1, size2 + 1):
        previous_row, current_row = current_row, [i] + [0] * size1
        for j in range(1, size1 + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if word1[j - 1] != word2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[size1]
    

def lev_modified(str1, str2):
    size1, size2 = len(str1), len(str2)
    if (size1 < 2 or size2 < 2):
        return levens(str1, str2)

    if size1 > size2:
        str1, str2 = str2, str1
        size1, size2 = size2, size1
        
    prev_row = range(size1 + 1)
    curr_row = [1] + [0] * size1
    for i in range(1, size1 + 1):
        add, delete, change = prev_row[i] + 1, curr_row[i - 1] + 1, prev_row[i - 1]
        if str1[i - 1] != str2[0]:
            change += 1
        curr_row[i] = min(add, delete, change)

    for i in range(2, size2 + 1):
        prev_prev_row = prev_row; prev_row = curr_row; curr_row = [i] + [0] * size1
        add, delete, change = prev_row[1] + 1, curr_row[0] + 1, prev_row[0]
        if (str1[0] != str2[i - 1]):
            change += 1
        curr_row[1] = min(add, delete, change)

        for j in range(2, size1 + 1):
            add, delete, change = prev_row[j] + 1, curr_row[j - 1] + 1, prev_row[j - 1]                                         
            if (str1[j - 1] != str2[i - 1]):
                change += 1
            if (str2[i - 1] == str1[j - 2] and str2[i - 2] == str1[j - 1]):
                transp = prev_prev_row[j - 2] + 1 
                curr_row[j] = min(add, delete, change, transp)
            else:
                curr_row[j] = min(add, delete, change)

    return curr_row[size1]
    pass



def printResult(str1, str2, countOperations):
    print("Result algorithm Levenstein")
    print("With 2 words [" + str1 + ", " + str2 + "]")

    print("\nCount operations:")
    getAnswer(str1, str2)

    print("\nWork Time:")
    getWorkTime(str1, str2, countOperations)

        
def getAnswer(str1, str2):
    print("Recursion        : ", levensteinRec(str1, str2))
    print("Levenstein: ", levens(str1, str2))
    print("Modified: ", lev_modified(str1, str2))


def getWorkTime(str1, str2, countOperations):
    t1_start = perf_counter()
    for i in range(countOperations):
        levensteinRec(str1, str2)
        
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop-t1_start) 
    t2_start = perf_counter()
    for i in range(countOperations):
        levens(str1, str2)
    t2_stop = perf_counter()
    print("Elapsed time:", t2_stop-t2_start) 

    t3_start = perf_counter()
    for i in range(countOperations):
        lev_modified(str1, str2)
    t3_stop = perf_counter()
    print("Elapsed time:", t3_stop-t3_start) 


#@profile
def main():
    countOperations = 100
    str1 = input("str1 = ")
    str2 = input("str2 = ")
    printResult(str1, str2, countOperations)
       
if __name__ == "__main__":
    main()
