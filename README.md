# metasploit_automation
Need to perform some steps to run the script
  - Install pymetasploit3 uing command: <br />
             pip3 install --user pymetasploit3 <br />
  - Run metasploit and run below commands: <br />
             $ msfconsole <br />
             msf> load msgrpc [Pass=rootroot]  (For now we have expicitely define the password if you need another password edit in the script). <br />
  - Connect metasploit with msfrpcd service: <br />
             msfrpcd -P yourpassword -S     (Edit the port you received in script).
