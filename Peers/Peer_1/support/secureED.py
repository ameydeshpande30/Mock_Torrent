import pyAesCrypt

from os import stat
# from M2Crypto import EVP

def encrypt_file(key, in_filename, chunksize=64*1024):
    with open(in_filename, "rb") as fIn:
        with open(str(in_filename).split("/")[-1] + ".aes", "wb") as fOut:
            pyAesCrypt.encryptStream(fIn, fOut, key, chunksize)



def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    encFileSize = stat(in_filename + ".aes").st_size
    with open(in_filename + ".aes", "rb") as fIn:   
        try:
            with open(in_filename, "wb") as fOut:
                # decrypt file stream
                pyAesCrypt.decryptStream(fIn, fOut, key, chunksize, encFileSize)
        except ValueError:
            # remove output file on error
            print("key is wrong")
# k = "hellohowareyou"
# encrypt_file(k, "Server.java")
# decrypt_file(k, "Server.java")