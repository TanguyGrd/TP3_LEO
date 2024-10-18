from sys import argv
import os
import socket
import re
import psutil
import ipaddress
from datetime import datetime
import platform
import subprocess

#dossier temp
specific_path = "D:\\TP3_LEO_DEV"
# Create the directory
try:
    os.makedirs(specific_path)
    print(f"Directory '{specific_path}' created successfully.")
except FileExistsError:
    print(f"Directory '{specific_path}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{specific_path}'.")
except Exception as e:
    print(f"An error occurred: {e}")

#fichier log
LOG_FILE = os.path.join(specific_path, 'network.log')

if not os.path.exists(LOG_FILE):
    open(LOG_FILE, 'w').close()

def write_log(message):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(message + '\n')

def log_command(command, args):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if command == "ip" :
        log_message = f"{timestamp} [INFO] Command '{command}' called successfully."
    else :
        log_message = f"{timestamp} [INFO] Command '{command}' called successfully with argument '{args}'."
    write_log(log_message)

def log_error(command, args):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if command == "ip" :
        log_message = f"{timestamp} [ERROR] Command '{command}' failed."
    else :
        log_message = f"{timestamp} [ERROR] Command '{command}' called with bad arguments : '{args}'."
    write_log(log_message)

result = "Error"

# Lookup
if argv[1] == "lookup":
    def reg_check(input_ip):
        regex = re.compile(r'^[a-zA-Z0-9.-]+\.(com|fr|net|org|edu|gov)$')
        match = regex.match(str(input_ip))
        return bool(match)

    validate = reg_check(argv[2])
    if validate == True:
        hostname, _, ip_addresses = socket.gethostbyname_ex(argv[2])
        result= '\n'.join(ip_addresses)
        log_command("lookup", argv[2]) #LOG
    else:
        result = "L'adresse IP n'est pas valide"
        log_error("lookup", argv[2]) #LOG

# Ping
elif argv[1] == "ping":
    response = os.system(f'ping -n 1 {argv[2]} > NUL 2>&1')  
    if response == 0:
        result = "UP !"
        log_command("ping", argv[2]) #LOG
    else:
        result = "DOWN !"
        log_error("ping", argv[2]) #LOG

# IP
elif argv[1] == "ip":
    if platform.system() == "Windows" :
        interfaces = psutil.net_if_addrs()
        try:
            ip = interfaces["Wi-Fi"][1][1]
            result = str(ip)

            def netmask_to_cidr(netmask):
                try:
                    network = ipaddress.IPv4Network(f"0.0.0.0/{netmask}", strict=False)
                    return network.prefixlen
                except ValueError:
                    return "Invalid netmask"

            cidr = netmask_to_cidr(interfaces["Wi-Fi"][1][2])
            nb_adresses = 2**(32 - cidr)
            result += "\n" + str(nb_adresses) + " adresses"
            log_command("ip", argv[1]) #LOG
        except KeyError:
            result = "Wi-Fi interface not found."
    else :
        try:
            output = subprocess.check_output(['ip', 'a'], universal_newlines=True)
            for line in output.splitlines():
                if 'inet ' in line and 'scope global' in line:
                    ip_info = line.strip().split()
                    ip = ip_info[1].split('/')[0]
                    netmask_cidr = ip_info[1].split('/')[1]
                    nb_adresses = 2**(32 - int(netmask_cidr))
                    result = f"{ip}\n{nb_adresses} addresses"
                    break
        except subprocess.CalledProcessError:
            result = "Error retrieving IP address."

    log_command("ip", argv[1])  # LOG


else:
    result = f"{argv[1]} is not an available command. Déso."

print(result)

if platform.system() == "Windows" :
    print("c windows")
else :
    print("c pas windows")