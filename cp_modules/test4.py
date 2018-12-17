#!/usr/bin/env python
import requests
import multiprocessing
from multiprocessing import Manager,Process, Queue, current_process, freeze_support
import os
from bs4 import BeautifulSoup
import time
import numpy as np
import sys

NUM_WORKERS = 4 #multiprocessing.cpu_count()

done_queue = Queue() # This is messages from the child processes for parent
process_queue = Queue() # This is the domains to process
master_queue = Queue()
ignore_queue = Queue()

manager = Manager()
master_dict = manager.dict()
website=''

def scraper(process_queue, done_queue,master_queue,master):
    if time.time()-master[7]>5:
        master_queue.put('STOP')

    for domain in iter(process_queue.get, 'STOP'):
        print(multiprocessing.current_process().name)
        if len(domain)>0:
            print('Getting '+domain)
            result = get_listing(domain)
            master[4].append(domain)
            if result != None and len(result)>0:
                for link in result:
                    if not link in master[1]:
                        if link.startswith('/') and not link.startswith('//'):
                            link = domain+link
                        master[1].append(link)
            a = master[1]
            b = master[2]                
            diff=(difference(a,b))
            for url in diff:
                if not url in master[2]:
                    cat, link = parse(url)
                    if cat == 'link':
                        # if link.startswith('/'):
                        #     url=domain+link
                        master[3].append(link)
                        master_queue.put(link) #process_queue
                        master[7] = time.time()
                    elif cat == 'http':
                        master[6].append(link)
                    elif cat == 'mail':
                        master[5].append(link)
                    elif cat == 'None':
                        master[2].append(link)
                master[2].append(url)

def get_listing(url):
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
    global last
    procs=[]
    for i in range(NUM_WORKERS):
        p = Process(target=scraper, args=(process_queue, done_queue,master_queue,master))
        procs.append(p)
        p.start()
        
    while valid(master[1],master[2])>0 and (time.time()-master[7])<2:
        #print(time.time()-master[7])
        for domain in iter(master_queue.get, 'STOP'):
            process_queue.put(domain)

    for p in procs:
        p.join()

    print('Big success')
    master[4]=list(set(master[4]))
    master[5]=list(set(master[5]))
    master[6]=list(set(master[6]))
    print('Found links:')
    print(master[4])
    print('Found mail:')
    print(master[5])
    print('Found external links:')
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
    # time
    master_dict[7] = time.time()

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