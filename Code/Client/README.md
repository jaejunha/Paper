## Info  
### DASH Player   
To play DASH player, need to set some environment   

<br>

Run google-chrome including **option** (at root mode)  
```
google-chrome --allow-file-access-from-files --no-sandbox 
```

<br>

Need to install **some plugins**   

<br>

Falcon Proxy  
```
https://chrome.google.com/webstore/detail/falcon-proxy/gchhimlnjdafdlkojbffdkogjhhkdepf?hl=ko
```

<br>

Allow-Control-Allow-Origin: *  
```
https://chrome.google.com/webstore/detail/allow-control-allow-origi/nlfbmbojpeacfghkpbjhddihlkkiljbi
```

<br>

Need to add below **header** (through above plugin)
```
Access-Control-Allow-Headers: Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers
```

<br>

In addition, need to **modify mpd files** because google-chrome doesn't support avc1 codec
```
avc1 -> avc1.4d401f
```
