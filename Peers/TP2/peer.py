from flask import Flask, request
from flask import jsonify
from tkinter import filedialog
import requests
import os
import json
import hashlib
import threading
import peer_processing as pp
import split_and_join as sj
import global_vars as gvs
import time
import tkinter
import socket
import sys

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP 

#Global Variables
filemap = {}
port = sys.argv[1]
ip = get_ip() + ':' + port
fullnodes = []
root_path = os.path.abspath(os.path.dirname(__file__))
#================================================================================================================================

def connect_to_fullnodes():
    global fullnodes
    with open('network.json', 'r') as jf:
        data = json.load(jf)
        for f in data:
            fullnodes.append(f)
        print(fullnodes)

def get_file_path():
    root = tkinter.Tk()
    root.withdraw()
    path = None
    s = None
    path = filedialog.askopenfilename(parent=root, initialdir=os.path.expanduser('~'), title='Please select a file')
    if len(path) == 0:
        print("File not selected properly")
        return 0, False
    else:
        return path, True

def addtorrent():
    global ip
    global filemap
        
    file_path, s = get_file_path()
    if s:
        folname = file_path.split('/')[-1]
        directory_path = root_path + "/static/Torrents"     #Add try catch over here
        filehash, names, ext, key = sj.splitFile(file_path, directory_path)
        print(len(names))
        print(names)

        filemap[folname] = names
        data = {"name":folname,"parts":len(names),"fileHash":filehash,"ip":ip,"ext":ext, "key" : key}

        for i in fullnodes:
            i1 = "http://" + i + '/torrent'
            #print(i1)
            r = requests.post(i1,json=data)
            if r.status_code == 200:
                print("Torrent Added successfully")
                break
            else:
                print("Problem occurred while adding torrent")
    else:
        return 

    
    # print(filemap)

def download_file():

    global ip
    
    start = time.time()

    fname = input("Enter the name of the file:")
    pp.start_processing(ip, fullnodes, fname)

    end = time.time()
    print("Seconds consumed->{}".format(end - start))
    print("===========================================================================================")

#=============================================================================================================================================
if __name__ == '__main__': 


    connect_to_fullnodes()

    # import flask_server
    # # t1 = threading.Thread(target=flask_server.start_server, args=(port,))
    # # t1.start()
    string1 = "python3 flask_server.py " + port
    string2 = "gnome-terminal -e '" + string1 +"'"
    os.system(string2)

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