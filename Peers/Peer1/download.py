import requests


def get_peers(ip, fullnodes, fname):
    for i in fullnodes:
        i1 = "http://" + i + '/download'
        data = {"name":fname}
        r = requests.post(i1,json=data)
        
        print(r.json())

        #Adding peer to network of torrent
        if r.status_code == 200:
            i1 = "http://" + i + '/peer'
            datap = {"name":fname,"ip":ip}
            r = requests.post(i1,json=datap)
            return r,1 
    else:
        print("File does note exist in the network")
        return "Error", 0


def process_peers(r, fname):

    phash = {}
    pinfo = {}
    pweight = {}
    counter = 1
    for i in r["peers"]:
        phash[counter] = i
        i1 = "http://" + i + "/fileinfo"
        data = {"name":fname}
        r = requests.post(i1,json=data)
        r = r.json()
        if r["code"] == 1:
            print("r in download ")
            print(r)
            pweight[counter] = len(r["parts"])

            for j in r["parts"]:
                if pinfo[j] in pinfo.keys():
                    pinfo[j].append(counter)
                else:
                    pinfo[j] = [counter]
            counter += 1
    print(phash)
    print(pinfo)
    print(pweight)

def start_download(ip, fullnodes, fname):

    r,status = get_peers(ip, fullnodes, fname)
    print("r->{} , status->{}".format(r,status))
    if(status == 1):
        print(status)
        process_peers(r,fname)
    else:
        return