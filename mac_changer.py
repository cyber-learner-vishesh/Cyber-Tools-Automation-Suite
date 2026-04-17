import re 
import subprocess as sp
import optparse as opt
import time
def project_parser():
    parser = opt.OptionParser()
    parser.add_option("-i" , "--interface" ,dest = "interface" , help= "use to specify the interface")
    parser.add_option("-s" , "--show",action="store_true", dest = "options_interface" , help="list all thhe avail interface")
    parser.add_option("-m" , "--mac-add" ,dest="mac_address", help="use to specify the mac_address to chnage to ")

    
    
    try:
        (options,argument)=parser.parse_args()
        output = sp.run("ifconfig | grep '^[a-zA-Z0-9]' | cut -d: -f1",shell=True , text=True , capture_output=True)
        
        optionslist=output.stdout.strip().split('\n')
        


        if options.options_interface !=None:
            print(optionslist)
        
        if options.interface!=None:
            if (options.interface not in optionslist) :
                print("[-] Invalid Interface use -s to see the interface")
                exit()

        if options.mac_address!=None: 
            if not re.match(r"^([0-9A-Fa-f]{2}[:\-]){5}([0-9A-Fa-f]{2})$",options.mac_address):
                print("[-] Invalid Mac address")
                exit()
        
        return parser.parse_args()
    except Exception as e:
        print(options)
        print(f"[-] some error has occured . {e}")
    
def change_mac(interface,mac_address):
    sp.run(["ifconfig",interface,'down'])
    sp.run(["ifconfig",interface,"hw", 'ether',mac_address])
    sp.run(["ifconfig",interface,'up'])
    time.sleep(0.05)
    

    ipconfig_result = sp.run(["ifconfig", interface],text=True ,capture_output=True)
    print(ipconfig_result.stdout)
    new_mac_address = re.search(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}",ipconfig_result.stdout)
    print(new_mac_address.group(0))

    if new_mac_address[0] == mac_address:
         return "changed Successfully"
    else:
         return "Something went wrong"

if __name__ =="__main__":
    try:
        (options,argument)=project_parser()
        
        result = change_mac(options.interface,options.mac_address)
        
        print(result)
    except Exception as e:
        print(f"error {e}")
