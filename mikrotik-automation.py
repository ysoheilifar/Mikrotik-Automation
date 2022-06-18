from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException


username = input('Enter your SSH username: ')
password = getpass()

with open('D:/Netmiko_Itration_script3/commands_all_devices.txt') as f:
	commands_list = f.read().splitlines()

with open('D:/Netmiko_Itration_script3/devices_list.txt') as f:
	devices_list = f.read().splitlines()

for devices in devices_list:
	print('Connecting to ' + devices)
	ip_address_of_device = devices
	ios_device = {
		'device_type': 'mikrotik_routeros',
		'ip': ip_address_of_device,
		'username': username,
	    'password': password,
		 }
	
	try:
		net_connect = ConnectHandler(**ios_device)
	except (AuthenticationException):
		print('Authentication failure: ' + ip_address_of_device)
		continue
	except (NetMikoTimeoutException):
		print('Timeout to device: ' + ip_address_of_device)
		continue
	except (EOFError):
		print('End of file while attempting device ' + ip_address_of_device)
		continue
	except (SSHException):
		print('***SSH Issue*** Are you sure SSH is enable??? ' + ip_address_of_device)
		continue
	except Exception as unknown_error:
		print('Some other error: ' + unknown_error)
		continue    

	output = net_connect.send_config_set(commands_list)
	print(output)