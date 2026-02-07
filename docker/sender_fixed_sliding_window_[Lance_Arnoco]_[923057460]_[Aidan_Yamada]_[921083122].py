import socket

PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
EXPECTED_SEQ_ID = 0

#Data that has been sent but has not received ACK Back from Receiver
SENT_DATA = {}
#SEQ ID Acks that were returned
ACK_RECEVID = {}





udp_ip = "127.0.0.1" # Local Host
udp_port = 5050 
print(f"Starting the UDP Client to send to {udp_ip}:{udp_port}")

# Creating a UDP Socket
# What is a socket?
# Application layer endpoint connecting to the Transport layer
socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4, UDP

message = "Hello, UDP Server!"
# Encoding the Message
encoded_message = message.encode()

# Sending the Message to the Server
socket_client.sendto(encoded_message, (udp_ip, udp_port))
print(f"Sent message: {message} to {udp_ip}:{udp_port}")
