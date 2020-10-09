import socket
import threading

nickname = input('Choose a nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Defining the socket
client.connect(('127.0.0.1',55555)) # Connect the host and the port

def receive():  # Receive all the time data from the server
    while True:
        try:
            message = client.recv(1024).decode('ascii') # client receve message from the server
            if message == 'NICK': # NICK is the keyword for sending the nickname. NICk comes from the server
                client.send(nickname.encode('ascii'))
            else:
                print(message) # if a NICK doesn't comes or any other keyword, it is a message from the server. All we need to do is just print
        except:
            print("An error occurred!")
            client.close()
            break

def write(): # Keep the treading running for all the messages we have to send.
    while True:
        message = f'{nickname}: {input("")}' # Always running a new input function
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()