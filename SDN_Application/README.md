# Create pom.xml   

mvn archetype:generate -Dfilter=org.onosproject: -DarchetypeGroupId=org.onosproject -DarchetypeArtifactId=onos-bundle-archetype -DarchetypeVersion=**Version**  
<br>
Example)  
```
mvn archetype:generate -Dfilter=org.onosproject: -DarchetypeGroupId=org.onosproject -DarchetypeArtifactId=onos-bundle-archetype -DarchetypeVersion=1.13.0
```

<br>
Define value for property 'groupId': **Group**  
Define value for property 'artifactId': **App**  
**ETC:** `Enter`  
<br>
Example)
```
Define value for property 'groupId': kr.ac.postech 
Define value for property 'artifactId': app
<Enter>...
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
# Prerequisite  
First, you need to run **Rserve()** in R (run as background daemon)  
```
install.packages("Rserve")
library(Rserve)
Rserve()
```
<br>
If your **R version is low**, then you can upgrade it using following instructions  
```
add-apt-repository ppa:marutter/rrutter
apt update
apt full-upgrade
```
<br>

# Install & Start Application  

(Application can be installed **with ONOS console**)  
bundle:install mvn:**Group**/**App**/1.0-SNAPSHOT  
start **App**  
<br>
Example)  
```
bundle:install mvn:kr.ac.postech/app/1.0-SNAPSHOT
start app
```