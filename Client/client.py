"""
    client.py - Connect to an SSL server

    CSCI 3403
    Authors: Matt Niemiec and Abigail Fernandes
    Number of lines of code in solution: 117
        (Feel free to use more or less, this
        is provided as a sanity check)

    Put your team members' names:



"""

import socket
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA

iv = "G4XO4L\X<J;MPPLD"

host = "localhost"
port = 10001

# A helper function that you may find useful for AES encryption
def pad_message(message):
    return message + " "*((16-len(message))%16)


# TODO: Generate a random AES key
def generate_key():
    return Random.get_random_bytes(16)


# TODO: Takes an AES session key and encrypts it using the server's
# TODO: public key and returns the value
def encrypt_handshake(session_key):
    message = session_key

    key = RSA.importKey(open('ssh.txt.pub').read(), 'timppfrsa1234')
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(message)
    return ciphertext


# TODO: Encrypts the message using AES. Same as server function
def encrypt_message(message, session_key):
    cipher = AES.new(session_key, AES.MODE_CFB, iv.encode("utf8"))
    ciphertext = cipher.encrypt(message.encode("utf8"))
    return ciphertext


# TODO: Decrypts the message using AES. Same as server function
def decrypt_message(message, session_key):
    cipher = AES.new(session_key, AES.MODE_CFB, iv.encode("utf8"))
    plaintext = cipher.decrypt(message)
    return plaintext.decode("utf8")


# Sends a message over TCP
def send_message(sock, message):
    sock.sendall(message)


# Receive a message from TCP
def receive_message(sock):
    data = sock.recv(1024)
    return data


def main():
    user = input("What's your username? ")
    password = input("What's your password? ")

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (host, port)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:
        # Message that we need to send
        message = user + ' ' + password

        # TODO: Generate random AES key
        session_key = generate_key()

        # TODO: Encrypt the session key using server's public key
        encrypted_session_key = encrypt_handshake(session_key)
        # TODO: Initiate handshake
        send_message(sock, encrypted_session_key)

        # Listen for okay from server (why is this necessary?)
        if receive_message(sock).decode() != "okay":
            print("Couldn't connect to server")
            exit(0)

        # TODO: Encrypt message and send to server
        send_message(sock, encrypt_message(message, session_key))

        # TODO: Receive and decrypt response from server and print
        response = receive_message(sock)
        decrytped_response = decrypt_message(response, session_key)
        print(decrytped_response)


    finally:
        print('closing socket')
        sock.close()


if __name__ in "__main__":
    main()
