from flask import Flask, request
from flask import jsonify
import requests
import os
import json
import hashlib
import download as dl
import split_and_join as sj
app = Flask(__name__)

root_path = os.path.abspath(os.path.dirname(__file__))


filemap = {}
fullnodes = []
ip = '127.0.0.1:8001'
port = 8001

def connect_to_fullnodes():
    global fullnodes
    with open('network.json', 'r') as jf:
        data = json.load(jf)
        fullnodes = [f for f in data]
        print(fullnodes)

def addtorrent():
    global ip
    global filemap

    file_path = input("Enter complete file path:")
    folname = file_path.split('/')[-1]
    directory_path = root_path + "/static/Torrents/"
    filehash, names, ext = sj.splitFile(file_path, directory_path)
    print(len(names))
    print(names)

    filemap[folname] = names
    data = {"name":folname,"parts":len(names),"fileHash":filehash,"ip":ip,"ext":ext}

    for i in fullnodes:
        i1 = "http://" + i + '/torrent'
        #print(i1)
        r = requests.post(i1,json=data)
        if r.status_code == 200:
            print("Torrrent Added successfully")
            break
        else:
            print("Problem occurred while adding torrent")

def download_file():

    global ip

    fname = input("Enter the name of the file:")
    dl.start_download(ip, fullnodes, fname)

    
'''

=====================================================================================
                        Api's start here
=====================================================================================

'''


@app.route("/fileinfo", methods=['POST'])
def peer():

    global filemap
    content = request.get_json(silent=True)
    if content["name"] in filemap.keys():
        data = {"parts":filemap[content["name"]],"code":1}
    else:
        data = {"code":0}
    return jsonify(data)






'''
=====================================================================================
'''
if __name__ == '__main__': 

    connect_to_fullnodes()
    addtorrent()
    app.debug = False
    app.run(port=port) 


    while True:
        print("\n1.)Add Torrent")
        print("2.)Download File")
        print("3.)Exit")
        choice = int(input("Enter your choice:"))

        if choice == 1:
            addtorrent()
        elif choice==2:
            download_file()
        else:
            break