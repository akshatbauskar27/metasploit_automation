import os, getpass
import re
import sys
import logging
import argparse
from datetime import datetime
from subprocess import check_output
from pymetasploit3.msfrpc import *


def list_all(client,data):

	logging.info("Inside list_all")
	if "exploits" in data:
		listing_exps=client.modules.exploits
		for i in listing_exps:
			print ("Available exploit modules: ", i)
	elif "auxiliary" in data:
		listing_auxs=client.modules.auxiliary
		for i in listing_auxs:
			print ("Available auxiliary modules:", i)

def list_service(data,services,client):

	logging.info("Inside list_service")
#	services = input ("Enter the service name you want to list: \n")
	if "exploits" in data:
		listing_exp=client.modules.exploits
		matches=[match for match in listing_exp if services in match]
		for i in matches:
			print ("Available exploit: ", i)
	elif "auxiliary" in data:
		listing_aux=client.modules.auxiliary
		matches=[match for match in listing_aux if services in match]
		for i in matches:
			print ("Available auxiliary: ", i)

def exploiting(client):

	logging.info("Inside exploiting")
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

	logging.info("Inside int_shell")
	print ("Interacting with user")
	shell_id = input ("enter the ID received: \n")
	try:
		shell = client.sessions.session(shell_id)
	except Exception as e:
		logging.error("Error occured %s", e)
		sys.exit(1)
	shell.write('whoami')
	print("You are logged in as:" , shell.read())

def get_pid(name):

	return int(check_output(["pidof","-s",name]))


def main():

# =========================== Help section ===============================

	parser = argparse.ArgumentParser(description='Show help for metaconnect')
	parser.add_argument("-e", help="run exploit module", action='store_true')
	parser.add_argument("-a", help="run auxilary module", action='store_true')
	parser.add_argument("-s", metavar='service', type=str, help="show specific service")
	parser.add_argument("-all", help="Show all modules", action='store_true')
	args = parser.parse_args()

# ========================== Help section Ends ==============================


# ========================= Connection establishing =========================
	if len(sys.argv) >= 2:
		pass
	else:
		os.system(f'python py_meta.py -h')
		sys.exit(0)

	logging.basicConfig(filename ='py_meta.log',
				level = logging.INFO,
				format = '%(levelname)s:%(asctime)s:%(message)s')
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	env_tinks = getpass.getuser()
#	logging.info("Script started at %s", dt_string)
	logging.info("================================ Starting Script ===============================================")
	logging.info("Script was run by %s at %s", env_tinks, dt_string)
	logging.info ("Initiating connetion between metasploit and script")
	cmd = 'msfconsole -q -x' + " " + '"load msgrpc' + " " + "[" + "Pass" + "=" + "rootroot" +"];" + " " + 'exit -y"' + " " + ">" + " " "/dev/null"
	cmd1 = "msfrpcd -P " + "rootroot" + " " +  "-S" + " "  +  "2> output.txt"
	logging.info("Loading msgrpc")
	msf_start = os.system(cmd)
	logging.info("Connecting to msfconsole using msfrpcd")
	try:
		msf_connect = os.system(cmd1)
	except Exception as e:
		logging.error("Error occured %s", e)
		sys.exit(1)
	logging.info("Conenction established between msfconsole and msfrpcd")
	try:
		logging.info("Trying to connect client")
		client = MsfRpcClient('rootroot', port=55553)
	except Exception as e:
		logging.error("Error occured %s", e)
		pid_of=get_pid("msfrpcd")
		cmd2 = "kill" + " " + str(pid_of)
		logging.info("Killing Process")
		os.system(cmd2)
		logging.info("Killed Process %s", str(pid_of))
		logging.info("Script Ended %s", dt_string)
		sys.exit(1)

# ========================= Connection established ===================================

# ==========================  User Inputs =============================================


	if args.e:
		logging.info("-e was selected")
		data = "exploits"
		if args.s:
			logging.info("-s was selected with service name %s", args.s)
			services = args.s
			list_service(data,services,client)
		else:
			logging.info("-all is selected")
			list_all(client,data)
	elif args.a:
		logging.info("-a was selected")
		data = "auxiliary"
		if args.s:
			logging.info("-s was selected with service name %s", args.s)
			services = args.s
			list_service(data,services,client)
		else:
			logging.info("-all is selected")
			list_all(client,data)
	else:
		print ("Please use --help to list the variables")
		sys.exit(0)

#========================= User input end ================================================

	if "exploit" in data:
		ask_exploit = input ("You want to exploit the target (Enter y or n) \n")
		if "y" in ask_exploit:
			exploiting(client)
			int_shell(client)
			logging.info("logging out client")
			client.logout()
			pid_of=get_pid("msfrpcd")
			cmd2 = "kill" + " " + str(pid_of)
			logging.info("Killing Process")
			os.system(cmd2)
			logging.info("Killed Process %s", str(pid_of))
			logging.info("Script Ended %s", dt_string)
			sys.exit(0)
		else:
			logging.info("logging out client")
			client.logout()
			pid_of=get_pid("msfrpcd")
			cmd2 = "kill" + " " + str(pid_of)
			logging.info("Killing Process")
			os.system(cmd2)
			logging.info("Killed Process %s", str(pid_of))
			logging.info("Script Ended %s", dt_string)
			sys.exit(0)
	elif "auxiliary" in data:
		logging.info("logging out client")
		client.logout()
		pid_of=get_pid("msfrpcd")
		cmd2 = "kill" + " " + str(pid_of)
		logging.info("Killing Process")
		os.system(cmd2)
		logging.info("Killed Process %s", str(pid_of))
		logging.info("Script Ended %s", dt_string)
		sys.exit(0)


if __name__ == "__main__":
    main()
