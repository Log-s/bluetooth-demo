import bluetooth

# the server's MAC address
hostMACAddress = "80:32:53:07:BA:8D"
# arbitrary chosen port (needs to be the same for the clients connection)
port = 1
# communication block size (bits)
size = 1024

# creating the socket and binding it
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
print("[+] Socket binded")
s.listen(0)
print("[!] Listening for incomming trafic")

# defining the client variable to avoid an error on keyboard interuption if no connection was established
client = None

try:
    # getting client and client info (A PRECISER)
    client, clientInfo = s.accept()
    print("[!] Connection established to :",clientInfo)
    # data receiving loop
    while True:
        data = client.recv(size)
        if data:
            print(data)
            client.send(data)


except KeyboardInterrupt:	
    print("\n[!] Keyboard interruption : closing connection")
    if client:
        client.close()
    s.close()
except:
    if client:
        client.close()
    s.close()