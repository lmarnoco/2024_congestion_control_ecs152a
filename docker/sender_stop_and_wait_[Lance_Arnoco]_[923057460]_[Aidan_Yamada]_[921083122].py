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
src_port = 4500

dst_port = 5001

socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4, UDP

#Convert Mp3 to Byte File

def parse_message(): 
    file_path = 'file.mp3'
    with open(file_path, 'rb') as file:
            file.seek(MESSAGE_SIZE * EXPECTED_SEQ_ID)
            # 
            # mp3_byte = mp3_byte.to_bytes(MESSAGE_SIZE)
            # mp3_byte.insert(0, seq_bytes)
            encoded_message = file.read(MESSAGE_SIZE)
            if not encoded_message:
                 return None
            
            seq_bytes = EXPECTED_SEQ_ID.to_bytes(SEQ_ID_SIZE, byteorder='big')
            message_bytes = seq_bytes + encoded_message
            return message_bytes


#Creates Final+ACK to send back to receiever

def create_FINACK(seq_id, message):
    return int.to_bytes(seq_id, SEQ_ID_SIZE, signed=True, byteorder='big') + message.encode()



with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    #Bind Socket to IP and Port
    udp_socket.bind((HOST, src_port))
    udp_socket.settimeout(1)

    #If received Correct Ack and Send FINACK Increment Expected_SEQ_ID (Else will just resend message)

    while True:
        try:
            data, address = udp_socket.recvfrom(PACKET_SIZE)

            ack_id = data[:SEQ_ID_SIZE]

            seq_ack = int.from_bytes(ack_id, byteorder='big')
        
            if seq_ack == EXPECTED_SEQ_ID:
                EXPECTED_SEQ_ID += 1
                if parse_message() is None:
                    udp_socket.sendto(create_FINACK(EXPECTED_SEQ_ID, "==FINACK=="), (HOST, dst_port))
                    #Done with sending
                    break


        except socket.timeout:
            #Get Message
            message = parse_message()
            #Put Message into Socket and Send
            udp_socket.sendto(message, (HOST, dst_port))
            print(f"Sent message: {EXPECTED_SEQ_ID} to {src_port}:{dst_port}") 






    




