import json
import requests
import base64
import jwt

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from os.path import dirname, abspath

base_url = "127.0.0.1:5006"
root_path =  dirname(dirname(abspath(__file__)))


def getEnrolled(uid):
    #making request to CA to get cipher text and SHA512 hash
    payload = {
        "uid":uid
    }

    url = base_url + "/challenge"

    response = requests.post(url, json=payload)
    response = response.json()

    return response['numberHash'], response['hash512']


def authenticate(uid, public_key, private_key, numberHash, hash512):
    number = getNumber(private_key, numberHash)
    payload = {
        "uid":uid,
        "number": number,
        "hash512": hash512
    }

    url = base_url + "/authenticate"
    
    response = requests.post(url, json=payload)
    response = response.json()

    if response['code'] == 1:
        token = jwtVerify(response['token'], public_key)
        return token
    else:
        return False



def getNumber(private_key, cipherText):
    cp = base64.decodebytes(cipherText.encode())
    pr_key = RSA.importKey(open(private_key, 'r').read())
    de = PKCS1_OAEP.new(key=pr_key)
    return de.decrypt(cp)

def jwtVerify(token, public_key):
    payload = jwt.decode(token, public_key, algorithms=['RS256'])
    return payload


         