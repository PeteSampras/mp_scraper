import configparser
import os
import sys
from cp_modules.utility import colorize
from cp_modules.multiproc import jobs,multProc,scrape,start_queue,done_queue,worker
from multiprocessing import Process, Queue, freeze_support
import time

config_file="domains.ini"
config = configparser.ConfigParser()            # setup
NUMBER_OF_PROCESSES = 4    # global cpu define

def mainmenu():
    d = None
    options = ['','Add domain','Start processing queue','Stop processing queue','Display logs']
    msg = ''    
    while d == None:
        print (colorize('\nM A I N   M E N U','pink'))
        print ('1. %s' % options[1])
        print ('2. %s' % options[2])
        print ('3. %s' % options[3])
        print ('4. %s' % options[4])
        print ('q. Quit')
        option = input ('Select an option: ')
        if option.lower () == 'q':
            sys.exit ()
        elif option == '1':
            msg = options[1]    
            d = add_domain_name()
        elif option == '2':
            msg =  options[2]    
            d = start_processing()
        elif option == '3':
            msg =  options[3]    
            d = stop_processing()
        elif option == '4':
            msg =  options[4]   
            d = display_logs()
        else:
            print (colorize('Invalid selection!','warning'))
    return msg, d

def start_processing():
    p = None
    while p == None:
        print (colorize('\nS U B  M E N U','pink'))
        print ('1. Process known domains')
        print ('b. Back')
        print ('q. Quit')
        option = input ('Select an option: ')
        if option.lower () == 'q':
            sys.exit ()
        elif option.lower () == 'b':
            mainmenu ()
            return
        elif option == '1':
            global start_queue
            global done_queue
            config.read(config_file)                        # read file
            print('hi')
            for each_section in config.sections():
                if each_section=='Domains':
                    for (each_key,each_val) in config.items(each_section):
                        #freeze_support()
                        #this=(scrape,each_key)
                        print(each_key)
                        start_queue.put(each_key)
            process()
            mainmenu()
            return
        else:
            print (colorize('Invalid selection!','warning'))
    mainmenu()
    return p

def process():
    print('process')
    freeze_support()
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(start_queue, done_queue))

    for each_section in config.sections():
        if each_section=='Domains':
            for (each_key,each_val) in config.items(each_section):
                start_queue.put(each_key)
    
    for message in iter(done_queue.get, 'STOP'):
        print(message)


def stop_processing():
    p = None
    while p == None:
        print (colorize('\nS U B  M E N U','pink'))
        print ('1. Add domain')
        print ('b. Back')
        print ('q. Quit')
        option = input ('Select an option: ')
        if option.lower () == 'q':
            sys.exit ()
        elif option.lower () == 'b':
            mainmenu ()
            return
        elif option == '1':
            p = 'Do something'
        else:
            print ('Invalid selection!')
    return p

def display_logs():
    p = None
    while p == None:
        print (colorize('\nS U B  M E N U','pink'))
        print ('1. Add domain')
        print ('b. Back')
        print ('q. Quit')
        option = input ('Select an option: ')
        if option.lower () == 'q':
            sys.exit ()
        elif option.lower () == 'b':
            mainmenu ()
            return
        elif option == '1':
            p = 'Do something'
        else:
            print ('Invalid selection!')
    return p

def add_domain_name():
    p=None
    config.read(config_file)                        # read file
    print(colorize('\r\nKnown domains:','pink'))
    for each_section in config.sections():
        if each_section=='Domains':
            for (each_key,each_val) in config.items(each_section):
                print(colorize(each_key, 'green'))
    domain = input ('Domain to add: ')
    for each_section in config.sections():
        if each_section=='Domains':
            for (each_key,each_val) in config.items(each_section):
                if each_key==domain:
                    p=True
                    this = "%s is already added as a domain." % domain
                    print(colorize(this,'fail'))
                    mainmenu()
    config.set('Domains',domain,'html')
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    print(colorize(domain + ' added.', 'green'))
    return p