import socket
import struct
import plistlib
from uuid import getnode as get_mac
from random import randint

packetType="bsdp" # bsdp or dhcp 
#packetType="dhcp" # bsdp or dhcp 

def getMacInBytes():
    mac = str(hex(get_mac()))
    mac = mac[2:]
    while len(mac) < 12 :
        mac = '0' + mac
    macb = b''
    for i in range(0, 12, 2) :
        m = int(mac[i:i + 2], 16)
        macb += struct.pack('!B', m)
    return macb

# http://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-of-eth0-in-python
def get_ip_address():
    # create a new socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # connect on 80
    s.connect(("8.8.8.8", 80))
    # get IP from socket
    return s.getsockname()[0]

def getIPInBytes():
    currIP=get_ip_address().split('.') # put IP address into list
    # print(currIP) # print current IP for testing
    bcurrIP=b'' # Create new byte holder
    for i in currIP:
        # add each part of IP as byte into byte holder
        bcurrIP += struct.pack("!B", int(i))
    # return byte formated IP
    return bcurrIP

def parse_vendor(v_opts):
    # Vendor Options Breakdown:
    # [1,1,1] = BSDP message type (1), length (1), value (1 = list)
    # [4,2,255,255] = Server priority message type 4, length 2, value 0xffff (65535 - Highest)
    # [7,4, x, x] = Option 7 (4) Default Boot Image ID number
    # [9,l, x] Boot Image List option 9 (l = random length) x = image names
    b = bytearray(v_opts)
    results = dict()
    while b:
        option_code  = b.pop(0)
        option_len   = b.pop(0)
        option_value = b[0:option_len]
        del b[0:option_len]
        if option_code == 9:
            # We found our list
            # Now to consume it
            # the list can have multiple entries and each will have its NBI ID 4 bytes as header
            # the full list length will be ALL of those entries - length of name plus 4-byte ID header
            nbi_list = []
            while option_value:
                nbi_id   = struct.unpack('!H', option_value[2:4])
                del option_value[0:4]
                nbi_len  = option_value.pop(0)
                nbi_name = option_value[0:nbi_len]
                del option_value[0:nbi_len]
                nbi_list.append((nbi_id[0], nbi_name.decode('utf-8')))
            results['nbi_list'] = nbi_list
        elif option_code == 7:
            default_nbi = struct.unpack('!H', option_value[2:4])
            results['default_nbi'] = default_nbi[0]
    return results

# write bsdp plist with found BSDP Server IPs and respective netboot sets
def writePlist(plist):
    infoPlist = dict(
        bsdpserver = offer.BSDPServerIP)
    with open(plist, 'wb') as fp:
        plistlib.dump(infoPlist, fp)

        
