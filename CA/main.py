
from flask import Flask, request
from flask import jsonify
import random
from Crypto.Hash import SHA512
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64
from datetime import datetime, timedelta
import jwt
app = Flask(__name__)
# JWT_SECRET = 'secret'
JWT_ALGORITHM = 'RS256'
JWT_EXP_DELTA_SECONDS = 20000000

private_key = open('JWT.pem').read()
key = "J:8kM~_@,8R-M=&[#H~vquxe9Bt;8Aw3MJRj3s#W"


def createJWT(uid):
    payload = {'user_id': uid,'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)}
    jwt_token = jwt.encode(payload, private_key, JWT_ALGORITHM)
    return jwt_token.decode('utf-8')

@app.route("/challenge", methods=['POST'])
def challange():
    content = request.get_json(silent=True)
    uid = content["uid"]
    out = {}
    out["uid"] = uid
    num = random.randint(a=100,b=1000000)
    
    h = SHA512.new()
    pb_key = RSA.importKey(open('pub/' + str(uid) + '.pub', 'r').read())
    cipher = PKCS1_OAEP.new(key=pb_key)
    out["numberHash"] = base64.b64encode(cipher.encrypt(str(num).encode())).decode()
    ss = str(uid)+str(num)+str(key)
    ss= ss.encode('utf-8')
    h.update(ss)
    out["hash512"] = str(h.hexdigest())
    return jsonify(out)


@app.route("/authenticate", methods=['POST'])
def check():
    content = request.get_json(silent=True)
    uid = content["uid"]
    number = content["number"]
    hash512 = content["hash512"]
    ss = str(uid) + str(number) + str(key)
    ss = ss.encode("utf-8")
    h = SHA512.new()
    h.update(ss)
    checkHash = str(h.hexdigest())
    if checkHash == hash512:
        return jsonify({"code": "1", "token": createJWT(uid)})
  
    else:
        return jsonify({"error": "bad request"})


app.run(port=5006, debug=True)