'''Receiver Module for packet reception'''

import sys
import const
from gen_packet import Packet


class Receiver:
    '''Receiver Class to implement packet receiving functionalities'''

    def __init__(self, name: int, channel_to_receiver):
        self.seq_no = 0             # need to be synced with sender
        self.name = name
        self.sender_list = {}
        self.packet_type = {'data': 0, 'ack': 1}
        self.channel_to_receiver = channel_to_receiver
        self.recent_ack = Packet(1, 0, "Acknowledgement Packet", self.name, 0).make_pkt()

    def open_file(self, filepath: str):
        '''Opens file in append mode and returns file-pointer-object'''
        try: fptr = open(filepath, 'a+', encoding='utf-8')
        except FileNotFoundError as file_err:
            print("\nEXCEPTION Caught : " + str(file_err))
            sys.exit("File {} Not Found!".format(filepath))
        return fptr

    def decode_sender(self, pkt):
        '''Decodes source-address from the received packets'''
        sender_address = pkt.decode_src_address()
        return sender_address

    def initiate_receiver_process(self):
        '''Receives & decodes packets from sender, extracts data and writes it to output file'''
        while True:
            pkt = self.channel_to_receiver.recv()
            sender = self.decode_sender(pkt)

            if sender not in self.sender_list.keys():
                self.sender_list[sender] = const.outfile_path + 'output' + str(sender)

            outfile = self.sender_list[sender]
            file = self.open_file(outfile)
            data = pkt.extract_data()
            file.write(data)
            file.close()
            print("RECEIVER-{} -->> PACKET RECEIVED".format(self.name+1))
