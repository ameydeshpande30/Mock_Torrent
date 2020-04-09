import requests
import json

from support.download import start_download

def get_peers(ip, token, fullnodes, fname):
    for i in fullnodes:
        headers = {
            "token": token
        }
        i1 = "http://" + i + '/download'
        data = {"name":fname}
        r1 = requests.post(i1, headers=headers, json=data)
        # print(r.status_code)  
        # print(r.json())

        #Adding peer to network of torrent
        if r1.status_code == 200:
            i1 = "http://" + i + '/peer'
            datap = {"name":fname, "ip":ip}
            r = requests.post(i1, headers=headers, json=datap)
            if r.status_code == 200:
                return r1,1
            else:
                print("Error in Authentication")
                return "Error", 0 
    else:
        print("File does not exist in the network")
        return "Error", 0


def process_peers(response, token, fname):

    phash = {}
    part_info = {}
    pweight = {}
    counter = 1
    fname = fname.split('.')[0]
    
    for i in response["peers"]:
        phash[counter] = i
        headers = {
            "token": token
        }
        data = {"name":fname}
        i1 = "http://" + i + "/fileinfo"
        try:
            r = requests.post(i1, headers=headers, json=data)
            r = r.json()
            if r["code"] == 1:
                print("r in download ")
                print(r)
                pweight[counter] = len(r["parts"])

                for j in r["parts"]:
                    if j in part_info.keys():
                        part_info[j].append(counter)
                    else:
                        part_info[j] = [counter]
                counter += 1
        except:
            pass
    print(phash)
    print(part_info)
    print(pweight)
    return phash, part_info, pweight

def start_processing(ip, token, fullnodes, fname):

    response,status = get_peers(ip, token, fullnodes, fname)
    print("r->{} , status->{}".format(response,status))
    if(status == 1):
        print(status)
        phash, part_info, pweight = process_peers(response.json(), token, fname)
        start_download(phash, part_info, pweight, fname ,response.json())
    else:
        return
