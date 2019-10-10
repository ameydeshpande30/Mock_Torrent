import db as db
from flask import Flask, request
from flask import jsonify

app = Flask(__name__)
other_fulll_nodes = []
@app.route("/")
def hello_world(): 
    d = {
        "key" : "value"
    }
    return jsonify(d)

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

@app.route("/torrent", methods=['POST'])
def torrent():
    content = request.get_json(silent=True)
    name = content["name"]
    parts = content["parts"]
    file_hash = content["fileHash"]
    ip = content["ip"]
    db.addData(name, parts, file_hash, ip)
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
    db.addPeer(ip, peer)
    return jsonify({"code" : 1})

if __name__ == '__main__': 
    app.debug = True
    app.run(port=5001) 