#Importing necessary modules
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify
#The message to be encrypted
message = b'Public and Private keys encryption'
#Generating private key (RsaKey object) of key length of 1024 bits
private_key = RSA.generate(1024)
#Generating the public key (RsaKey object) from the private key
public_key = private_key.publickey()
print(type(private_key), type(public_key))
#Converting the RsaKey objects to string 
private_pem = private_key.exportKey().decode()
public_pem = public_key.exportKey().decode()
print(type(private_pem), type(public_pem))
#Writing down the private and public keys to 'pem' files
with open('pub/private_pem.pem', 'w') as pr:
    pr.write(private_pem)
with open('pub/public_pem.pem', 'w') as pu:
    pu.write(public_pem)