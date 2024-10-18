from sys import argv
import os
import socket
import re

cmd = argv[1]

def reg_check(input_ip):
    regex = re.compile(r'^[a-z]+\.(com|fr|net|org|edu|gov)$')
    match = regex.match(str(input_ip))
    return bool(match)

validate = reg_check(cmd)
if validate == True:
        hostname, _, ip_addresses = socket.gethostbyname_ex(cmd)
        print(f"{'\n'.join(ip_addresses)}")
else:
    print("L'adresse IP n'est pas valide")