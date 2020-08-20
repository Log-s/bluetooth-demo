import socket, os.path

def read_file(path):
    """
    reads a file, and converts its to bytes, to allow bluetooth transfer
    § param :
        - path : file path
    § return :
        - name        : file name
        - byte_file   : file as a bytes
    """
    # reading file as bytes
    with open(path, "rb") as f:
        byte_file = f.read()
    # getting file name
    name = path.split("/")[-1]
    return name,byte_file


# server MAC address
serverMACAddress = '40:e2:30:df:3d:62'
# server port
port = 1

# creating socket and connecting it to the server
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
print("[+] Connected to server, ready to transfer data")
print()
print(  "[!]    ===     ===     ===     ===     ===     ===\n\
        Enter any text to print it on the server's screen\n\
        Commands :\n\
            - quit : quits the program and closes the socket\n\
            - file : runs the file transfer routine\n\
        ===     ===     ===     ===     ===     ===")

# Main loop for message transfering
while True:
    # get text data or instruction
    text = input("Enter msg : ")

    if text == "quit": # quits the program
        break

    elif text == "file": # runs the file transfer routine
        s.send(str.encode("FILE_TRANSFER"))
        path = input("Enter path to file : ")
        # cheking if the file exists
        while not os.path.isfile(path):
            path = input("Enter path to file : ")
        # reads the file
        file_name, file_byte = read_file(path)
        s.send(str.encode(file_name))
        s.sendall(file_byte)

    else: # Send text data
        s.send(str.encode(text))

# Closing socket
s.close()