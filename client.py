import bluetooth

# the server's MAC address
server_MAC = '80:32:53:07:BA:8D'
# port chosen on the server
port = 1

# creating the socket and binding it
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((server_MAC, port))
print("[+] Connection to the server made")

# sending text to the server
while 1:
    # getting input
    text = input()
    if text == "quit":
        break
    # seding input
    s.send(text)
s.close()