# metasploit_automation
Need to perform some steps to run the script
  - Install pymetasploit3 uing command:
             pip3 install --user pymetasploit3
  - Run metasploit and run below commands:
             $ msfconsole
             msf> load msgrpc [Pass=rootroot]  (For now we have expicitely define the password if you need another password edit in the script).
  - Connect metasploit with msfrpcd service:
             msfrpcd -P yourpassword -S     (Edit the port you received in script).
