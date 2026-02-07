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
Src_PORT = 4500

Dst_PORT = 5001


#Convert Mp3 to Byte File
file_path = 'file.mp3'
with open(file_path, 'rb') as file:
    mp3_byte = file.read()


#Creates Final+ACK to send back to receiever

def create_FINACK(seq_id, message):
    return int.to_bytes(seq_id, SEQ_ID_SIZE, signed=True, byteorder='big') + message.encode()


def parse_message():
    #Parse bits like [Packet Size * Expected ID]
    message = int.to_bytes(EXPECTED_SEQ_ID) + mp3_byte[EXPECTED_SEQ_ID * 1020].encode('utf-8')
    
    #Converts message to a string that can later be returned as integers
    return message



with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    #Bind Socket to IP and Port
    udp_socket.bind(HOST, Src_PORT)

    #If received Correct Ack and Send FINACK Increment Expected_SEQ_ID (Else will just resend message)

    #Get Message
    message = parse_message

    #Put Message into Socket

    #Send Socket





    




