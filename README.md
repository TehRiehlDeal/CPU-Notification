# CPU Notification

This project is used on my media server to constantly check the temperature
of the system and make sure it doesn't go over a target temperature that can be changed.

If it does reach higher than the target temperature it will send the owner an email that
the machine is overheating and advise them to take action

# Prerequisites
### Ubuntu Linux
If you are running on an Ubuntu machine you will have to install a few things for this script to work.
- You'll have to install lm-sensors and hddtemp
```
sudo apt install lm-sensors hddtemp
```
- Next you'll want to run the sensors-detect command to have it detect all your devices
```
sudo sensors-detect
```
- Finally to check that everything worked you can just run the sensors command
```
sensors
```
### Mac OS
If you are running on Mac OS you'll need a couple things to get this script to work.
- Make sure you have ruby installed on your machine
```
brew install ruby
```
- Then you want to install iStats
```
gem install iStats
```
# How to use

### Using screen
- To keep from having to work with cronjobs you can run the script in a 'screen'
```
sudo apt install screen
```
- Start a new screen
```
screen -S screenName
```
This will open up a seperate terminal window that will always be running in the background.
- First clone the repo to where you want the script located
```
git clone https://github.com/TehRiehlDeal/CPU-Notification.git
```
- From there change directories to where the script is located
```
cd /CPU-Notification
```
- Create a credentials.py file and put your email address and password into the file
```
touch credentials.py
```
- Then run the script and it should work
```
python3 main.py
```
- To exit a screen hit CTRL+a then press d
- To get back into the screen you created run
```
screen -r screenName
```

### Make it a system service
* I have provided a service unit file, what you need to do is edit it so that it has the correct path to the main.py file.
* Then you will have the file to /lib/systemd/system/pycputemp.service
```
sudo cp pycputemp.service /lib/systemd/system/pycputemp.service
```
* Set the file permissions correctly
```
sudo chmod 644 /lib/systemd/system/pycputemp.service
```
* Reload the systemd
```
sudo systemctl daemon-reload
```
* Enable the service so it runs at boot
```
sudo systemctl enable pycputemp.service
```
This will set it up to run at boot, if it throws any errors then something is wrong with the unit file
* Reboot your system
```
sudo reboot
```
You can check to make sure the service is running as intended by running the following command
```
sudo systemctl status pycputemp.service
```
# Planned Features

Eventually I want to add the ability for it to read emails so that the user can 
send in commands for it to run to hopefully correct the problems. 

For example the user could reply asking for the server to be shutdown or restarted and the
script would read the email see the requested action and perform said action.