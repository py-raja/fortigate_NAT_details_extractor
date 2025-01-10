# Extract VIP Details from Fortinet Firewalls

This Python script extracts Virtual IP (VIP) details, including external and internal IP mappings, from Fortinet Firewalls. The script uses the Netmiko library to connect to the firewalls via SSH, fetches VIP configurations, and processes the data.

## Features

- Connects to multiple Fortinet Firewalls using credentials stored in a file.
- Extracts VIP configurations, including external and internal IP mappings.
- Displays VIP details along with firewall location.

## Requirements

- Python 3.6+
- Required libraries:
  - `netmiko`
  - `re`
  - `ipaddress`

Install the required libraries with the following command:

```bash
pip install netmiko
```

## File Descriptions

- `firewalls.txt`: Contains firewall IP addresses and their locations in the format:
  ```
  <firewall_ip>:<location>
  ```
  Example:
  ```
  192.168.1.1:Headquarters
  192.168.2.1:Branch Office
  ```

- `credentials.txt`: Contains the username and password for the firewalls. The first line is the username, and the second line is the password:
  ```
  admin
  password123
  ```

## Usage

1. Ensure you have the required files (`firewalls.txt` and `credentials.txt`) in the same directory as the script.
2. Run the script with the command:

```bash
python extract_vip_details.py
```

## Example Output

The script outputs VIP details in the following format:

```text
Location: Headquarters ; Name: VIP1 ; Internal_IP: 10.0.0.1 ; External_IP: 203.0.113.1
Location: Branch Office ; Name: VIP2 ; Internal_IP: 10.0.1.1 ; External_IP: 203.0.113.2
```

If no VIP information is found for a firewall, the script will output:

```text
No VIP information found for Firewall <firewall_ip> at location <location>
```

## Script Description

### `extract_vip_details(device_ip, username, password)`

Connects to a Fortinet Firewall and retrieves VIP details.

#### Parameters
- `device_ip`: IP address of the firewall.
- `username`: Username for SSH access.
- `password`: Password for SSH access.

#### Returns
- A list of dictionaries, each containing VIP details:
  - `vip_name`: Name of the VIP.
  - `External_IP`: External IP address.
  - `Internal_IP`: Internal IP address.

### `ip_location(file_path)`

Reads a file containing firewall IP addresses and locations.

#### Parameters
- `file_path`: Path to the file.

#### Returns
- A dictionary mapping IP addresses to locations.

### `read_credentials(file_path)`

Reads a file containing the username and password for firewalls.

#### Parameters
- `file_path`: Path to the file.

#### Returns
- A tuple with the username and password.

## Error Handling

- Handles connection issues using Netmiko exceptions.
- Prints stack traces for unexpected errors.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute it as needed.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue if you find a bug or have a feature request.

