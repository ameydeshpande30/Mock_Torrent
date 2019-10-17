# d = {"1":10,"2":10,"3":20}

# print(min(d, key=d.get))
# import getpass
# print(getpass.getuser())


# import os
# import tkinter
# root = tkinter.Tk()
# root.withdraw() #use to hide tkinter window

# tempdir = tkinter.filedialog.askopenfilename(parent=root, initialdir=os.path.expanduser('~'), title='Please select a file')

# if len(tempdir) > 0:
#     print ("You chose %s" % tempdir)

# import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# try:
#     # doesn't even have to be reachable
#     s.connect(('10.255.255.255', 1))
#     IP = s.getsockname()[0]
# except:
#     IP = '127.0.0.1'
# finally:
#     s.close()
# return IP 

# import sys
# print(type(sys.argv[1]))
import os
import shutil
root_path = os.path.abspath(os.path.dirname(__file__))
path = root_path + '/static/Temp/' + 'fname'   

shutil.rmtree(root_path + '/t')