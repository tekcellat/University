text=['Он. ','её любил. Она съела кусок мяса. Он её',
      'убил. И в землю закопал.']
minlen=len(text[0].split(' '))
maxword='В тексте нет слов'
word=''
maxwordlen=0
wordcount=0
mincount=len(text[0])
locmaxwordlen=0
for i in range(len(text)):
    wordcount+=1
    if len(word)>locmaxwordlen:
        locmaxword=word
        locmaxwordlen=len(word)
    word=''
    print(text[i])
    for j in range(len(text[i])):
        lord=ord(text[i][j].lower())
        if lord>=ord('а') and lord<=ord('я') or lord==ord('ё'):
            word+=text[i][j]
        elif text[i][j]==' ':
            wordcount+=1
            if len(word)>locmaxwordlen:
                locmaxword=word
                locmaxwordlen=len(word)
            word=''
        elif text[i][j]=='.':
            if len(word)>locmaxwordlen:
                    locmaxword=word
                    locmaxwordlen=len(word)
            if wordcount<mincount or (wordcount==mincount
                                      and len(locmaxword)>maxwordlen):
                mincount=wordcount
                maxword=locmaxword
                maxwordlen=len(locmaxword)
            word=locmaxword=''
            locmaxwordlen=0
            wordcount=0   
print('\n',end=maxword)
