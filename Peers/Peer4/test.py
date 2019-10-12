from flask import Flask, request
from flask import jsonify


import requests
import os

filemap = {}

def addtorrent():

    while True:
        folname = input("Enter folder name:")
        if os.path.isdir('/home/blazehunter/College/SEM7/LP-2/DS/Mock_Torrent/Peers/'+folname):
            names = []
            for file in os.listdir(folname):
                if file.endswith(".txt"):
                    names.append(int(file[0]))

            filemap[folname] = names
            break
        else:
            print("Folder does not exist")
    print(filemap)


def download():
    print()

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


if __name__ == '__main__': 

    app.debug = True
    app.run(port=8001) 
    while True:
        print("1.)Add Torrent\n")
        print("2.)Download File\n")
        print("3.)Exit")
        choice = int(input("Enter your choice:"))

        if choice == 1:
            addtorrent()
        elif choice==2:
            download()
        else:
            break