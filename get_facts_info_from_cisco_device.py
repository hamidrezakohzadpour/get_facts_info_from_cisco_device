#To install napalm you just have to run the following command: 
#pip install napalm
#=====================================================================================================================================
import os
from colorama import Fore
from datetime import datetime
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

def str_date_time():
    now = datetime.now()
    str_date = now.strftime("%Y%m%d")
    str_time = now.strftime("%H%M%S")
    return "_" + str_date + "_" + str_time

driver = get_network_driver('ios')
if not os.path.exists("configs"):
    os.mkdir("configs")
if not os.path.exists("configs\\device_ip.txt"):
    file = open("configs\\device_ip.txt", 'w')
    print (Fore.RED + "Please add IP Addresses to configs\\device_ip.txt" + Fore.WHITE)
    file.close()
    exit()
    
with open ("configs\\device_ip.txt",'r') as f:
    devices_list = f.read().splitlines()
    f.close()
for ip_address in devices_list:
    Switch = { 
            "hostname": ip_address,
            "username": "admin",
            "password": "admin",
            "optional_args": {"secret": "admin"} 
            }
    Switch_Driver = driver(**Switch)
    
    try:
        print(Fore.WHITE + f"{'=' * 50}\nConnecting to the Device {Switch['hostname']}")
        Switch_Driver.open()
    except (ConnectionException):
        print(Fore.RED + f"Connecting Failed on {Switch['hostname']}" + Fore.WHITE)
    except (NetmikoAuthenticationException):
        print(Fore.RED + f"Authentication failed. {Switch['hostname']}" + Fore.WHITE)
    except:
        print(Fore.RED + f"Unknown Err!. {Switch['hostname']}" + Fore.WHITE)
    else:
        # Make output file for save IP and Model of Cisco devices 
        output_file_name = "configs\\device_facts.csv"
        with open ( output_file_name, 'a') as f:
            print (Fore.GREEN + "Connected....")
            # This section get fact of cisco devices
            fact = Switch_Driver.get_facts()
            print (Switch['hostname'] + "," 
                   + fact['vendor']+ ","
                   + fact['model']+ "," 
                   + fact['os_version']+ ","
                   + fact['serial_number']+ ","
                   + fact['hostname']+ ","
                   ,file=f)
            print(Fore.GREEN + "Pass...." + Fore.WHITE)
            f.close()
            Switch_Driver.close()