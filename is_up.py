from sys import argv
import os
import socket

cmd = argv[1]

try:
    socket.inet_aton(cmd)
    is_valid_ip = True
except OSError:
    is_valid_ip = False

if is_valid_ip:
    ping = os.system(f"ping -n 1 {cmd} > NUL 2>&1")
    if ping == 0:
        print("UP !")
    else:
        print("DOWN !")
else:
    print("Donne une vraie adresse IP")