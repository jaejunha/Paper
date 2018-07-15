# Create OVS bridge   

```
ovs-vsctl add-br br0
ifconfig br0 up
ovs-vsctl set-controller br0 tcp:<IP>:6653
```

<br>