''' main script to implement all the functionalities defined in the modules'''

import const
import threading
import multiprocessing
from sender import Sender
from channel import Channel
from receiver import Receiver


def start_simulation(technique: int):

    # write_from_sender_to_channel = []
    # read_from_sender_to_channel = []

    write_from_channel_to_sender = []
    read_from_channel_to_sender = []

    write_from_channel_to_receiver = []
    read_from_channel_to_receiver = []

    # write_from_receiver_to_channel = []
    read_from_receiver_to_channel = []


    ######################################################################################
    # Pipe() returns a tuple (of two objects) whose 1st-one can read and 2nd-one can write
    ######################################################################################
    for _ in range(const.total_sender_number):
        read_head, write_head = multiprocessing.Pipe()
        read_from_channel_to_sender.append(read_head)       # goes to sender
        write_from_channel_to_sender.append(write_head)     # goes to channel

    for _ in range(const.total_receiver_number):
        read_head, write_head = multiprocessing.Pipe()
        read_from_channel_to_receiver.append(read_head)     # goes to receiver
        write_from_channel_to_receiver.append(write_head)   # goes to channel

    read_from_sender_to_channel, write_from_sender_to_channel = multiprocessing.Pipe()


    ##################################################################################
    # making the sender list, receiver list, sender threadlist and receiver threadlist
    ##################################################################################
    sender_list = []
    receiver_list = []
    sender_threads = []
    receiver_threads = []


    ##############################################################
    # creating the channel, sender and receiver classes' instances
    ##############################################################
    channel = Channel(read_from_sender_to_channel, write_from_channel_to_sender, read_from_receiver_to_channel, write_from_channel_to_receiver)

    for i in range(const.total_sender_number):
        sender = Sender(i, 'textfiles/input/input'+str(i)+'.txt', write_from_sender_to_channel, read_from_channel_to_sender[i], technique)
        sender_list.append(sender)

    for i in range(const.total_receiver_number):
        receiver = Receiver(i, read_from_channel_to_receiver[i])
        receiver_list.append(receiver)


    ########################################################################################
    # making one channel thread, and multiple sender-receiver threads, and add them to lists
    ########################################################################################
    channel_thread = threading.Thread(target=channel.initiate_channel_process)

    for i in range(len(sender_list)):
        s = threading.Thread(target=sender_list[i].initiate_sender_process)
        sender_threads.append(s)

    for i in range(len(receiver_list)):
        r = threading.Thread(target=receiver_list[i].initiate_receiver_process)
        receiver_threads.append(r)


    #############################################################################################
    # MULTIPROCESSING STARTS HERE
    # initialise and end execution of single channel thread, and multiple sender-receiver threads
    #############################################################################################
    channel_thread.start()

    for thread in receiver_threads:
        thread.start()

    for thread in sender_threads:
        thread.start()

    for thread in sender_threads:
        thread.join()

    channel_thread.join()

    for thread in receiver_threads:
        thread.join()


    # print("**************************************************")
    # print("**************************************************")
    # print("**************************************************")
    # print("******************  END  *************************")
    # print("**************************************************")
    # print("**************************************************")
    # print("**************************************************")


if __name__ == "__main__":
    while True:
        print("------------------------------------------------------")
        print("|    Choose the CSMA technique you want to use -     |")
        print("|        1. One Persistent Method                    |")
        print("|        2. Non Persistent Method                    |")
        print("|        3. P-Persistent Methodt                     |")
        print("------------------------------------------------------")
        choice = int(input(" \nEnter your choice (1, 2 or 3): "))
        if choice == 1: ch = "One Persistent Method"
        elif choice == 2: ch = "Non Persistent Method"
        elif choice == 3: ch = "P Persistent Method"
        else: ch = "No Method Chosen!"
        print("Chosen CSMA technique is : {}".format(ch))
        start_simulation(choice)

        # print("**************************************************")
        # print("**************************************************")
        # print("**************************************************")
        # print("******************  END  *************************")
        # print("**************************************************")
        # print("**************************************************")
        # print("**************************************************")
