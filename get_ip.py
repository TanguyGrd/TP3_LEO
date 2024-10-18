import psutil
import ipaddress

interfaces = psutil.net_if_addrs()
ip = interfaces["Wi-Fi"][1][1]
print(str(ip))

def netmask_to_cidr(netmask):
    try:
        network = ipaddress.IPv4Network(f"0.0.0.0/{netmask}", strict=False)
        return network.prefixlen
    except ValueError:
        return "Invalid netmask"
    
cidr = netmask_to_cidr(interfaces["Wi-Fi"][1][2])

nb_adresses = 2**(32 - cidr)
print(str(nb_adresses) + " adresses")