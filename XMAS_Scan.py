from scapy.all import *


host = '192.168.65.128'          #  Replace it with the IP Address of Host Machine.
ip = socket.gethostbyname(host)
openp = []
filterdp = []
common_ports = {21, 22, 23, 25, 53, 69, 80, 88, 109, 110,
 123, 137, 138, 139, 143, 156, 161, 389, 443,
 445, 500, 546, 547, 587, 660, 995, 993, 2086,
 2087, 2082, 2083, 3128, 3306, 8443, 10000
}


# Function to Check Host is up or down

def is_up(ip):
    icmp = IP(dst=ip)/ICMP()
    resp = sr1(icmp, timeout=10)
    if resp == None:
        return False
    else:
        return True


# Scan Port using XMAS Scan

def probe_port(ip, port, result = 1):
    src_port = RandShort()
    try:
        p = IP(dst=ip)/TCP(sport=src_port, dport=port, flags= 'FPU')
        resp = sr1(p, timeout=2) #Sending Packet
        if str(type(resp)) == "<type 'NoneType'>":
            result = 1
        elif resp.haslayer(TCP):
            if resp.getlayer(TCP).flags == 0x14:
                result = 0
            elif (int(resp.getlayer(ICMP).type)==3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                result = 2
    except Exception as e:
        pass
    return result

# Loop Through the Common Ports to Check if Host is up or down

if is_up(ip):
    for port in common_ports:
        print (port)
        response = probe_port(ip, port)
        if response == 1:
            openp.append(port)
        elif response == 2:
            filterdp.append(port)
    if len(openp) != 0:
        print ("Possible Open or Filtered Ports:")
        print (openp)
    if len(filterdp) != 0:
        print ("Possible Filtered Ports:")
        print (filterdp)
    if (len(openp) == 0) and (len(filterdp) == 0):
        print ("Sorry, No open ports found.!!")
else:
	print ("Host is Down")


            
