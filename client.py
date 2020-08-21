import socket, os.path, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad



## ---------- functions ---------- ##


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


def print_help():
    """
    prints the help message with the available commands
    """
    print()
    print(  "[!]\n\
        Enter any text to print it on the server's screen\n\
        Commands :\n\
            - /help : prints this help\n\
            - /quit : quits the program and closes the socket\n\
            - /file : runs the file transfer routine")



def encrypt_data(data):
    """
    Encrypts data to be transferd to server in a secure way
    § param :
        - data : bytes to be encrypted
    § return :
        - encrypted_data
    """
    # create object to encrypt data with a key that needs to be the same on the server side
    crypter = AES.new("SuperSecretKey!!", AES.MODE_ECB)
    # pads the data to match a multiple of 16 bytes, encrypts the data using AES
    # and encodes it to b64 to shrink the data
    encrypted_data = base64.b64encode(crypter.encrypt(pad(data,16)))
    return encrypted_data


# ---------- ---- ---------- ##



## ---------- main ---------- ##


# server MAC address
serverMACAddress = '40:e2:30:df:3d:62'
# server port
port = 1

# creating socket and connecting it to the server
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
print("[+] Connected to server, ready to transfer data")
print_help()

# Main loop for message transfering
while True:
    # get text data or instruction
    text = input("> ")

    if text == "/quit": # quits the program
        break

    elif text == "/help": # prints the help screen
        print_help()

    elif text == "/file": # runs the file transfer routine
        s.send(encrypt_data(str.encode("FILE_TRANSFER")))
        path = input("Enter path to file : ")
        # cheking if the file exists
        while not os.path.isfile(path):
            print("[-] Error : file doesn't exists")
            path = input("Enter path to file : ")
        # reads the file
        file_name, file_byte = read_file(path)
        s.send(encrypt_data(str.encode(file_name)))
        s.sendall(encrypt_data(file_byte))

    else: # Send text data
        s.send(encrypt_data(str.encode(text)))

# Closing socket
s.close()

## ---------- ---- ---------- ##