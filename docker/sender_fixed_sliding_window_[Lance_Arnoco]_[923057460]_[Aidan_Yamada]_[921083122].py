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

# TESTING THING
total = 0
total_pkts = 0

def parse_message(index): 
    file_path = 'file.mp3'
    with open(file_path, 'rb') as file:
            file.seek(index * MESSAGE_SIZE)

            mp3_byte = file.read(MESSAGE_SIZE)

            return mp3_byte

def send_pkt(i):
    global total_pkts
    # Convert seq_id into bits
    seq_bytes = (i * MESSAGE_SIZE).to_bytes(SEQ_ID_SIZE, 'big')

    # Puts sequence id infront of data
    pkt = seq_bytes + SENT_DATA[i]

    # print("SENDING WITH ID", i)
    if i not in pkt_start:
        pkt_start[i] = time.time()
    total_pkts += 1
    socket_client.sendto(pkt, (udp_ip, dst_port))


def sendFinAck():
    print("FINACK SEQ", (end + 1))
    seq_bytes = ((end + 1) * MESSAGE_SIZE).to_bytes(SEQ_ID_SIZE, 'big')

    pkt = seq_bytes + b'==FINACK=='

    socket_client.sendto(pkt, (udp_ip, dst_port))
                    


udp_ip = "127.0.0.1" # Local Host
udp_port = 50505 # DELETE
print(f"Starting the UDP Client to send to {udp_ip}:{dst_port}")

# Creating a UDP Socket
# 5216
# Application layer endpoint connecting to the Transport layer
start_time = time.time()
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_client:

    socket_client.settimeout(5)

    while True:
        for i in range(start, end + 1):
            if not i in SENT_DATA:
                payload = parse_message(i)

                if not payload:
                    last = True
                    end = i - 1
                    break
                else:
                    SENT_DATA[i] = payload
            print(i)
            send_pkt(i)
        
        timeouts = 0
        count = 0
        while timeouts == 0:
            if last and start == end:
                done = True
                break
            # if start == end:
            #     if last:
            #         # sendFinAck()
            #         finPkt = ((end + 1) * MESSAGE_SIZE).to_bytes(SEQ_ID_SIZE, 'big')

            #         # print("SENDING WITH ID", i)
            #         socket_client.sendto(finPkt, (udp_ip, dst_port))

            #         packet, client = socket_client.recvfrom(PACKET_SIZE)

            #         id, message = packet[:SEQ_ID_SIZE], packet[SEQ_ID_SIZE:]
                
            #         #print("GETTING DATA")
            #         # check if finack message
            #         if message == b'fin':
            #             done = True
            #     break
            try:
                print("REMOVE PKT", start, end, count)
                # receive the packet
                packet, client = socket_client.recvfrom(PACKET_SIZE)
                count += 1
                
                # get the message id
                id, message = packet[:SEQ_ID_SIZE], packet[SEQ_ID_SIZE:]
                
                #print("GETTING DATA")
                # check if finack message
                # if message == b'fin':
                #     finish = True

                # if the message id is -1, we have received all the packets
                seq_id = int.from_bytes(id, signed=True, byteorder='big')
                print("RECIEVED SEQ ID", seq_id)
                print("EXPECTED SEQ ID", EXPECTED_SEQ_ID)

                if seq_id >= EXPECTED_SEQ_ID:
                    ACK_RECEVID[EXPECTED_SEQ_ID] = message

                    if (math.ceil(EXPECTED_SEQ_ID/MESSAGE_SIZE) - 1) not in pkt_end:
                        # print(math.ceil(EXPECTED_SEQ_ID/MESSAGE_SIZE))
                        # print(len(pkt_start))
                        # print(len(pkt_end))
                        pkt_end[math.ceil(EXPECTED_SEQ_ID/MESSAGE_SIZE) - 1] = time.time()

                    start += 1
                    end += 1

                    if start > end:
                        break

                    EXPECTED_SEQ_ID += len(SENT_DATA[math.ceil(EXPECTED_SEQ_ID/MESSAGE_SIZE)])

                    payload = parse_message(end)

                    if not payload:
                        last = True
                        end = end - 1
                    else:
                        #print(payload)
                        SENT_DATA[end] = payload
                        send_pkt(end)


                    
            except socket.timeout:
                print("\n\n\n\n\n\n\n\n\nTIMEOUT")
                timeouts += 1
                total += 1
                print("TOTAL TIMEOUTS", total)
        
        if done:
            print("IM FREEEEEEEEEEEEEEE")
            break

    sendFinAck()
    # finPkt = ((end + 1) * MESSAGE_SIZE).to_bytes(SEQ_ID_SIZE, 'big')

    # # print("SENDING WITH ID", i)
    # socket_client.sendto(finPkt, (udp_ip, dst_port))

    # packet, client = socket_client.recvfrom(PACKET_SIZE)

    # id, message = packet[:SEQ_ID_SIZE], packet[SEQ_ID_SIZE:]

    # print("EXIT")

    # print("ACKS RECEIEVED:", len(ACK_RECEVID))
    # print("TOTAL_PKTS:", len(SENT_DATA))
    # print(total_pkts)
    # print("DATA", len(SENT_DATA[5215]))

    end_time = time.time()

    elapsed_time = end_time - start_time

    print("\n\n\nTIME TAKEN IS", elapsed_time)

    throughput = EXPECTED_SEQ_ID / elapsed_time
    print("Throughput:", round(throughput, 7))

    total_diff = 0
    # print(len(pkt_start), len(pkt_end))
    for i in range(len(pkt_start) - 1):
        total_diff += pkt_end[i] - pkt_start[i]

    pkt_delay = total_diff / len(pkt_start)
    print("Per-packet Delay:", round(pkt_delay, 7))

    performance = 0.3 * throughput / 1000 + 0.7 /pkt_delay
    print("Performance:", round(performance, 7))

    # print("TOTAL TIMEOUTS", total)
