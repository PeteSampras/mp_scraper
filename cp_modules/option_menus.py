import configparser
import os
import sys
from cp_modules.utility import colorize
#from cp_modules.multiproc import jobs,multProc,scrape,start_queue,done_queue,worker
#from multiprocessing import Process, Queue, freeze_support
#import time
#from new import process_queue,done_queue,add_to_queue


config_file="domains.ini"
config = configparser.ConfigParser()            # setup
NUMBER_OF_PROCESSES = 4    # global cpu define

def menu_options(selection):
    if selection==None:
        options = ['MAIN MENU','Add domain','Start processing queue','Stop processing queue','Display logs']
        for i in range(1,5):
            print(str(i) + '. '+options[i])
    else:
        options = ['SUB MENU']
        print (colorize(options[0],'pink'))
        print('1. %s' % selection)
        print('b. Back')
    print ('q. Quit\n')

def mainmenu():
    while True:
        menu_options(None)
        d = None
        while d == None:
            option = input ('Select an option: ')
            if option.lower () == 'q':
                os._exit(0)
            elif option == '1':
                d = add_domain_name()
            elif option == '2':
                d = start_processing()
            elif option == '3':
                d = stop_processing()
            elif option == '4':
                d = display_logs()
            else:
                print (colorize('Invalid selection!','warning'))

def start_processing():
    menu_options("Process known domains")
    p = None
    while p == None:
        option = input ('Select an option: ')
        if option.lower () == 'q':
            os._exit(0)
        elif option.lower () == 'b':
            p = mainmenu()
        elif option == '1':
            global process_queue
            global done_queue
            config.read(config_file)                        # read file
            for each_section in config.sections():
                if each_section=='Domains':
                    for (each_key,each_val) in config.items(each_section):
                        if "http" in each_key:
                            add_to_queue(each_key)
                        else:
                            this = 'https://'
                            if not 'www' in each_key:
                                this = this + 'www.' + each_key
                            else:
                                this = this + each_key
                            add_to_queue(this)
                            print(this)
            p=mainmenu()
        else:
            print (colorize('Invalid selection!','warning'))
            p=mainmenu()
    p = mainmenu()
    return p


# def stop_processing():
#     p = None
#     while p == None:
#         print (colorize('\nS U B  M E N U','pink'))
#         print ('1. Add domain')
#         print ('b. Back')
#         print ('q. Quit')
#         option = input ('Select an option: ')
#         if option.lower () == 'q':
#             sys.exit ()
#         elif option.lower () == 'b':
#             mainmenu ()
#             return
#         elif option == '1':
#             p = 'Do something'
#         else:
#             print ('Invalid selection!')
#     return p

# def display_logs():
#     p = None
#     while p == None:
#         print (colorize('\nS U B  M E N U','pink'))
#         print ('1. Add domain')
#         print ('b. Back')
#         print ('q. Quit')
#         option = input ('Select an option: ')
#         if option.lower () == 'q':
#             sys.exit ()
#         elif option.lower () == 'b':
#             mainmenu ()
#             return
#         elif option == '1':
#             p = 'Do something'
#         else:
#             print ('Invalid selection!')
#     return p

# def add_domain_name():
#     p=None
#     config.read(config_file)                        # read file
#     print(colorize('\r\nKnown domains:','pink'))
#     for each_section in config.sections():
#         if each_section=='Domains':
#             for (each_key,each_val) in config.items(each_section):
#                 print(colorize(each_key, 'green'))
#     domain = input ('Domain to add: ')
#     for each_section in config.sections():
#         if each_section=='Domains':
#             for (each_key,each_val) in config.items(each_section):
#                 if each_key==domain:
#                     p=True
#                     this = "%s is already added as a domain." % domain
#                     print(colorize(this,'fail'))
#                     mainmenu()
#     config.set('Domains',domain,'html')
#     with open(config_file, 'w') as configfile:
#         config.write(configfile)
#     print(colorize(domain + ' added.', 'green'))
#     return p