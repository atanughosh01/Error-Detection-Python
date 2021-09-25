'''Sender Module for data sending'''

import sys
import time
import const
import threading
from datetime import datetime


class Sender:
    '''Sender Class to implement data sending functionalities'''

    def __init__(self, name, walsh_code, sender_to_channel):
        self.name               = name
        self.sender_to_channel  = sender_to_channel # a pipe
        self.walsh_code         = walsh_code        # tuple containg walshCode


    def open_file(self, sender):
        '''Opens file in read mode and returns file-pointer-object'''
        try:
            file_name = const.input_file_path + 'input' + str(sender+1) + '.txt'
            fptr = open(file_name, 'r', encoding='utf-8')
        except FileNotFoundError as fnfe:
            curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(curr_datetime + " EXCEPTION CAUGHT : {}".format(str(fnfe)))
            sys.exit("File with name {} is not found!".format(file_name))
        return fptr


    def send_data(self):
        '''Sends data continuously'''
        file = self.open_file(self.name)
        byte = file.read(const.default_data_packet_size)
        while byte:
            data = '{0:08b}'.format(ord(byte))      # send the data bits of byte
            for i in range(len(data)):
                data_to_send = []
                data_bit = int(data[i])
                if data_bit == 0: data_bit = -1
                for j in self.walsh_code:
                    data_to_send.append(j * data_bit)
                ##############################################
                self.sender_to_channel.send(data_to_send)
                ##############################################
                print("(Sender{}:) data bit send {}".format(self.name+1, data_bit))
                curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                with open('textfiles/report.txt', 'a+', encoding='utf-8') as rep_file:
                    rep_file.write(curr_datetime + " SENDER-{}    ||  DATA BIT SEND {}".format(self.name+1, data_bit) + '\n')
                ##############################################
                time.sleep(1)
                ##############################################
            byte = file.read(const.default_data_packet_size)

        print("(Sender{}:) DONE SENDING...".format(self.name + 1))
        curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open('textfiles/report.txt', 'a+', encoding='utf-8') as rep_file:
            rep_file.write(curr_datetime + " SENDER-{}    ||  DONE SENDING...".format(self.name+1) + '\n')


    def start_sender(self):
        '''Initializes and terminates the sending thread'''
        sender_thread = threading.Thread(name="Sender-Thread" + str(self.name+1), target=self.send_data)     
        sender_thread.start()
        sender_thread.join()
