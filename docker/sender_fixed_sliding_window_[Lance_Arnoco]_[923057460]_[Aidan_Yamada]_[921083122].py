import socket

PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
EXPECTED_SEQ_ID = 1020

MAX_WINDOW_SIZE = 100

#Data that has been sent but has not received ACK Back from Receiver
SENT_DATA = {}
#SEQ ID Acks that were returned
ACK_RECEVID = {}

RECEIVED_DATA = {}

src_port = 5050
dst_port = 5001

# Starting number for sequence id
id = 0

start = 0
end = start + MAX_WINDOW_SIZE - 1


def send_pkt(start, end):
    for i in range(start, end + 1):
        # Convert seq_id into bits
        seq_bytes = (i * MESSAGE_SIZE).to_bytes(SEQ_ID_SIZE, 'big')

        # Makes sure the data read from mp3 is the right size
        # payload = payload.to_bytes(MESSAGE_SIZE)

        # Puts sequence id infront of data
        pkt = seq_bytes + SENT_DATA[i]

        print("SENDING WITH ID", i)
        socket_client.sendto(pkt, (udp_ip, dst_port))
        #print(f"Sent message: {pkt} to {udp_ip}:{dst_port}") 


udp_ip = "127.0.0.1" # Local Host
udp_port = 50505 # DELETE
print(f"Starting the UDP Client to send to {udp_ip}:{dst_port}")

# Creating a UDP Socket
# 5216
# Application layer endpoint connecting to the Transport layer
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_client:

    socket_client.settimeout(5)

    #Convert Mp3 to Byte File
    file_path = 'file.mp3'

    finish = False

    with open(file_path, 'rb') as file:
        while True:
            for i in range(start, end + 1):
                if not i in SENT_DATA:
                    mp3_byte = file.read(1020)

                    if not mp3_byte:
                        finish = True
                        SENT_DATA[i] = b'==FINACK=='
                        end = i
                        break
                    else:
                        SENT_DATA[i] = mp3_byte

            send_pkt(start, end)
            
            timeouts = 0
            count = 0
            while timeouts == 0:
                try:
                    print("REMOVE PKT", start, end)
                    # receive the packet
                    packet, client = socket_client.recvfrom(PACKET_SIZE)

                    if not packet:
                        print("IM HERE\n\n\n\n\n\n\n\n\n\n\n\n\n")
                        break
                    
                    # get the message id
                    id, message = packet[:SEQ_ID_SIZE], packet[SEQ_ID_SIZE:]
                    
                    #print("GETTING DATA")
                    # check if finack message
                    if message == b'==FINACK==':
                        break
                    
                    # if the message id is -1, we have received all the packets
                    seq_id = int.from_bytes(id, signed=True, byteorder='big')
                    print("RECIEVED SEQ ID", seq_id)
                    print("EXPECTED SEQ ID", EXPECTED_SEQ_ID)

                    if seq_id >= EXPECTED_SEQ_ID:
                        # diff = seq_id - EXPECTED_SEQ_ID
                        # for i in range(0, diff):
                        #     ACK_RECEVID[EXPECTED_SEQ_ID + (MESSAGE_SIZE * i)] = message
                        ACK_RECEVID[EXPECTED_SEQ_ID] = message

                        EXPECTED_SEQ_ID += MESSAGE_SIZE
                        start += 1
                        end += 1


                    #ACK_RECEVID[seq_id] = message
                    
                    # print("RECIEVING ACK")
                    # print(seq_id <= EXPECTED_SEQ_ID, len(ACK_RECEVID[seq_id]))
                    # print(EXPECTED_SEQ_ID in ACK_RECEVID)
                    # # check if sequence id is same as expected and move forward
                    # if len(ACK_RECEVID[seq_id]) > 0:
                    #     while EXPECTED_SEQ_ID in ACK_RECEVID:
                    #         print("LOOPING")
                    #         EXPECTED_SEQ_ID += MESSAGE_SIZE
                    #         start += 1
                    #         end += 1
                        
                except socket.timeout:
                    print("\n\n\n\n\n\nTIMED OUT")
                    #EXPECTED_SEQ_ID = start * MESSAGE_SIZE
                    timeouts += 1
            
            if finish:
                print("IM FREEEEEEEEEEEEEEE")
                break

        print("EXIT")
