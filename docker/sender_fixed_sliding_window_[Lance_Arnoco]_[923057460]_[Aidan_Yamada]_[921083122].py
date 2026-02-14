import socket
import time
import math

PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
EXPECTED_SEQ_ID = 1020

MAX_WINDOW_SIZE = 100

#Data that has been sent but has not received ACK Back from Receiver
SENT_DATA = {}
#SEQ ID Acks that were returned
ACK_RECEVID = {}

pkt_start = {}
pkt_end = {}

src_port = 5050
dst_port = 5001

start = 0
end = start + MAX_WINDOW_SIZE - 1

last = False
done = False


def set_up():
    global end
    for i in range(start, end + 1):
        payload = parse_message(i)

        if not payload:
            last = True
            end = i - 1
            break
        else:
            SENT_DATA[i] = payload


def parse_message(index): 
    file_path = 'file.mp3'
    with open(file_path, 'rb') as file:
        file.seek(index * MESSAGE_SIZE)

        mp3_byte = file.read(MESSAGE_SIZE)

        return mp3_byte

def send_pkt(i):
    # Convert seq_id into bits
    seq_bytes = (i * MESSAGE_SIZE).to_bytes(SEQ_ID_SIZE, 'big')

    pkt = seq_bytes + SENT_DATA[i]
    
    if i not in pkt_start:
        pkt_start[i] = time.time()

    socket_client.sendto(pkt, (udp_ip, dst_port))


def sendFinAck():
    seq_bytes = ((end + 1) * MESSAGE_SIZE).to_bytes(SEQ_ID_SIZE, 'big')

    pkt = seq_bytes + b'==FINACK=='

    socket_client.sendto(pkt, (udp_ip, dst_port))
                    


udp_ip = "127.0.0.1" # Local Host

# Creating a UDP Socket
# Application layer endpoint connecting to the Transport layer
start_time = time.time()
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_client:

    socket_client.settimeout(5)

    set_up()

    while True:
        for i in range(start, end + 1):
            send_pkt(i)
        
        timeouts = 0
        count = 0
        while timeouts == 0:
            if last and start > end:
                done = True
                break
            try:
                # receive the packet
                packet, client = socket_client.recvfrom(PACKET_SIZE)
                count += 1
                
                # get the message id
                id, message = packet[:SEQ_ID_SIZE], packet[SEQ_ID_SIZE:]

                # if the message id is -1, we have received all the packets
                seq_id = int.from_bytes(id, signed=True, byteorder='big')

                if seq_id >= EXPECTED_SEQ_ID:
                    ACK_RECEVID[EXPECTED_SEQ_ID] = message

                    if (math.ceil(EXPECTED_SEQ_ID/MESSAGE_SIZE) - 1) not in pkt_end:
                        pkt_end[math.ceil(EXPECTED_SEQ_ID/MESSAGE_SIZE) - 1] = time.time()

                    start += 1
                    end += 1

                    payload = parse_message(end)

                    if not payload:
                        last = True
                        end = end - 1
                    else:
                        SENT_DATA[end] = payload
                        send_pkt(end)

                    if start > end:
                        break

                    EXPECTED_SEQ_ID += len(SENT_DATA[math.ceil(EXPECTED_SEQ_ID/MESSAGE_SIZE)])

            except socket.timeout:
                timeouts += 1
        
        if done:
            break

    sendFinAck()

    end_time = time.time()

    print()
    # Throughput Calcualtion
    elapsed_time = end_time - start_time

    throughput = EXPECTED_SEQ_ID / elapsed_time
    print(round(throughput, 7), ",")

    # Packet Delay Calculation
    total_diff = 0
    for i in range(len(pkt_start)):
        total_diff += pkt_end[i] - pkt_start[i]

    pkt_delay = total_diff / len(pkt_start)
    print(round(pkt_delay, 7), ",")

    # Performance Calculation
    performance = 0.3 * throughput / 1000 + 0.7 /pkt_delay
    print(round(performance, 7), ",")

    print()
