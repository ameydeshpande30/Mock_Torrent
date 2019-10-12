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
        path = os.path.join(my_path, "../Peers/Peer5/"+folname)
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
                #print(i1)
                r = requests.post(i1,json=data)
                print(r)
            break
        else:
            print("Folder does not exist")
    print(filemap)


def download():
    fname = input("Enter the name of the file:")

    for i in fullnodes:
        i1 = "http://" + i + '/download'
        data = {"name":fname}
        r = requests.post(i1,json=data)
        if r.status_code == 200:
            break
    else:
        print("File does note exist in the network")
        return 
    
    




if __name__ == '__main__': 

    # app.debug = True
    # app.run(port=8001) 

    connect_to_fullnodes()

    while True:
        print("\n1.)Add Torrent")
        print("2.)Download File")
        print("3.)Exit")
        choice = int(input("Enter your choice:"))

        if choice == 1:
            addtorrent()
        elif choice==2:
            download()
        else:
            break