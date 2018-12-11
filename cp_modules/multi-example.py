#!/usr/bin/env python
import requests
from multiprocessing import Process, Queue, current_process

NUM_WORKERS = 4

done_queue = Queue() # This is messages from the child processes for parent
process_queue = Queue() # This is the domains to process

def scraper(process_queue, done_queue):
  done_queue.put("{} starting".format(current_process().name))
  for domain in iter(process_queue.get, 'STOP'):
    result = requests.get(domain)
    done_queue.put("{}: Domain {} retrieved with {} bytes".format(current_process().name, domain, len(result.text)))
  # while True:
  #   message = process_queue.get()
  #   if message == 'STOP':
  #     quit()
  #   else:
  #     result = requests.get(message)
  #     done_queue.put("Domain {} retrieved with {} bytes".format(message, len(result.text)))

def main():
  domain_list = [
    'https://google.com',
    'https://sudokrew.com',
    'https://www.devleague.com',
    'https://google.com',
    'https://sudokrew.com',
    'https://www.devleague.com',
    'https://google.com',
    'https://sudokrew.com',
    'https://www.devleague.com',
    'https://google.com',
    'https://sudokrew.com',
    'https://www.devleague.com',
    'https://google.com',
    'https://sudokrew.com',
    'https://www.devleague.com',
    'https://google.com',
    'https://sudokrew.com',
    'https://www.devleague.com',
    'https://google.com',
    'https://sudokrew.com',
    'https://www.devleague.com',
    'https://google.com',
    'https://sudokrew.com',
    'https://www.devleague.com',
    'https://google.com',
    'https://sudokrew.com',
    'https://www.devleague.com',
    'https://google.com',
    'https://sudokrew.com',
    'https://www.devleague.com'
  ]
  for i in range(NUM_WORKERS):
    Process(target=scraper, args=(process_queue, done_queue)).start()

  for domain in domain_list:
    process_queue.put(domain)

  for message in iter(done_queue.get, 'STOP'):
    print(message)

    
if __name__ == "__main__":
  main()