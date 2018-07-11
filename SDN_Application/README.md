# Create pom.xml   

mvn archetype:generate -Dfilter=org.onosproject: -DarchetypeGroupId=org.onosproject -DarchetypeArtifactId=onos-bundle-archetype -DarchetypeVersion=**Version**  

Example)  

```
mvn archetype:generate -Dfilter=org.onosproject: -DarchetypeGroupId=org.onosproject -DarchetypeArtifactId=onos-bundle-archetype -DarchetypeVersion=1.13.0
```

<br>

# Compile Project  

Normal)  
```
mvn clean install
```

No Test Code)  
```
mvn clean install -DskipTests
```
<br>