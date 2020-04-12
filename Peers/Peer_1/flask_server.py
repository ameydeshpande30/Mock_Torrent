from flask import Flask, request
from flask import send_file
from flask import jsonify
import os
app = Flask(__name__)
root_path = os.path.abspath(os.path.dirname(__file__))


    
'''

=====================================================================================
                        Api's start here
=====================================================================================

'''


@app.route("/fileinfo", methods=['POST'])
def peer():

    content = request.get_json(silent=True)
    path = root_path + '/static/Torrents/'+ content["name"]
    try:
        parts = os.listdir(path)
    except:
        parts = []
    if len(parts)!= 0:
        data = {"parts":parts,"code":1}
    else:
        data = {"code":0}
    return jsonify(data)


@app.route("/downloadpart", methods=['POST'])
def download():
    content = request.get_json(silent=True)
    name = content["name"]
    part = content["part"]
    path = os.path.abspath(os.path.dirname(__file__)) + "/static/Torrents/" + name + "/" + part
    print(path)
    return send_file(path, attachment_filename = part)




'''
=====================================================================================
'''

def start_server(port):
    app.debug = False
    app.run(port=port,host= '0.0.0.0') 
    print("Flask Server started")

import sys
start_server(int(sys.argv[1]))