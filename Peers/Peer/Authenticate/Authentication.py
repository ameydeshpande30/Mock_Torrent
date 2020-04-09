import json
import requests
import base64
import jwt

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from os.path import dirname, abspath

base_url = "http://127.0.0.1:5006"
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


def authenticate(uid, numberHash, hash512):
    number = getNumber(uid, numberHash)
    payload = {
        "uid":uid,
        "number": number,
        "hash512": hash512
    }

    url = base_url + "/authenticate"
    
    response = requests.post(url, json=payload)
    response = response.json()
    print(response)
    if 'code' in response.keys() and response['code'] == 1 :
        token = response['token']
        return True, token
    else:
        return False, ""


def getNumber(uid, cipherText):
    cp = base64.decodebytes(cipherText.encode())
    path = root_path + '/Authenticate/' + str(uid) + '_private_pem.pem'
    pr_key = RSA.importKey(open(path, 'r').read())
    de = PKCS1_OAEP.new(key=pr_key)
    return de.decrypt(cp)

