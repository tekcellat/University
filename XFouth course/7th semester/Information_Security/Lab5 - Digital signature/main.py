import rsa
import sys
import os
from Crypto.Hash import SHA256


def hash_file(message_file):
    h = SHA256.new()
    with open(message_file, "rb") as f:
        while True:
            buf = f.read(1024)
            if len(buf) == 0:
                break
            h.update(buf)

    return h.digest()  # hash like array baytov


def make_signature(message_file, key):

    h = hash_file(message_file)

    # crypto hash with closed keys
    signature = rsa.encrypt(h, key)

    # digital signa in file
    signature_file_name = input("signature filename:")
    with open(signature_file_name, "wb") as f:
        f.write(signature)

    print("Signature saved in file '{0}'".format(signature_file_name))

    return signature_file_name

# check


def check_signature(message_file, signature_file, key):
    # read hash file
    h1 = hash_file(message_file)

    # encrypt
    signature = None
    with open(signature_file, "rb") as f:
        signature = f.read()

    try:
        h2 = rsa.decrypt(signature, key)
    except rsa.pkcs1.DecryptionError:
        return False

    return (h1 == h2)


def main():
    try:
        message_file = sys.argv[1]
    except IndexError:
        print("input error")
        return

    if not os.path.exists(message_file):
        print("file doesn't exist")
        return

    (privkey, pubkey) = rsa.newkeys(2048)
    signature_file = make_signature(message_file, privkey)
    filename = input("file with signature:")
    is_valid = check_signature(message_file, filename, pubkey)

    if is_valid:
        print("All it's okay.")
    else:
        print("Wrong signature.")


if __name__ == '__main__':
    main()
