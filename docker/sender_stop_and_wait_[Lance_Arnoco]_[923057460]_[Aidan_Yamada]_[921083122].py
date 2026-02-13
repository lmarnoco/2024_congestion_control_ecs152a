import socket

#1024 Bytes - 8192 Bits (Personal Note: MP3 has a lot more bytes than that)
PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
#Use as Iterator
EXPECTED_SEQ_ID = 0

#Data that has been sent but has not received ACK Back from Receiver
SENT_DATA = {}
#SEQ ID Acks that were returned
ACK_RECEVID = {}
#ACKS Sent Back to Rec
FINACKS_EXPECTED_TO_SEND = {}

#IP Address and Host
HOST = '0.0.0.0'
#Possibly change
udp_ip = 4500

dst_port = 5001

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



#Creates Final+ACK to send back to receiever

def create_FINACK(seq_id, message):
    return int.to_bytes(seq_id, SEQ_ID_SIZE, signed=True, byteorder='big') + message.encode()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    #Bind Socket to IP and Port
    udp_socket.bind(HOST, Src_PORT)

    #If received Correct Ack and Send FINACK Increment Expected_SEQ_ID (Else will just resend message)

    #Get Message
    message = parse_message

    #Put Message into Socket

    #Send Socket





    




