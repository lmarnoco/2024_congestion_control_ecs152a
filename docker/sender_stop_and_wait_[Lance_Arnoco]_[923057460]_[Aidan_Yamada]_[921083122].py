import socket
import sys
import time


#1024 Bytes - 8192 Bits (Personal Note: MP3 has a lot more bytes than that)
PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE

#IP Address and Host
HOST = "127.0.0.1"
#Possibly change
src_port = 4500

dst_port = 5001

real_avg_throughput = 0

real_avg_packet_delay = 0

real_avg_performance = 0

sum_throughput = 0

sum_pd = 0

sum_p = 0

socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4, UDP


#Actual 
EXPECTED_SEQ_ID = 0

total_per_packet = 0

total_packets = 0


#Convert Mp3 to Byte File

def parse_message(): 
    global EXPECTED_SEQ_ID
    file_path = 'file.mp3'
    with open(file_path, 'rb') as file:
            file.seek(EXPECTED_SEQ_ID)
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
    start_time_throughput = time.time()
    udp_socket.settimeout(2.5)

    #If received Correct Ack and Send FINACK Increment Expected_SEQ_ID (Else will just resend message)

    while True:
        message = parse_message()
        #Put Message into Socket and Send
        if message is None:
            
            udp_socket.sendto(create_FINACK(EXPECTED_SEQ_ID, "==FINACK=="), (HOST, dst_port))

            end_time_throughput = (time.time() - start_time_throughput)
            sum_throughput += end_time_throughput
            avg_packet_delay = total_per_packet / total_packets
            sum_pd += avg_packet_delay
            performance = ((((0.3)* end_time_throughput)/1000) + (0.7 / avg_packet_delay))
            sum_p += performance
            break

        start_time_per_packet = time.time()
        udp_socket.sendto(message, (HOST, dst_port))

        #print(f"Sent message: {EXPECTED_SEQ_ID} to {src_port}:{dst_port}") 

        try:

            data, address = udp_socket.recvfrom(PACKET_SIZE)

            ack_id = data[:SEQ_ID_SIZE]

            seq_ack = int.from_bytes(ack_id, byteorder='big')
            
            payload_size = len(message) - SEQ_ID_SIZE
            if seq_ack == EXPECTED_SEQ_ID + payload_size:
                EXPECTED_SEQ_ID += MESSAGE_SIZE
                end_time_perpack = time.time() - start_time_per_packet
                total_per_packet += end_time_perpack
                total_packets += 1


        except socket.timeout:
            #Put Message into Socket and Send
            udp_socket.sendto(message, (HOST, dst_port))
            #print(f"Sent message: {EXPECTED_SEQ_ID} to {src_port}:{dst_port}")
    
#1 Trial

print(f"{sum_throughput:.7f}, \n")
print(f"{avg_packet_delay:.7f}, \n")
print(f"{performance:.7f} \n")