class DHCPDiscover:
    def __init__(self):
        self.transactionID = b''
        for i in range(4):
            t = randint(0, 255)
            self.transactionID += struct.pack('!B', t) 

    def buildPacket(self):
        macb = getMacInBytes()
        if packetType == "dhcp":
            packet = b''
            packet += b'\x01'   #Message type: Boot Request (1)
            packet += b'\x01'   #Hardware type: Ethernet
            packet += b'\x06'   #Hardware address length: 6
            packet += b'\x00'   #Hops: 0 
            packet += self.transactionID       #Transaction ID
            packet += b'\x00\x00'    #Seconds elapsed: 0
            packet += b'\x80\x00'   #Bootp flags: 0x8000 (Broadcast) + reserved flags
            packet += b'\x00\x00\x00\x00'   #Client IP address: 0.0.0.0
            packet += b'\x00\x00\x00\x00'   #Your (client) IP address: 0.0.0.0
            packet += b'\x00\x00\x00\x00'   #Next server IP address: 0.0.0.0
            packet += b'\x00\x00\x00\x00'   #Relay agent IP address: 0.0.0.0
            #packet += b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
            packet += macb
            packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
            packet += b'\x00' * 67  #Server host name not given
            packet += b'\x00' * 125 #Boot file name not given
            packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
            # DHCP IP Address
            packet += b'\x35\x01\x01'   #Option: (t=53,l=1) DHCP Message Type = DHCP Discover
            packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'   #Option: (t=61,l=6) Client identifier
            packet += b'\x3d\x06' + macb
            packet += b'\x37\x03\x03\x01\x06'   #Option: (t=55,l=3) Parameter Request List
            packet += b'\xff'   #End Option
            packet += b'\x00' * 6
            return packet
        else:
            clientIPb = getIPInBytes()
            packet = b''
            packet += b'\x01'   #Message type: Boot Request (1)
            packet += b'\x01'   #Hardware type: Ethernet
            packet += b'\x06'   #Hardware address length: 6
            packet += b'\x00'   #Hops: 0 
            packet += self.transactionID       #Transaction ID
            packet += b'\x00\x00'    #Seconds elapsed: 0
            packet += b'\x00\x00'   #Bootp flags: 0x0000 (Unicast) + reserved flags
            packet += clientIPb # Client IP address
            # packet += b'\x80vlJ' # Client IP address: 128.118.108.74
            #packet += b'\x00\x00\x00\x00'   # Client IP address: 0.0.0.0
            packet += b'\x00\x00\x00\x00'   #Your (client) IP address: 0.0.0.0
            packet += b'\x00\x00\x00\x00'   #Next server IP address: 0.0.0.0
            packet += b'\x00\x00\x00\x00'   #Relay agent IP address: 0.0.0.0
            #packet += b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
            packet += macb
            packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
            packet += b'\x00' * 67  #Server host name not given
            packet += b'\x00' * 125 #Boot file name not given
            packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
            # NetBoot List Request
            packet += b'\x35\x01\x08'   #Option: (t=53,l=1) DHCP Message Type = DHCP INFORM[LIST]
            packet += b'\x37\x02\x3c\x2b'   #Option: (t=55,l=2) Parameter Request List - Option 60 (3c) and 43 (2b)
            packet += b'\x39\x02\x05\xdc' # Option 57, length 2, max dhcp message sizeL 1500
            # Short APLBSDPC
            # packet += b'\x3c\x39\x41\x41\x50\x4c\x42\x53\x44\x50\x43' # #Option: (t=60,l=9) Client identifier APLBSDPC
            # Long APLBSDPC
            packet += b'\x3c\x17\x41\x41\x50\x4c\x42\x53\x44\x50\x43' # #Option: (t=60,l=23) Client identifier APLBSDPC + next line
            packet += b'\x2f\x69\x33\x38\x36\x2f\x69\x4d\x61\x63\x31\x34\x2c\x32' #Model /i386/iMac14,2
            packet += b'\x2b\x0f\x01\x01\x01\x02\x02\x01\x01\x05\x02\x03\xe1\x0c\x02\x20\x00' #Option 43 vendor specific???        
            packet += b'\xff'   #End Option
            return packet

class BSDPOffer:
    def __init__(self, data, transID):
        self.type = "bsdp"
        self.plistName = "/tmp/com.example.bsdpptest.plist"
        self.data = data
        self.transID = transID
        self.ClientIP = ''
        self.nextServerIP = ''
        self.vendorOptionResults = {}
        self.BSDPServerIP = ''
        self.vendorClassID = ''
        self.unpack()

    def unpack(self):
        # print(self.data) # print out the data for testing
        
        print('{0}{1}'.format('Length: ', len(self.data)))
        if self.data[4:8] == self.transID :
            self.ClientIP = '.'.join(map(lambda x:str(x), data[12:16]))
            self.nextServerIP = '.'.join(map(lambda x:str(x), data[20:24]))  #c'est une option
            self.vendorOptionResults = parse_vendor(self.data[242:274]) # Vendor Options 240-273
            self.BSDPServerIP = '.'.join(map(lambda x:str(x), data[279:283]))
            self.vendorClassID = "".join(map(chr,data[286:294]))
            # print(self.vendorOptionResults['nbi_list'][0][1]) # print NBIName (1) from first entry in list (0)

    def printOffer(self):
        key = ['Client IP', 'BSDP Server IP' , 'Vendor Class ID']
        val = [self.ClientIP, self.BSDPServerIP, self.vendorClassID]
        for i in range(3):
            print('{0:20s} : {1:15s}'.format(key[i], val[i]))
        
        # print(self.vendorOptionResults['nbi_list'])
        print('{0:20s}{1}'.format('NetBoot Image Names ', ' : ' , end=''))
        if self.vendorOptionResults['nbi_list'][0]:
            print('{0:21s}  {1:15s} (ID: {2})'.format(' ', self.vendorOptionResults['nbi_list'][0][1], self.vendorOptionResults['nbi_list'][0][0]))
        if len(self.vendorOptionResults['nbi_list']) > 1:
            for i in range(1, len(self.vendorOptionResults['nbi_list'][0])): 
                print('{0:22s} {1:15s}'.format(' ', self.vendorOptionResults['nbi_list'][0][i]))

        print('{0:20s} :{1:15}'.format('Default Image ID ', self.vendorOptionResults['nbi_list'][0][0]))


