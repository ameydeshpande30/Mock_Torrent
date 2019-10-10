from flask import Flask, request
from flask import jsonify
import requests
import os
import json
import hashlib
app = Flask(__name__)


filemap = {}
fullnodes = []


def connect_to_fullnodes():
    global fullnodes
    with open('network.json', 'r') as jf:
        data = json.load(jf)
        fullnodes = [f for f in data]
        print(fullnodes)

def addtorrent():

    while True:
        my_path = os.path.abspath(os.path.dirname(__file__))
        folname = input("Enter folder name:")
        path = os.path.join(my_path, "../Peers/"+folname)
        if os.path.isdir(path):
            names = []
            for file in os.listdir(folname):
                if file.endswith(".txt"):
                    names.append(file) #to-do

            filemap[folname] = names
            fhash = str(hashlib.md5(open(path+'/main.txt','rb').read()).hexdigest())
            ip = '127.0.0.1:8001'
            data = {"name":folname,"parts":len(names)-1,"fileHash":fhash,"ip":ip}
            print(data)
            for i in fullnodes:
                i1 = "http://" + i + '/torrent'
                print(i1)
                r = requests.post(i1,json=data)
                print(r)
            break
        else:
            print("Folder does not exist")
    print(filemap)


def download():
    print()



# @app.route("/node", methods=['GET', 'POST'])  
# def full_node():
#     if request.method == 'POST':
#         global other_fulll_nodes
#         content = request.get_json(silent=True)
#         node = content["node"]
#         other_fulll_nodes.append(node)
#         return jsonify(content)
#     else:
#         return jsonify(other_full_nodes)
# main driver function 


if __name__ == '__main__': 

    # app.debug = True
    # app.run(port=8001) 

    connect_to_fullnodes()

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