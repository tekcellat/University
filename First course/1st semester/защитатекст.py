#защита текста
# Массив строк в которой есть предложения 2+. Надо найти самое короткое и самое
# длинное предложение и найти одинаковые в них слова.

txt =['dtom dtom dtom.']




for i in txt:
    print(i)

raznie_znaki = {',','—',';',')','(','—','+','\\','/'}
konec_predlozh = {'!','?','.'}
cifri = {'0','1','2','3','4','5','6','7','8','9'}
ne_bukvi = konec_predlozh.union(raznie_znaki,cifri)
ne_bukvi_i_mnozh = konec_predlozh.union(raznie_znaki,cifri,{' '})
ne_bukvi_c_ciframi = konec_predlozh.union(raznie_znaki)

#print(txt)
#Преобразуем исходный массив строк в единный текст
def v_odin_txt(massive):
    new_txt = ''
    for string in massive:
        new_txt += string + ' '
    return new_txt

