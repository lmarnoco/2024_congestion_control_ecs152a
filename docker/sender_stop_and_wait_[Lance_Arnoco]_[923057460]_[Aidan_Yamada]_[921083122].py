import socket

PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
EXPECTED_SEQ_ID = 0

#Data that has been sent but has not received ACK Back from Receiver
SENT_DATA = {}
#SEQ ID Acks that were returned
ACK_RECEVID = {}
#ACKS Sent Back to Rec
FINACKS_SENT = {}

#Convert Binary File to Mp3


#Creates Final+ACK to send back to receiever

def create_FINACK(seq_id, message):
    return int.to_bytes(seq_id, SEQ_ID_SIZE, signed=True, byteorder='big') + message.encode()


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    pass




