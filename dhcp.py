import socket
import time 
address = (socket.gethostname(), 50007)
client = socket.socket()
client.settimeout(0.1)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Next line might or might not work, depending on your platform.
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
sol_ip = socket.SOL_IP
print(sol_ip)
sol_mul_ip = socket.IP_MULTICAST_TTL
print(sol_mul_ip)
s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)

s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)

dhcp_server_port=67 # DHCP Traffic trying to reach a server (not sure actually...)
addr="0.0.0.0" # From all Interfaces/IPs
buf_size=1024

s.bind(('', dhcp_server_port))

intf = socket.gethostbyname(socket.gethostname())
s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(intf))

# "IP_ADD_MEMBERSHIP" is an invalid argument on (OSX at least).
#s.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton(intf))

data, sender_addr = s.recvfrom(buf_size)

# "IP_DROP_MEMBERSHIP" is also an invalid argument on (OSX at least).
#s.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton('0.0.0.0'))

s.close()

print (":".join("{:02x}".format(ord(c)) for c in data))