class DHCPOffer:
    def __init__(self, data, transID):
        self.type = "dhcp"
        self.plistName = "/tmp/com.example.dhcptest.plist"
        self.data = data
        self.transID = transID
        self.offerIP = ''
        self.nextServerIP = ''
        self.DHCPServerIdentifier = ''
        self.leaseTime = ''
        self.router = ''
        self.subnetMask = ''
        self.DNS = []
        self.unpack()
    
    def unpack(self):
        print('{0}{1}'.format('Length: ', len(self.data)))
        if self.data[4:8] == self.transID :
            self.offerIP = '.'.join(map(lambda x:str(x), data[16:20]))
            self.nextServerIP = '.'.join(map(lambda x:str(x), data[20:24]))  #c'est une option
            self.DHCPServerIdentifier = '.'.join(map(lambda x:str(x), data[245:249]))
            self.leaseTime = str(struct.unpack('!L', data[251:255])[0])
            self.router = '.'.join(map(lambda x:str(x), data[257:261]))
            self.subnetMask = '.'.join(map(lambda x:str(x), data[263:267]))
            dnsNB = int(data[268]/4)
            # dnsNB = ord(data[268])/4 
            for i in range(0, 4 * dnsNB, 4):
                self.DNS.append('.'.join(map(lambda x:str(x), data[269 + i :269 + i + 4])))
                
    def printOffer(self):
        key = ['DHCP Server', 'Offered IP address', 'subnet mask', 'lease time (s)' , 'default gateway']
        val = [self.DHCPServerIdentifier, self.offerIP, self.subnetMask, self.leaseTime, self.router]
        for i in range(4):
            print('{0:20s} : {1:15s}'.format(key[i], val[i]))
        
        print('{0:20s}{1}'.format('DNS Servers ', ' : ' , end=''))
        if self.DNS:
            print('{0:21s}  {1:15s}'.format(' ', self.DNS[0]))
        if len(self.DNS) > 1:
            for i in range(1, len(self.DNS)): 
                print('{0:22s} {1:15s}'.format(' ', self.DNS[i])) 

    def writePlist(self):
        infoPlist = dict(
            ipaddress = self.offerIP,
            dhcpserverip = self.DHCPServerIdentifier)
        with open(self.plistName, 'wb') as fp:
            plistlib.dump(infoPlist, fp)
            
if __name__ == '__main__':
    #defining the socket
    dhcps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #internet, UDP
    dhcps.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #broadcast
    
    try:
        if packetType == "dhcp":
            dhcps.bind(('', 68))    #we want to listen on 68 for DHCP
        else:
            dhcps.bind(('', 993))    #we want to listen on 993 for BSDP
    except Exception as e:
        print('port 68 in use...')
        dhcps.close()
        input('press any key to quit...')
        exit(0)
 
    #buiding and sending the DHCPDiscover packet
    discoverPacket = DHCPDiscover()
    dhcps.sendto(discoverPacket.buildPacket(), ('<broadcast>', 67))
    
    print('DHCP Discover sent waiting for reply...\n')
    bsdpServerIPs = []
    #receiving DHCPOffer packet  
    dhcps.settimeout(10)
    try:
        while True:
            data = dhcps.recv(1024)
            if packetType == "dhcp":
                offer = DHCPOffer(data, discoverPacket.transactionID)
                if offer.offerIP:
                    offer.printOffer()
                    writePlist(offer)
                    break
            else:
                if len(data) < 300: # BSDP packets are 295, only check for those ignoring the DHCP responses
                    offer = BSDPOffer(data, discoverPacket.transactionID)
                    if offer.BSDPServerIP:
                        offer.printOffer()
                        bsdpServerIPs.append(offer.BSDPServerIP)
                        writePlist(offer)
                        # break
    except socket.timeout as e:
        print(e)
    
    dhcps.close()   #we close the socket
    
    print(bsdpServerIPs)
    # input('press any key to quit...')
    exit()
    

# Example Codes:    
# Vendor Option Block
#\x01\x01\x01 - [1,1,1] = BSDP message type (1), length (1), value (1 = list)
#\x04\x02\xd6\xcb - [4,2,255,255] = Server priority message type 4, length 2, value 0xffff (65535 - Highest)
#\x07\x04\x81\x00\x13\xba - Option 7 (4bytes long) Default Boot Image ID
#\x09\x11\x81\x00\x13\xba\x0c\x43\x4c\x4d\x42\x75\x69\x6c\x64\x4d\x65\x6e\x75 - Boot Image List option (option 9)

# Vendor Info breakdown Example
# vendorInfo=b'\x81\x00\x13\xba\x0c\x43\x4c\x4d\x42\x75\x69\x6c\x64\x4d\x65\x6e\x75'
# vendorlist=""
# vendorlist = "".join(map(chr,vendorInfo[5:]))
# print(vendorInfo[0:4])
# for each in range(len(vendorInfo)) :
#     vendorlist.append(ord(vendorInfo[each]))
# print(vendorlist)
# exit(0)