import db as db
from flask import Flask, request
from flask import jsonify
import asyncio, requests
import argparse
parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('port', type=int, help='Port To Run The Server')
args = parser.parse_args()
port = args.port
# db.init(str(port))
app = Flask(__name__)
other_fulll_nodes = []
@app.route("/")
def hello_world(): 
    d = {
        "key" : "value"
    }
    return jsonify(d)

# @asyncio.coroutine
def syncAllTorrent(name, parts, filehash, ip, ext, key):
    data = {"name":name,"parts":parts,"fileHash":filehash,"ip":ip, "ext": ext, "key" : key}
    for i in other_fulll_nodes:
        i1 = "http://" + i + '/ntorrent'
        r = requests.post(i1,json=data)

# @asyncio.coroutine
def syncAllPeer(name, ip):
    data = {"name":name,"ip":ip}
    for i in other_fulll_nodes:
        i1 = "http://" + i + '/npeer'
        r = requests.post(i1,json=data)

@app.route("/node", methods=['GET', 'POST'])  
def full_node():
    if request.method == 'POST':
        global other_fulll_nodes
        content = request.get_json(silent=True)
        node = content["node"]
        other_fulll_nodes.append(node)
        return jsonify(content)
    else:
        return jsonify(other_fulll_nodes)
# main driver function 
@app.route("/ntorrent", methods=['POST'])
def ntorrent():
    content = request.get_json(silent=True)
    name = content["name"]
    parts = content["parts"]
    file_hash = content["fileHash"]
    ip = content["ip"]
    ext = content["ext"]
    key = content["key"]
    db.addData(name, parts, file_hash, ext, ip, key)
    return jsonify({"code" : 200})

@app.route("/torrent", methods=['POST'])
def torrent():
    content = request.get_json(silent=True)
    print(content)
    name = content["name"]
    parts = content["parts"]
    file_hash = content["fileHash"]
    ip = content["ip"]
    ext = content["ext"]
    key = content["key"]
    db.addData(name, parts, file_hash, ext, ip, key)
    syncAllTorrent(name, parts, file_hash, ip, ext, key)
    return jsonify({"code" : 200})

@app.route("/download", methods=['POST'])
def download():
    content = request.get_json(silent=True)
    name = content["name"]
    out = db.getTorrent(name)
    data = {}
    data["data"] = out
    data["peers"] = db.getPerrs(name)
    return jsonify(data)

@app.route("/peer", methods=['POST'])
def peer():
    content = request.get_json(silent=True)
    name = content["name"]
    ip = content["ip"]
    db.addPeer(ip, name)
    syncAllPeer(name, ip)
    return jsonify({"code" : 1})

@app.route("/npeer", methods=['POST'])
def npeer():
    content = request.get_json(silent=True)
    name = content["name"]
    ip = content["ip"]
    db.addPeer(ip, name)
    return jsonify({"code" : 1})

if __name__ == '__main__': 
    app.debug = False
    app.run(port=port, host= '0.0.0.0') 
