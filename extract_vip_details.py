import netmiko
import re
import traceback
from ipaddress import ip_network, IPv4Network

def extract_vip_details(device_ip, username, password):
    """
    Extracts detailed VIP information from a fortinet Firewall.

    Args:
        device_ip (str): IP address of the Firewall.
        username (str): Username for Firewall access.
        password (str): Password for Firewall access.

    Returns:
        list: A list of dictionaries, each containing VIP information.
    """
    vip_details = []

    try:
        device = netmiko.ConnectHandler(
            device_type='fortinet',
            ip=device_ip,
            username=username,
            password=password
        )

        # Retrieve VIP List
        vip_list = device.send_command("show firewall vip | grep edit")
        #print(vip_list)

        # Parse VIP details from the output
        for line in vip_list.splitlines():
            if line:
                match = re.search(r'"(.*?)"', line)
                if match:
                    vip_name = match.group(1)
                    vip_output = device.send_command(f' show firewall vip "{vip_name}"')

                    # Extract information and create a dictionary
                    vip_info = {"vip_name": vip_name}
                    extip = re.search(r"extip (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", vip_output)
                    #print(extip.group(1).strip())
                    mappedip = re.search(r'mappedip "(.*?)"', vip_output)
                    #print(mappedip.group(1).strip())
                    vip_info['External_IP'] = extip.group(1).strip()
                    vip_info['Internal_IP'] = mappedip.group(1).strip()
                    vip_details.append(vip_info)

        device.disconnect()
        return vip_details

    except netmiko.NetmikoBaseException as e:
        print(f"Error connecting to device {device_ip}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()

    return None

# Read input from a text file
def ip_location(file_path):
    ip_location = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                ip, location = line.strip().split(":")
                ip_location[ip] = location  
    return ip_location

def read_credentials(file_path):
    with open(file_path, 'r') as file:
        username = file.readline().strip()
        password = file.readline().strip()
    return username, password

# File containing IP addresses and credentials
#input_file = "input.txt"
#straive_networks = "straive_networks.txt"
straive_firewalls = "straive_firewalls.txt"
credentials_file = "credentials.txt"

# Read IP addresses and credentials

ip_location = ip_location(straive_firewalls)
username, password = read_credentials(credentials_file)

# Iterate through devices and extract VLAN information
for firewall_ip, location in ip_location.items():
    vip_info = extract_vip_details(firewall_ip, username, password)
    if vip_info:        
        for vip in vip_info:
            print(f"Location: {location} ; Name : {vip['vip_name']} ; Internal_IP : {vip['Internal_IP']} ; External_IP : {vip['External_IP']}")
    else:
        print(f"No VIP information found for Firewall {firewall_ip} at location {location}")
