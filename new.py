#!/usr/bin/env python
import argparse
from cp_modules.configure import configuration
import configparser
import sys
from cp_modules.utility import colorize,header
import requests
import multiprocessing
from multiprocessing import Process, Queue, current_process, freeze_support, Manager
import os
import logging
import time
import re
from bs4 import BeautifulSoup
import urllib.request

#from queue import Queue
#from cp_modules.option_menus import menu_options,mainmenu,start_processing#,stop_processing

config_file="domains.ini"
config = configparser.ConfigParser()            # setup
NUM_WORKERS = 4
log_name='gets_log.log'

done_queue = Queue() # This is messages from the child processes for parent
process_queue = Queue() # This is the domains to process

manager = Manager()
done_list = manager.list()

def logger(data):
    logging.basicConfig(level=logging.INFO,filename=log_name)
    logging.info(str(data))
    
def rescrape():
    file = open(log_name,'r')
    for line in file:
        line=line.replace("INFO:root:[","")
        line=line.replace("]",'')
        line=line.replace(", '",'')
        new_line = line.split("\'")
        site=new_line[1]
        print(site)
        for each in new_line:
            if each==new_line[1]:
                continue
            if len(each)>1:
                if not "://" in each:
                    each=site+each
                scrape(each)
    file.close()


def scrape(this_url):
    data = []
    data.append(this_url)
    result = requests.get(this_url)
    if result.status_code == 200:
        soup = BeautifulSoup(result.text,'html.parser')
        for link in soup.findAll('a',href=True):
            if "/" in link.get('href'):
                data.append(link.get('href'))
        #print(str(data) + ' ##2')
        logger(data)
    else:
        print('Failed: {} - {}' .format(result.text,result.status_code))



def scraper(input, output):
  # output.put("{} starting".format(current_process().name))
    for domain in iter(input.get, 'STOP'):
        scrape(domain)
        output.put("{}: Domain {} retrieved".format(current_process().name, domain))
    

def add_to_queue(domain):
    process_queue.put(domain)

def process_done_queue(input):
    for message in iter(input.get, 'STOP'):
        print(message)

def main():
    for i in range(NUM_WORKERS):
        Process(target=scraper, args=(process_queue, done_queue)).start()
    Process(target=process_done_queue, args=(done_queue,)).start()
    mainmenu()

def menu_options(selection):
    if selection==None:
        options = ['MAIN MENU','Add domain','Start processing queue','Stop processing queue','Display logs','Spider crawl logged sites']
        print (colorize(options[0],'pink'))
        for i in range(1,6):
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
            elif option=='5':
                d = rescrape()
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

def stop_processing():
    menu_options('Confirm cancellation')
    p = None
    while p == None:
        option = input ('Select an option: ')
        if option.lower() == 'q':
            os._exit(0)
        elif option.lower() == 'b':
            p = mainmenu()
        elif option == '1':
            print('Stopping all processes')
            process_queue.put('STOP')
            done_queue.put('STOP')
            p = mainmenu()
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

def display_logs():
    file = open(log_name,'r')
    for line in file:
        line=line.replace("INFO:root:[","")
        line=line.replace("]",'')
        line=line.replace(", '",'')
        new_line = line.split('\'')
        for each in new_line:
            print(each)
    file.close()
    menu_options(None)
    return











if __name__=='__main__':
    parser = argparse.ArgumentParser(prog='Multiprocess',
                                     add_help=True,
                                     description='A multi-process scraper')
    configuration(parser)

    # make a sweet intro to impress Jason
    print(colorize(header, 'blue'))
    print(colorize('version 1.0\n', 'green'))

    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupted")
    except Exception as e:
        print(e)
    finally:
        print('Finished')
        os._exit(0)

