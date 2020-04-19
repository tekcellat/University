def mysort_bubble(arr):
    n = len(arr)

    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                buf = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = buf
    
    return arr
    
def mysort_insert(arr):
    n = len(arr)

    for i in range(1, n, 1):
        value = arr[i]
        temp = i
        
        while temp > 0 and arr[temp - 1] > value:
                arr[temp] = arr[temp - 1]
                temp -= 1
                
        arr[temp] = value
    
    return arr

def mysort_quick_rec_end(arr, begin, end):
    if begin < end:
        i = begin - 1
        base = arr[end]

        for j in range(begin, end + 1):
            if arr[j] <= base:
                i += 1
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp

        mysort_quick_rec_end(arr, begin, i - 1)
        mysort_quick_rec_end(arr, i + 1, end)

    return arr

def mysort_quick_rec_middle(arr, begin, end):
    if begin < end:
        i = begin - 1
        ibase = (end + begin) // 2
        base = arr[ibase]

        for j in range(begin, ibase):
            if arr[j] <= base:
                i += 1
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp

        for j in range(ibase + 1, end + 1):
            if arr[j] <= base:
                i += 1
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp

        if i < ibase:
            i += 1
            temp = arr[i]
            arr[i] = arr[ibase]
            arr[ibase] = temp        
            mysort_quick_rec_middle(arr, begin, i - 1)
            mysort_quick_rec_middle(arr, i + 1, end)
        else:
            mysort_quick_rec_middle(arr, begin, i)
            mysort_quick_rec_middle(arr, i + 1, end)

    return arr

def mysort_quick_middle(arr):
    return mysort_quick_rec_middle(arr, 0, len(arr) - 1)

def mysort_quick_end(arr):
    return mysort_quick_rec_end(arr, 0, len(arr) - 1)
    
