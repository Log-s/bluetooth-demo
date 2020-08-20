import socket

# server MAC address
serverMACAddress = '40:e2:30:df:3d:62'
# server port
port = 1

# creating socket and connecting it to the server
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
print("[+] Connected to server, ready to transfer data")

# Main loop for message transfering
while True:
    # get text data
    text = input("Enter msg : ")
    if text == "quit":
        break
    # Send text data
    s.send(str.encode(text))

# Closing socket
s.close()