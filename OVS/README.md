# Create OVS bridge   

```
ovs-vsctl add-br br0
ifconfig br0 up
ovs-vsctl set-controller br0 tcp:<IP>:6653
```

<br>

# Add wlan port  
Add **wlan port** which will be managed by SDN controller  
Reset **wlan**'s IP and Give this IP to **bridge**  
```
ovs-vsctl add-port br0 wlan0
ifconfig wlan0 0
ifconfig br0 <ip>
/* if device is client */
route add default gw <gate way ip>
/* if device is client */
```
