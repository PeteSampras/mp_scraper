from multiprocessing import Manager, Pool, Queue
import os
import requests
from bs4 import BeautifulSoup
from time import sleep

done_queue = Queue() # This is messages from the child processes for parent
process_queue = Queue() # This is the domains to process

website = 'https://www.devleague.com'

manager = Manager()
start_list = manager.list()
master_list = manager.list()
ignore_list=manager.list()
done_list = manager.list()
mail_list=manager.list()
http_list=manager.list()
diff_list = manager.list()
master_list.append(website)
start_list.append(website)



def get_listing(url,masterlist,donelist):
    print('url: {} , master {}, done {}, ' .format(url, len(masterlist), len(donelist)))
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    html = None
    links = None
    donelist.append(url)
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
                masterlist.append(link)
        except Exception as e:
            print(e)


def parse(link,mail,http):
    if link.startswith('//'):
        link = link[2:]
        if not link in http:
            http.append(link)
        return None
    if not link.startswith('//'):
        if link != '/' and not link.startswith('#') and '/' in link:
            if website in link:
                link = link.replace(website,'')
                return link
            if 'http' in link.lower() or 'www' in link.lower():
                http_list.append(link)
                return None
            elif 'mailto:' in link.lower():
                mail_list.append(link)
                return None
            else:
                return link
    return None

def do_stuff(args):
    print(os.getpid())
    # difflist,startlist,donelist,httplist,maillist,masterlist
    difflist=args[0]
    startlist=args[1]
    donelist=args[2]
    httplist=args[3]
    maillist=args[4]
    masterlist=args[5]
    ignorelist=args[6]
    this = diff(startlist,donelist)
    for url in this:
        get_urls = get_listing(url,masterlist,donelist)
        if get_urls!=None:
            for each_url in get_urls:
                masterlist.append(each_url)
    update_master(masterlist,ignorelist,startlist,donelist,maillist,httplist)
    print('Done:'+str(donelist)+ ' start: '+ str(startlist))
    donelist=list(set(donelist))
    startlist=list(set(startlist))
    difflist=diff(startlist,donelist)
    difflist=list(set(difflist))

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def update_master(master,ignore,start,done,mail,http):
    this = diff(master,ignore)
    this = diff(this,done)
    this = diff(this,start)
    #print('Master:'+str(this))
    for url in this:
        if parse(url,mail,http) != None:
            start.append(url)
        else:
            ignore.append(url)
    #print("Start: "+str(start))
    #print("Ignore: " + str(ignore))




def main():
    global start_list
    global done_list
    global diff_list
    global master_list
    global mail_list
    global http_list
    global ignore_list
    pool = Pool(processes=10)
    while len(diff(start_list,done_list))>0:
        #print('Main: ' + str(start_list))
        master_list=list(set(master_list))
        ignore_list=list(set(ignore_list))
        start_list=list(set(start_list))
        diff_list=diff(start_list,done_list)
        diff_list=list(set(diff_list))
        print('Diff: '+str(diff_list))
        pool.map(do_stuff, [(diff_list,start_list,done_list,http_list,mail_list,master_list,ignore_list)])
    pool.close()
    done()

def done():
    global start_list
    global done_list
    global diff_list
    global master_list
    global mail_list
    global http_list
    print(done_list)
    print(mail_list)
    print(http_list)

    #print(list(set(start_list)))
    print('Big Success')
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