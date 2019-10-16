import os
import hashlib
import random
from termcolor import colored 

def getHash(file):
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(file, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return(str(hasher.hexdigest()))


def div_ratio(size):
    if size < 1000000:
        return 4
    elif size < 5000000:
        return 9
    elif size < 10000000:
        return 14
    else:
        return 19

def makeParts(outputDir, filePath, ChukSize, name, ext):
    flag = 1
    names = []
    randomizer = int(ChukSize*0.1)
    with open(filePath, "rb") as f:
        while True:
            data = f.read(ChukSize + random.randint(-randomizer, randomizer))
            if not data:
                break
            out = open(outputDir  + "/" + name + str(flag) + "." + ext + ".part", "wb")
            names.append(name + str(flag) + "." + ext + ".part")
            out.write(data)
            out.close()
            flag += 1
    return names
 
def splitFile(fileCompletePath, outputDir):
    filehash = getHash(fileCompletePath)
    statinfo = os.stat(fileCompletePath)
    size = statinfo.st_size
    parts = div_ratio(size)
    dr = int(size/parts)
    folderName = str(fileCompletePath).split("/")[-1]
    ext = folderName.split(".")[-1]
    folderName = folderName.split(".")[0]
    finaloutput = outputDir + "/" + folderName
    try : 
        os.mkdir(finaloutput)
    except:
        pass
    finally:
        names = makeParts(finaloutput, fileCompletePath, dr, folderName, ext)
    return filehash, names, ext


# splitFile("input/eastside.mp3", "output")

def joinFile(folderPath, parts, ext, outputLoc, filehash):
    name = folderPath.split("/")[-1]
    fileT  = open(folderPath + "/" + name + "1."  + ext + ".part", "rb")
    output = fileT.read()
    for i in range(2, parts+1):
        fileT2  = open(folderPath + "/" + name +  str(i) + "."  + ext + ".part", "rb")
        output += fileT2.read()
    lastLoc = outputLoc + "/" + name + "." + ext
    outputFile = open(lastLoc, "wb")
    outputFile.write(output)
    originalHash = getHash(lastLoc)
    if originalHash == filehash:
        print(colored(u'\u2714', 'green') + " File Integrity is correct")
    else:
        print(colored(u'\u274c', 'red') + " File is corrupt")
    return 0

# joinFile("output/eastside", 21, "mp3" , "test")
