import multiprocessing
from multiprocessing import Process, Queue, current_process, freeze_support
import urllib.request
import os
from bs4 import BeautifulSoup

start_queue = Queue()
done_queue = Queue()
jobs=[]

# def worker(input, output):
#     print('worker')
#     jobs.append(input)
#     for func, args in iter(input.get,'STOP'):
#         print('%s - %s' % func,args)
#         result = run_this(func, args)
#         output.put(result)
#     return

def worker(start_queue,done_queue):
    pass


def run_this(func, args):
    result = func(*args)
    print('run this')
    return '%s says that %s%s = %s' % \
        (current_process().name, func.__name__, args, result)

# Creates a function for multiprocessing. Several things at once.
def multProc(targetin, item):
    freeze_support()
    p = multiprocessing.Process(target=targetin, args=(item,))
    # q.put(p)
    # jobs.append(p)
    p.start()
    p.join()
    return

def scrape(site):
    print(site)
    pass