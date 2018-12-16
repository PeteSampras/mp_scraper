#!/usr/bin/env python
import requests
import multiprocessing
from multiprocessing import Manager,Process, Queue, current_process, freeze_support
import os
from bs4 import BeautifulSoup
import time
import numpy as np
import sys

NUM_WORKERS = 4

done_queue = Queue() # This is messages from the child processes for parent
process_queue = Queue() # This is the domains to process
master_queue = Queue()
ignore_queue = Queue()

manager = Manager()
master_dict = manager.dict()
website=''

start = time.time()

def scraper(process_queue, done_queue,master_queue,master):
    #print(master)
    #print("{} starting".format(current_process().name))
    #print(master[1])
    for domain in iter(process_queue.get, 'STOP'):
        if len(domain)>0:
            print('Getting '+domain)
            result = get_listing(domain)
            done_queue.put(domain)
            master[4].append(domain)
                #print(result)
            if result != None and len(result)>0:
                    #print(result)
                for link in result:
                    if not link in master[1]:
                        master[1].append(link)
            a = master[1]
            b = master[2]                
            diff=(difference(a,b))
            print('Diff1: ' + str(len(diff)))
            for url in diff:
                if not url in master[2]:
                    cat, link = parse(url)
                    if cat == 'link':
                        master[3].append(link)
                        process_queue.put(link)
                    elif cat == 'http':
                        master[6].append(link)
                    elif cat == 'mail':
                        master[5].append(link)
                    elif cat == 'None':
                        master[2].append(link)
                master[2].append(url)


def get_listing(url):
    #print('url: {} , master {}, ' .format(url, len(masterlist)))
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    html = None
    links = url
    if url.startswith('/'):
        url = website+url
    r = requests.get(url, timeout=10)         
    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        listing_section = soup.findAll('a', href=True)
        links = [link['href'].strip() for link in listing_section]
        return links

def parse(link):
    #print('parse')
    if link == "''":
        return 'None', 'None'
    if link.startswith('//'):
        link = link[2:]
        #if not link in http:
        return 'http',link
    if link.startswith('mailto:'):
        return 'mail',link.replace('mailto:','')
    if not link.startswith('//'):
        if link != '/' and not link.startswith('#') and '/' in link:
            if website in link:
                link = link.replace(website,'')
                return 'link',link
            if 'http' in link.lower() or 'www' in link.lower():
                return 'http',link
            else:
                return 'link',link
        else:
            return 'None', 'None'
    return 'None', 'None'

def difference(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def valid(master1,master2):
    a = master1
    b = master2
    return len(difference(a,b))

def main(master):
    global start
    for i in range(NUM_WORKERS):
        p = Process(target=scraper, args=(process_queue, done_queue,master_queue,master))
        p.start()
        p.join()
    # while (time.time()-start)<2:
    #     pass
    while valid(master[1],master[2])>0:
        pass
        # and len(difference(master[3],master[4]))>0
        # master_list=list(set(master_list))
        # ignore_list=list(set(ignore_list))
    print(valid(master[1],master[2]))

    print('Big success')
    print(master[1])
    print(master[2])
    print(master[4])
    master[3]=list(set(master[3]))
    master[5]=list(set(master[5]))
    master[6]=list(set(master[6]))
    print(master[3])
    print(master[5])
    print(master[6])
        
    
if __name__ == "__main__":
    website = 'https://www.devleague.com'
    #master_queue.put(Link(website))
    # master
    master_dict[1] = manager.list()
    # ignore
    master_dict[2] = manager.list()
    # process
    master_dict[3] = manager.list()
    # done
    master_dict[4] = manager.list()
    # mail
    master_dict[5] = manager.list()
    # http
    master_dict[6] = manager.list()

    master_dict[1].append(website)
    master_dict[3].append(website)
    process_queue.put(website)
    try:
        main(master_dict)
    except KeyboardInterrupt:
        print("Keyboard interrupted")
    except Exception as e:
        print(e)
    finally:
        print('Finished')
        os._exit(0)