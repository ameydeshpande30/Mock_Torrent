import requests
import os
import threading
import getpass
import shutil

from termcolor import colored 
from os.path import dirname, abspath


from support.split_and_join import joinFile


  
root_path =  dirname(dirname(abspath(__file__)))


def make_directories(fname):
    fname = fname.split('.')[0]
    path = root_path + '/static/Temp/' + fname   
    try:
        shutil.rmtree(path)
    except:
        pass
    finally:
        os.mkdir(path)                              #make directory in temp folder
                       

    path1 = root_path + '/static/Torrents/' + fname   
    try:
        shutil.rmtree(path1)
    except:
        pass
    finally:
        os.mkdir(path1)                              #make directory in Torrent folder


def thread_download(ip, fname, part):
    print("Downloading part----->{} from peer----->{}".format(part,ip))
    url = "http://" + ip + '/downloadpart'
    data = {"name":fname.split('.')[0],"part":part}
    r = requests.post(url, json=data)

    pp = str(r.status_code) + " Part----->"+part+"    Done"
    print(colored(pp,'green'))

    source_path = root_path + "/static/Temp/" + fname.split('.')[0] + "/" + part
    with open(source_path, 'wb') as f:
        f.write(r.content)

    destination_path = root_path + "/static/Torrents/" + fname.split('.')[0] + "/" + part
    os.rename(source_path, destination_path)


def start_download(phash, part_info, pweight, fname, response):

    make_directories(fname)
    for part, peers in part_info.items():
        min1 = 90000000000
        rpeer = -1
        for i in peers:
            if pweight[i] < min1:
                rpeer = i
                min1 = pweight[i]
        ip = phash[rpeer]
        t = threading.Thread(target=thread_download, args=(ip, fname, part))
        t.start()
        pweight[rpeer] += 1

    destination = root_path + "/static/Torrents/" + fname.split('.')[0]
    while True:
        if len(os.listdir(destination)) == len(part_info.keys()):

            print("===============================================================")
            folder_path = root_path + "/static/Torrents/" + fname.split('.')[0]
            outputdir_path = "Downloads"
            try : 
                os.mkdir(outputdir_path)
            except:
                pass
            joinFile(folder_path, len(part_info.values()), fname.split('.')[1], outputdir_path, response['data']['file_hash'], response['data']['key'])
            print(colored(u'\u2714', 'green')+" File Downloaded successfully")
            break
