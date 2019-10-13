from flask import Flask, request
from flask import jsonify
import requests
import os
import json
import hashlib
import threading
import peer_processing as pp
import split_and_join as sj
import global_vars as gvs

app = Flask(__name__)

root_path = os.path.abspath(os.path.dirname(__file__))


filemap = {}
ip = '127.0.0.1:8001'
port = 8001
fullnodes = []
#fname in all files represent the complete file name with extension

'''
To-do

exception handling for already existing folders
'''
def connect_to_fullnodes():
    global fullnodes
    with open('network.json', 'r') as jf:
        data = json.load(jf)
        for f in data:
            fullnodes.append(f)
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
            print("Torrent Added successfully")
            break
        else:
            print("Problem occurred while adding torrent")
    
    print(filemap)

def download_file():

    global ip

    fname = input("Enter the name of the file:")
    pp.start_processing(ip, fullnodes, fname)


if __name__ == '__main__': 


    connect_to_fullnodes()

    import flask_server
    t1 = threading.Thread(target=flask_server.start_server, args=(port,))

    t1.start()

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