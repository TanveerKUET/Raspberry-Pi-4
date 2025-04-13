# Raspberry-Pi-4 remote Access
Step by step guidelines to remotely access Raspberry Pi 4 OS from your Laptop

1.	Turn on your WiFi mobile hotspot in your PC
2.	Rename your SSID as TANVEER PhD CoE
3.	Set Password as r221b816
4.	Connect the type-C cable to Raspberry Pi
5.	Wait for few minutes to boot the OS in raspberry pi
6.	check your Wi-Fi hotspot connected device list at the beginning it is empty

![alt tag](https://github.com/TanveerKUET/Raspberry-Pi-4/blob/main/Raspberry%20Pi%204%20OS%20Remote%20Access/Wi-Fi%20Mobile%20Hotspot%20setup.jpg)

7. Check your Wi-Fi hotspot connected device list at the beginning it is empty
8. When the raspberry pi gets an IP from your PC through DHCP it will be on the device list

![alt_tag](https://github.com/TanveerKUET/Raspberry-Pi-4/blob/main/Raspberry%20Pi%204%20OS%20Remote%20Access/Raspberry%20Pi%204%20gets%20IP%20from%20PC%20hotspot.jpg)

9. Now, we would like to access the raspberry pi using PuTTY through SSH
10. Download the PuTTY and open this 
11. In PuTTY write the IP address of the raspberry pi in this case my raspberry pi gets 192.168.137.19

![alt_tag](https://github.com/TanveerKUET/Raspberry-Pi-4/blob/main/Raspberry%20Pi%204%20OS%20Remote%20Access/PuTTY%20Login.jpg?)

12. Click Open. It will open a terminal window. In terminal window login using username **tanveer** and password **1234**

![alt_tag](https://github.com/TanveerKUET/Raspberry-Pi-4/blob/main/Raspberry%20Pi%204%20OS%20Remote%20Access/PuTTY%20Terminal%20Login%20to%20raspberry%20Pi.jpg)

13. Now you get the access to raspberry pi OS.
14. You can remotely access raspberry Pi as like windows in remote desktop connection through VNC viewer.
15. In the terminal do this command **sudo raspi-config**

![alt_tag](https://github.com/TanveerKUET/Raspberry-Pi-4/blob/main/Raspberry%20Pi%204%20OS%20Remote%20Access/VNC%20configure.jpg)

16. Select Interface options

![alt_tag](https://github.com/TanveerKUET/Raspberry-Pi-4/blob/main/Raspberry%20Pi%204%20OS%20Remote%20Access/Interface%20option.jpg)

17. Select VNC

![alt_tag](https://github.com/TanveerKUET/Raspberry-Pi-4/blob/main/Raspberry%20Pi%204%20OS%20Remote%20Access/Enable%20VNC.jpg)

18. Enable VNC Yes

![alt_tag](https://github.com/TanveerKUET/Raspberry-Pi-4/blob/main/Raspberry%20Pi%204%20OS%20Remote%20Access/Enable%20VNC%20Yes.jpg)

19. Now Download VNC viewer

![alt_tag](https://github.com/TanveerKUET/Raspberry-Pi-4/blob/main/Raspberry%20Pi%204%20OS%20Remote%20Access/Download%20VNC%20viewer.jpg)

20. Open VNC viewer and provide your Raspberry Pi IP address 192.168.137.19 and username and password to connect

![alt_tag](https://github.com/TanveerKUET/Raspberry-Pi-4/blob/main/Raspberry%20Pi%204%20OS%20Remote%20Access/VNC%20Remote%20access.jpg)

21. Now you can see your Raspberry Pi as like windows remote desktop
22. Do what things necessary to do. I open the terminal and check my IP address

![alt_tag](https://github.com/TanveerKUET/Raspberry-Pi-4/blob/main/Raspberry%20Pi%204%20OS%20Remote%20Access/Remote%20Raspberry%20Pi%20Access.jpg)
