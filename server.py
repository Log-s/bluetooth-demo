import socket, os.path

def close_socket(client, s):
    """
    This function closes a socket
    § param :
        - client  : remote client
        - s       : socket
    """
    if client:
        client.close()
    s.close()

def write_file(file_name, byte_file):
    """
    writes a byte file on the server
    § param :
        - file_name : the file name
        - byte_file : file decomposed as bytes
    """
    path = "transferd_files/"
    # if the folder doesn't exists yet, creates it
    if not os.path.isdir(path):
        os.mkdir(path)
    # writes the file
    with open(path+file_name, "wb") as f:
        f.write(byte_file)

# local MAC address
server_MAC = '40:e2:30:df:3d:62'
# arbitrary chosen port (needs to be the same for the client)
port = 1
# Data block size
size = 1024
file_size = 1000000 # 10x greater the regular size

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
        print(data)
        if data: # if data is not None
            if data.decode() == "FILE_TRANSFER": # if the file transfer protocol is enganged
                print("[+] File transfer started")
                # gets the file name
                file_name = client.recv(size).decode()
                print(file_name)
                # gets the file
                bytes_file = b''
                data = client.recv(size)
                count = 0
                while data:
                    bytes_file += data
                    data = client.recv(size)
                    count += 1
                    print(count, data)
                
                # write the file on the server
                try:
                    write_file(file_name, bytes_file)
                    print("[+] File writen successfuly")
                except:
                    print("[-] Error while writing file")

            else:
                # printing data
                print("msg :",data.decode())
                # echo back response to server
                client.send(data)

# Exception when the server is closed by keybord exception
except KeyboardInterrupt:	
    print("\n[!] Keybord Interruption : closing socket")	
    close_socket(client, s)

# Exception when the remote host closes the connection
except ConnectionResetError:
    print("[!] Connection aborted by remote host : closing socket")
    close_socket(client, s)

# Other exception
"""except:
    print("[-] Error : closing socket")
    close_socket(client, s)"""