Why this project ?
-
This project acts as a demo for a IT internship interview for **winnove medical**

![README_IMAGE](https://github.com/Log-s/bluetooth-demo/blob/master/ressources/readme_image.jpg)

A bit of explanation :
-
The bluetooth protocol uses MAC addresses to find the right host to communicate with, unlike TCP/IP protocole wich uses IP addresses. IP addresses are dynamicaly allocated (your local IP address may change from your home network to your friend's home network), while MAC adresses are physical addresses, more like your home address.

This set of programms allows a client to send data (STL files for example) to a server via bluetooth (so make sure you are in range). For this demo, we place ourselfs in a medical environment, so the data transfer is encrypted, so an attacker who might intercept the bluetooth traffic would have a hard time getting the plain data. Of course the data is safe as long as the attcker doesn't posses the source code, in which the asymetric crypting keys are writen, and would allow someone to create it's own decryption tools, to decrypt intercepted traffic. 

Being a demo, there is no user configuration possibility. MAC addresses will have to be changed directly into the code, as well as the encryption settings.

Noticable things :
-
I learned a lot about sockets, bluetooth and other things working on this demo.

I implemented a method that I felt was missing in the socket module (```recvall()```). This method allows to receive a large set of data regardless of it's size, while data is received, and the time between packets doesn't exceed the timeout value. Very practical to send and receive STL files for example.

Requirements :
-
* python3
* pycrypto
* pycryptodome

Usage
-
The 2 computers that will communicate will have to be connected through bluetooth.

Run the server on one bluetooth equiped device, and replace the MAC address with the devices address (on linux : ```hcitool dev```) : ```python3 server.py```

Run the client on an other bluetooth equiped device (and replace once again the MAC address, with the same as the server): ```python3 client.py```

On the client side, you can transfer regular text data you directly type in, or files you have on the client's local drive. Transferd files will be stored in the servers */transferd_files* folder.
