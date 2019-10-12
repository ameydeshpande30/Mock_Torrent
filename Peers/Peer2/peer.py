from flask import Flask, request
from flask import jsonify
import requests
import os
import json
import hashlib
import download as dl

app = Flask(__name__)


filemap = {}
fullnodes = []
ip = '127.0.0.1:8002'
port = 8002

def connect_to_fullnodes():
    global fullnodes
    with open('network.json', 'r') as jf:
        data = json.load(jf)
        fullnodes = [f for f in data]
        print(fullnodes)

def addtorrent():
    global ip
    global filemap

    while True:
        my_path = os.path.abspath(os.path.dirname(__file__))
        folname = input("Enter folder name:")
        path = os.path.join(my_path,folname)
        print(path)
        if os.path.isdir(path):
            names = []
            for file in os.listdir(folname):
                if file.endswith(".txt") and file!="main.txt":
                    names.append(file) #to-do

            filemap[folname] = names
            fhash = str(hashlib.md5(open(path+'/main.txt','rb').read()).hexdigest())
            data = {"name":folname,"parts":len(names)-1,"fileHash":fhash,"ip":ip}
            print(data)
            for i in fullnodes:
                i1 = "http://" + i + '/torrent'
                #print(i1)
                r = requests.post(i1,json=data)
                if r.status_code == 200:
                    print("Torrrent Added successfully")
                    break
            #print(filemap)
            break
        else:
            print("Folder does not exist")
            return 


def download_file():

    global ip

    fname = input("Enter the name of the file:")
    dl.start_download(ip, fullnodes, fname)

    
'''

=====================================================================================
                        Api's start here
=====================================================================================

'''


# @app.route("/fileinfo", methods=['POST'])
# def peer():

#     global filemap
#     content = request.get_json(silent=True)
#     if content["name"] in filemap.keys():
#         data = {"parts":filemap[content["name"]],"code":1}
#     else:
#         data = {"code":0}
#     return jsonify(data)






'''
=====================================================================================
'''
if __name__ == '__main__': 

    # app.debug = True
    # app.run(port=port) 

    connect_to_fullnodes()

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