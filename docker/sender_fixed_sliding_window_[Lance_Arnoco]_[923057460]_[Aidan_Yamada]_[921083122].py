import socket

PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
EXPECTED_SEQ_ID = 0

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

win_size = 0


def send_pkt(payload, seq_id):
    # Convert seq_id into bits
    seq_bytes = seq_id.to_bytes(SEQ_ID_SIZE, 'big')

    # Makes sure the data read from mp3 is the right size
    # payload = payload.to_bytes(MESSAGE_SIZE)

    # Puts sequence id infront of data
    pkt = seq_bytes + payload

    print("SENDING")
    socket_client.sendto(pkt, (udp_ip, dst_port))
    #print(f"Sent message: {pkt} to {udp_ip}:{dst_port}") 


udp_ip = "127.0.0.1" # Local Host
udp_port = 50505 # DELETE
print(f"Starting the UDP Client to send to {udp_ip}:{dst_port}")

# Creating a UDP Socket
# 5216
# Application layer endpoint connecting to the Transport layer
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_client:

    socket_client.settimeout(5.0)

    #Convert Mp3 to Byte File
    file_path = 'file.mp3'

    # I AS CHECKING HOW BIG THE FILE WAS
    count = 0

    timeouts = 0
    with open(file_path, 'rb') as file:
        while True:
            if win_size < MAX_WINDOW_SIZE:
                mp3_byte = file.read(1020)

                if not mp3_byte:
                    break
                else:
                    send_pkt(mp3_byte, id)
                    win_size += 1
                    id += 1
            
            try:
                print("REMOVE PKT ", win_size, id)
                # receive the packet
                packet, client = socket_client.recvfrom(PACKET_SIZE)
                print("STUCK")
                
                # get the message id
                seq_id, message = packet[:SEQ_ID_SIZE], packet[SEQ_ID_SIZE:]
                
                print("GETTING DATA")
                # check if finack message
                if message == b'==FINACK==':
                    break
                
                # if the message id is -1, we have received all the packets
                seq_id = int.from_bytes(seq_id, signed=True, byteorder='big')
                
                # keep track of received sequences
                RECEIVED_DATA[seq_id] = message
                
                print("RECIEVING ACK")
                # check if sequence id is same as expected and move forward
                if seq_id <= EXPECTED_SEQ_ID and len(RECEIVED_DATA[seq_id]) > 0:
                    while EXPECTED_SEQ_ID in RECEIVED_DATA:
                        EXPECTED_SEQ_ID += 1
                    win_size -= 1
            except socket.timeout:
                timeouts += 1
