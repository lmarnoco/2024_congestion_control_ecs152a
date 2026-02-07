import socket

PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
EXPECTED_SEQ_ID = 0

#Data that has been sent but has not received ACK Back from Receiver
SENT_DATA = {}
#SEQ ID Acks that were returned
ACK_RECEVID = {}

src_port = 5050

dst_port = 5001



udp_ip = "127.0.0.1" # Local Host
udp_port = 50505 # DELETE
print(f"Starting the UDP Client to send to {udp_ip}:{dst_port}")

# Creating a UDP Socket
# What is a socket?
# Application layer endpoint connecting to the Transport layer
socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4, UDP


#Convert Mp3 to Byte File
file_path = 'file.mp3'
with open(file_path, 'rb') as file:
    while True:
        mp3_byte = file.read(1020)

        if not mp3_byte:
            break
        else:
            seq_bytes = EXPECTED_SEQ_ID.to_bytes(SEQ_ID_SIZE)
            mp3_byte = mp3_byte.to_bytes(MESSAGE_SIZE)
            mp3_byte.insert(0, seq_bytes)
            encoded_message = mp3_byte.encode()
            socket_client.sendto(encoded_message, (udp_ip, dst_port))
            print(f"Sent message: {mp3_byte} to {udp_ip}:{dst_port}") 
            EXPECTED_SEQ_ID += 1   


message = "Hello, UDP Server!"
# Encoding the Message
encoded_message = message.encode()

# Sending the Message to the Server
socket_client.sendto(encoded_message, (udp_ip, dst_port))
print(f"Sent message: {message} to {udp_ip}:{dst_port}")
