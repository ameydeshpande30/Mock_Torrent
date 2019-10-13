import requests
import os
import threading
import global_vars as gvs
import split_and_join as sj
import getpass

root_path = os.path.abspath(os.path.dirname(__file__))


def make_directories(fname):
    fname = fname.split('.')[0]
    path = root_path + '/static/Temp/' + fname      
    os.mkdir(path)                                      #make directory in temp folder

    path1 = root_path + '/static/Torrents/' + fname      
    os.mkdir(path1)                                      #make directory in Torrent folder


def thread_download(ip, fname, part):
    print("Downloading part----->{} from peer----->{}".format(part,ip))
    url = "http://" + ip + '/downloadpart'
    data = {"name":fname.split('.')[0],"part":part}
    r = requests.post(url, json=data)
    print(r.status_code)
    print("Part {} done ".format(part))

    source_path = os.path.abspath(os.path.dirname(__file__)) + "/static/Temp/" + fname.split('.')[0] + "/" + part
    with open(source_path, 'wb') as f:
        f.write(r.content)

    destination_path = os.path.abspath(os.path.dirname(__file__)) + "/static/Torrents/" + fname.split('.')[0] + "/" + part
    os.rename(source_path, destination_path)


def start_download(phash, pinfo, pweight, fname):

    make_directories(fname)
    for part, peers in pinfo.items():
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

    destination = os.path.abspath(os.path.dirname(__file__)) + "/static/Torrents/" + fname.split('.')[0]
    while True:
        if len(os.listdir(destination)) == len(pinfo.keys()):

            folder_path = os.path.abspath(os.path.dirname(__file__)) + "/static/Torrents/" + fname.split('.')[0]
            # outputdir_path = '/home/' + getpass.getuser() + '/Downloads'
            outputdir_path = "Downloads"
            try : 
                os.mkdir(outputdir_path)
            except:
                pass
            sj.joinFile(folder_path, len(pinfo.values()), fname.split('.')[1], outputdir_path)
            print("File Downloaded successfully")
            break
