# Allow web port   
To use **proxy server**, need to open web port(**80**)  
```
iptables -D INPUT -p tcp --dport <포트번호> -j ACCEPT
```