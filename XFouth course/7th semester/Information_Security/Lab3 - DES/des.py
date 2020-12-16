from config import *
from struct import pack

class DES():
    
    def __init__(self, key):
        if len(key) < 8:
            raise "Key lenght must be 64 bits"
        if len(key) > 8:
            key = key[:8]

        self.key = key
        self.keys = self.generate_16_keys()

    def generate_16_keys(self):
        keys = []
        key = self.to_bit_array(self.key)
        key = self.permut(key, C0_D0) # перестановка
        l, r = self.split_on_blocks(key, 28) # 2 по 28
        for i in range(ROUNDS):
            # сдвиг влево
            l = self.shift(l, SHIFT[i])
            r = self.shift(r, SHIFT[i])
            keys.append(self.permut(l + r, C1_D1)) #  получаем 48 бит
        return keys

    # шифрация / дешифрация строки (размер кратен 8 байт)
    def process_string(self, string, action=ENCRYPT):
        res = b''
        for block in self.split_on_blocks(string, 8):
            res += self.process(block, action)
        return res
  
    # шифрация / дешифрация блока data (64 бита)
    def process(self, data, action=ENCRYPT):
        
        if len(data) != 8: 
            raise "Lenght of data must be 64 bits"
        
        data = self.to_bit_array(data)
        #print(data)
        data = self.permut(data, PI) # начальная перестановка

        # 16 раундов с функцией фейстеля
        l, r = self.split_on_blocks(data, 32)
        t = None
        for i in range(ROUNDS):
            if action == ENCRYPT:
                t = r
                r = self.xor(l, self.funcFeistel(r, self.keys[i]))
                l = t
            else:
                t = l
                l = self.xor(r, self.funcFeistel(l, self.keys[::-1][i]))
                r = t

        # конечная перестановка
        data =  self.permut(l + r, PI_1)

        # переводим в байты
        return self.to_bytestring(data)

    # функция фейстеля: ключ - 48 бит, данные - 32 бита
    def funcFeistel(self, data, key):
        data = self.permut(data, E) # расширяем данные до 48 бит
        data = self.xor(data, key) # xor данных с ключом

        blocks = self.split_on_blocks(data, 6) # делим на 8 блоков по 6

        # получаем по 4 бита из каждого блока с помощью S
        res = []
        for i in range(len(blocks)):
            block = blocks[i]
            row = int(str(block[0]) + str(block[5]), 2)
            column = int(''.join([str(x) for x in block[1:5]]), 2)
            value = S[i][row][column]
            bin_value = self.binvalue(value, 4)
            res += [int(x) for x in bin_value]
        
        return self.permut(res, P) # Перестановка по таблице P

    # перестановка элементов data по таблице table
    def permut(self, data, table):
        return [data[x-1] for x in table]

    # разделение списка data на списки размера size
    def split_on_blocks(self, data, block_size):
        count = int(len(data) / block_size)
        blocks = []
        for i in range(count):
            blocks.append(data[block_size * i : block_size * (i + 1)])
        
        return blocks

    # сдвиг списка data на n влево
    def shift(self, data, n):
        return data[n:] + data[:n]

    # xor двух массивов одинаковой размерности
    def xor(self, arr1, arr2):
        return [x^y for x,y in zip(arr1, arr2)]
        
    def binvalue(self, val, bitsize): 
        binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
        while len(binval) < bitsize:
            binval = '0' + binval
        return binval

    def to_bit_array(self, data):
        array = list()
        for item in data:
            binval = self.binvalue(item, 8)
            array.extend([int(x) for x in list(binval)])
        return array

    # преобразование массива битов в байтовую строку, пригодную для записи в файл
    # размер массива кратен 8
    def to_bytestring(self, data):
        n = int(len(data) / 8)
        res = b''
        for i in range(n):
            arr = data[8 * i: 8 * (i + 1)]
            num = int(''.join([str(x) for x in arr]), 2)
            res += pack('B', num)
        return res

        

