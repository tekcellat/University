abc=['а','е','ё','и','о','у','ы','э','ю','я']
text=['Пусть мама','услышит, пусть','мама придет;',
'Съешь же ещё этих','мягких французских булок','да выпей чаю;',
      'А эти','предложения созданы','просто чтобы быть.']
for i in text:
    print(i)
print()
for i in range(len(text)):
    wordlist=[]
    arr=[]
    c=0
    cmax=0
    word=''
    for j in text[i]:
        k=0
        while k<len(arr) and arr[k]<c:
            k+=1
        wordlist.insert(k,word)
        k=0
        f=True
        word+=j
        while f and k<10:
            if abc[k]==j.lower():
                c+=1
                f=False
            k+=1
        if f:
            jnum=ord(j.lower())
            if not (jnum>=ord('а') and jnum<=ord('я')
            or j=='ё'):
                k=0
                while k<len(arr) and arr[k]<c:
                    k+=1
                wordlist.insert(k,word)
                arr.insert(k,c)
                word=''
                c=0
    text[i]=''
    for j in wordlist:
        text[i]+=j+' '
for i in text:
    print(i)
