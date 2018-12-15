from multiprocessing import Manager, Pool, Queue
import os
import requests
from bs4 import BeautifulSoup
from time import sleep

done_queue = Queue() # This is messages from the child processes for parent
process_queue = Queue() # This is the domains to process

website = 'https://www.devleague.com'

manager = Manager()
shared_list = manager.list()
master_list = manager.list()
done_list = manager.list()
mail_list=manager.list()
http_list=manager.list()
diff_list = manager.list()
shared_list.append(website)
i=0

def get_listing(url):
    global done_list
    global shared_list
    global mail_list
    global http_list
    if url in done_list:
        return None
    print(done_list)
    print('shared: {} , done {}, mail {}, http {}: ' .format(len(shared_list), len(done_list), len(mail_list), len(http_list)))
    # print(url)
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    html = None
    links = None
    if url.startswith('/'):
        url = website+url
    r = requests.get(url, timeout=10)         

    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        listing_section = soup.findAll('a', href=True)
        links = [link['href'].strip() for link in listing_section]

        #global done_list
        try:
            for link in links:
                if not link in done_list and not link in shared_list:
                    this = parse(link)
                    if this != None and this != website:
                        new_url=url+link
                        shared_list.append(new_url)
            shared_list=list(set(shared_list))
            done_list=list(set(done_list))
        except Exception as e:
            print(e)
            return None
    return links

def parse(links):
    global done_list
    global shared_list
    global mail_list
    global http_list
    #links=list(set(links)) # get uniques
    if links.startswith('//') or links == website:
        http_list.append(links.replace('//',''))
        return None
    if not links.startswith('//'):
        if links != '/' and not links.startswith('#') and '/' in links:
            if website in links:
                link = links.replace(website,'')
                return link
            if 'http' in links:
                http_list.append(links)
                return None
            elif 'mailto:' in links:
                mail_list.append(links)
                return None
            else:
                return links
    return None

def do_stuff(url_list):
    #print(url_list)
    global done_list
    if url_list==website and website in done_list:
        return
    global shared_list
    this = diff(shared_list,done_list)
    for url in this:
        get_urls = get_listing(url)
        if get_urls!=None:
            for each_url in get_urls:
                if each_url!=None:
                    if not url in done_list:
                        done_list.append(url)
                        shared_list.append(each_url)


    done_list=list(set(done_list))
    shared_list=list(set(shared_list))
    #print(len(diff(shared_list,done_list)))

def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]


def main():
    global shared_list
    global done_list
    global diff_list
    global master_list
    global mail_list
    global http_list
    global i
    pool = Pool(processes=10)
    while len(diff(shared_list,master_list))>0:
        if len(shared_list) < 1 and i > 3:
            done()
            os._exit(0)
        i = i + 1
        if len(mail_list)>0:
            http_list=list(set(http_list))
        if len(mail_list)>0:
            mail_list=list(set(mail_list))
        shared_list=list(set(shared_list))
        diff_list=diff(shared_list,done_list)
        diff_list=list(set(diff_list))
        pool.map(do_stuff, diff_list)

def done():
    global shared_list
    global done_list
    global diff_list
    global master_list
    global mail_list
    global http_list
    print(done_list)
    print(mail_list)
    print(http_list)
    pool.close()
    #print(list(set(shared_list)))
    print('Finished')
    os._exit(0)

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupted")
    except Exception as e:
        print(e)
    finally:
        print('Finished')
        os._exit(0)