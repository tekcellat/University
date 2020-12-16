import sys
from config import MAX_LEN, DECRYPT
from des import DES
from random import randint


def check_8byte(string):
    d = len(string) % 8
    if d:
        d = 8 - d
    return d


def main():
    try:
        file = open(sys.argv[1], "rb")
    except IndexError:
        print("Set file as argv[1]")
        return

    enc_file_name = "enc_" + sys.argv[1] 
    dec_file_name = "dec_" + sys.argv[1] 
    enc_file = open(enc_file_name, "wb")

    count = 0
    append_bytes = 0
    d = DES([randint(0, 255) for _ in range(8)])

    print("Start encrypting '{0}' ...".format(sys.argv[1]))
    while True:
        buf = file.read(MAX_LEN)
        if(not len(buf)):
            file.close()
            enc_file.close()
            print("Encrypting done. Results saved in file: '{0}'".format(enc_file_name))
            break
        else:
            count += 1
            append_bytes = check_8byte(buf)
            if append_bytes:
                buf += b'0' * append_bytes
            enc_str = d.process_string(buf)
            enc_file.write(enc_str) 

    enc_file = open(enc_file_name, "rb")    
    dec_file = open(dec_file_name, "wb")
    
    print("Start decrypting '{0}' ...".format(enc_file_name))
    while True:
        buf = enc_file.read(MAX_LEN)
        if(not len(buf)):
            enc_file.close()
            dec_file.close()
            print("Decrypting done. Results saved in file: '{0}'".format(dec_file_name))
            break
        else:
            count -= 1
            dec_str = d.process_string(buf, DECRYPT)
            if not count and append_bytes:
                dec_str = dec_str[:-append_bytes]
            dec_file.write(dec_str)

if __name__ == "__main__":
    main()