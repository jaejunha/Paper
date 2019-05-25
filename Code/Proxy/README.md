# Allow web port   
To use **proxy server**, need to open web port(**80**)  
```
iptables -A INPUT -p tcp --dport <port number> -j ACCEPT
```
<br>

# Set Server IP
Please modify **server.json** file!  
<br>

# /etc/rc.local  
```
#!/bin/sh
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

service ssh restart
iptables-restore < /etc/iptables.ipv4.nat

su root -c "ifconfig wlan0 0"
su root -c "ifconfig ap0 192.168.100.1"
su root -c "service apache2 stop"
su root -c "iptables -A INPUT -p tcp --dport 80 -j ACCEPT"

exit 0
```
