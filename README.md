# Fiberhome HG6145F1 Web Admin Password Generator
Generates web admin password for Fiberhome HG6145F1 ONT available in Algeria 

The password is device specific because it is derived from the device's MAC address

|       Model      |    HG6145F1   |       HG6145D2       |        HG6243C       | SR1041F<br>(repeater) |
|:----------------:|:-------------:|:--------------------:|:--------------------:|:---------------------:|
| Firmware Version |     RP4423    |        RP2902        |        RP2951        |           -           |
|   Compatibility  | ✔️<br>(Tested) | ✔️<br>(User reported) | ❌<br>(User reported) |           ❌           |


Usage: 
- Use provided python code or download windows binary from [**here**](https://github.com/numberonedz/Fiberhome-HG6145F1-DZA-Web-Admin-Pass/releases/latest)  
**You can also download and open provided HTML page with your web browser (no internet connection required)
- Enter your device's MAC address ( XX:XX:XX:XX:XX:XX ) to generate the password
- Copy the generated password and use it to login in the web interface ( http://192.168.1.1 | username: admin ) 
- Optional but recommended: change the default admin password


## "Admin account unavailable!"

This issue affects newly shipped ONT devices running firmware RP4423. To resolve it, simply connect the fiber optic cable to the device and try again.



**Disclaimer**
This project is provided for educational and learning purposes only
