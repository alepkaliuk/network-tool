# network-tool
This script was created to monitor and alarm about incidents on Cisco routers with IOS XE.
Script installation is need set up of guest-shell on the Cisco router. Before using it, write all log messages to /flash/guest-share/log_file.
The script checks the log file, checks log time, and checks the severity level of the log if it is upper 4 - sends a notification using Telegram API. 

Tested on Cisco Router 1111 IOS XE 17.3.5.
