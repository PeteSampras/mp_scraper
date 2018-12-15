#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
from time import sleep
from multiprocessing import Pool,Manager

# NUM_WORKERS = 4
website = 'https://www.devleague.com'

manager = Manager()
start_list = manager.list()
done_list = manager.list()
start_list.append(website)

def get_listing(url):
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    html = None
    links = None
    r = requests.get(url, timeout=10)

    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        listing_section = soup.findAll('a', href=True)
        links = [link['href'].strip() for link in listing_section]
    return links

search = get_listing(website)

def parse(links):
    #links=list(set(links)) # get uniques
    if not links.startswith('//'):
        if links != '/' and links !='#' and '/' in links:
            if website in links:
                link = links.replace(website,'')
            # if links.startswith('/'):
            #     link = website+links
                return link
            return links


def add_to_queue(domain):
    process_queue.put(domain)

def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]



while len(diff(start_list,done_list))>0:
    with Pool(10) as p:
        print(start_list)
        # global start_list
        # global done_list
        records = p.map(parse, start_list)
        records=list(set(records))
        print(records)
        for each in records:
            if each != None:
                if not each in start_list and not each in done_list:
                    if each.startswith('/'):
                        each = website+each
                        start_list.append(each)


# get uniques


if len(done_list) > 0:
    for each in done_list:
        if each != None:
            print(each)
    # with open('data_parallel.csv', 'a+') as f:
    #     f.write('\n'.join(records))
manager = Manager()
# done_queue = Queue() # This is messages from the child processes for parent
# process_queue = Queue() # This is the domains to process

# def scraper(input_Q, output_Q):
#     for domain in iter(input_Q.get, 'STOP'):
#         if not domain in list(output_Q):


# def add_to_queue():


# def main():
#     for i in range(NUM_WORKERS):
#         Process(target=scraper, args=(process_queue, done_queue)).start()
#         #Process(target=process_done_queue, args=(done_queue,)).start()
#     process_queue.put(website)


# if __name__=='__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("Keyboard interrupted")
#     except Exception as e:
#         print(e)
#     finally:
#         print('Finished')
#         os._exit(0)

# def diff(first, second):
#         second = set(second)
#         return [item for item in first if item not in second]