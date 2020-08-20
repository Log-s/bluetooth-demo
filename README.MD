A bit of explanation :
-
The bluetooth protocol uses MAC addresses to find the right host to communicate with, unlike TCP/IP protocole wich uses IP addresses. IP addresses are dynamicaly allocated (your local IP address may change from your home network to your friend's home network), while MAC adressses are physical addresses, more like your home address.

This set of programms allows a client to send data (SLT files for example) to a server via bluetooth (so make sure you are in range). For this demo, we place ourselfs in a medical environment, so the data transfer is encrypted, so an attacker who might intercept the bluetooth traffic would have a hard time getting the plain data.

Being a demo, there is no user configuration possibility. MAC addresses will have to be changed directly into the code.


Requirements :
-
* python3
* pybluez : ```sudo apt-get install libbluetooth-dev && python3 -m pip install pybluez```

Usage
-
Run the server on one bluetooth equiped device, and replace the MAC address with the devices address (on windows ```ipconfig /all```) : ```python3 server.py```

Run the client on an other bluetooth equiped device : ```python3 client.py```

On the client side, choose a file to transfer.