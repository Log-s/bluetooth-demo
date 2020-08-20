import socket

# local MAC address
server_MAC = '40:e2:30:df:3d:62'
# arbitrary chosen port (needs to be the same for the client)
port = 1
# Data block size
size = 1024

# creating socket and connecting it to the server
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((server_MAC,port))
s.listen(0)
print("[+] Bluetooth socket ready")

# creating client variable, to avoid error on keyboard interuption if no connection was previously made
client = None

try:
    client, address = s.accept()
    print("[+] Remote host connected")
    while True:
        data = client.recv(size)
        # decode bytes to text
        data = str.decode(data)
        if data:
            print(data)
            # echo back response to server
            client.send(data)

except KeyboardInterrupt:	
    print("[!] Keybord Interruption : closing socket")	
    if client:
        client.close()
    s.close()

"""except:
    print("[!] Closing socket")
    if client:
        client.close()
    s.close()"""