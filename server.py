import socket, os.path, time



## ---------- functions ---------- ##


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



def recvall(socket, timeout=2):
    """
    receives all the data sent before the timeout is reached
    (timer is reset every time data is received)
    $ param :
        - socket    : socket used for receiving the data
        - timeout   : timeout value in seconds (default : 2s)
    $ return :
        - data      : the total data received
    """
    # variables
    data_part = b""
    data = b""
    begin = time.time()

    # set to non blocking to avoid wainting on recv() instruction
    socket.setblocking(0)

    # receiving loop
    while True:
        # handle timeout
        if time.time() - begin > timeout:
            break

        # handle receiving data
        else:
            try:
                data_part = socket.recv(1024)
                if data_part:
                    # reset timer
                    begin = time.time()
                    data += data_part
                else:
                    # sleep to avoid traffic overflow
                    time.sleep(0.1)
            except:
                pass
    
    # set socket back to blocking
    socket.setblocking(1)
    return data



def decrypt_data(data):
    pass


## ---------- ---- ---------- ##



## ---------- main ---------- ##


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

        if data: # if data is not None
            if data.decode() == "FILE_TRANSFER": # if the file transfer protocol is enganged
                print("[+] File transfer started")
                # gets the file name
                file_name = client.recv(size).decode()
                print("[!] Transfering :",file_name)
                # gets the file
                bytes_file = recvall(client)
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
except:
    print("[-] Error : closing socket")
    close_socket(client, s)

## ---------- ---- ---------- ##