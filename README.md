# Gazebo Garden installation
To install correctly gazebo garden we have to delete all packages related to gazebo
```
sudo apt-get remove gazebo*
```

Then install gazebo garden 
```
sudo apt-get update
sudo apt-get install lsb-release curl gnupg
sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install gz-garden
```

Finally install the ros_gz package
```
apt-get install ros-humble-ros-gzgarden
```
