import os
os.popen('gsettings set org.gnome.system.proxy mode manual')
os.popen('gsettings set org.gnome.system.proxy.http host 192.168.100.1')
os.popen('gsettings set org.gnome.system.proxy.http port 80')
