#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
from time import sleep
from multiprocessing import Pool


def get_listing(url):
    html = None
    links = None
    r = requests.get(url, timeout=10)

    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        listing_section = soup.findAll('a', href=True)
        links = [link['href'].strip() for link in listing_section]
    return links

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
    
    #links = [link in links if not link.startswith('//')]
    #return links

# parse a single item to get information
def parse2(url):
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    r = requests.get(url, timeout=10) # header=headers
    sleep(2)

    info = []
    title_text = '-'
    location_text = '-'
    price_text = '-'
    title_text = '-'
    images = '-'
    description_text = '-'

    if r.status_code == 200:
        print('Processing..' + url)
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find('h1')
        if title is not None:
            title_text = title.text.strip()

        location = soup.find('strong', {'class': 'c2b small'})
        if location is not None:
            location_text = location.text.strip()

        price = soup.select('div > .xxxx-large')
        if price is not None:
            price_text = price[0].text.strip('Rs').replace(',', '')

        images = soup.select('#bigGallery > li > a')
        img = [image['href'].strip() for image in images]
        images = '^'.join(img)

        description = soup.select('#textContent > p')
        if description is not None:
            description_text = description[0].text.strip()

        info.append(url)
        info.append(title_text)
        info.append(location_text)
        info.append(price_text)
        info.append(images)

    return ','.join(info)

website = 'https://www.devleague.com'
search = get_listing(website)

with Pool(10) as p:
    records = p.map(parse, search)

# get uniques
records=list(set(records))

if len(records) > 0:
    for each in records:
        if each != None:
            print(each)
    # with open('data_parallel.csv', 'a+') as f:
    #     f.write('\n'.join(records))