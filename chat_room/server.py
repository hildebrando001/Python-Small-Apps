import threading
import socket

host = '127.0.0.1' # localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating socket with TCP connection

server.bind((host, port)) # bind server to the host and port
server.listen() # Put server in the listenning mode for incoming connections

clients   = [] # Every new connected client will be put in the client list
nicknames = [] # All nicknames for the connected clients


def broadcast(message):    # Definning broadcast methood
    for client in clients:  # This method send message to every connected client
        client.send(message)


def handle(client):   # Definning method to handle the client connection
    while True:       # This method receive each message and send it to all clients, including the sender
        try:          # Try to receive a message from the client
            message = client.recv(1024) # Client receive 1024 bytes
            broadcast(message)          # Broadcast all the other clients
        except:       # If we have some error while receiving the message or while broadcast
            index = clients.index(client) # Fidding where is this client in the list
            clients.remove(client) # Cut the connection with this particular client and remove from the list
            client.close()

            nickname = nicknames[index] # The nickname index will be the same of client index
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():  # Definning receiving method
    while True:
        client, address = server.accept() # Running accept method all the time and returning client and address
        print(f"Connected with {str(address)}") # Message on the server shell when new connection comes

        client.send('NICK'.encode('ascii')) # Send the message "NICK" to the client
        nickname = client.recv(1024).decode('ascii') # Reveves Nickname informed by the client
        nicknames.append(nickname) # Send nickname to the nicknames list
        clients.append(client) # Send client to the clients list

        print(f'Nickname of the client in {nickname}!') # Informs user your nickname
        broadcast(f'{nickname} joined the chat!'.encode('ascii')) # Tell to everybody that someone new enjoined to the chat
        client.send('Connected to the server'.encode('ascii')) # Send a message to the new client

        thread = threading.Thread(target=handle, args=(client,)) # Load the "threading" to the handle function
        thread.start()

print('Server is linstening...')
receive()