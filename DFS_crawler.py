import sys
import time
import requests
from bs4 import BeautifulSoup
import re



visited = []
seed_url = "https://en.wikipedia.org/wiki/Tropical_cyclone"


def write_to_file(data):
    with open('DFSurls', 'w+') as f:
        for url in data:
            f.write(str(url) + "\n")
    f.close()

def get_url(current_url):
    #return a list of urls
    time.sleep(1)
    next_depth_urls = []
    handle = requests.get(current_url)

    html_raw_data =  handle.text
    soup = BeautifulSoup(html_raw_data, 'html.parser')

    # Get Body from Page
    if len(soup.find('ol', attrs={'class': 'references'}) or ()) > 1:
        soup.find('ol', attrs={'class': 'references'}).decompose()
    if len(soup.find('div', attrs={'class': 'thumb tright'}) or ()) > 1:
        soup.find('div', attrs={'class': 'thumb tright'}).decompose()
    if len(soup.find('div', attrs={'id': 'toc'}) or ()) > 1:
        soup.find('div', attrs={'id': 'toc'}).decompose()
    if len(soup.find('table', attrs={'class': 'vertical-navbox nowraplinks'}) or ()) > 1:
        soup.find('table', attrs={'class': 'vertical-navbox nowraplinks'}).decompose()
    if len(soup.find('table', attrs={'class': 'vertical-navbox nowraplinks hlist'}) or ()) > 1:
        soup.find('table', attrs={'class': 'vertical-navbox nowraplinks hlist'}).decompose()

    data = soup.find('div', attrs={'id': 'mw-content-text'})
    for urls in data.find_all('a', attrs={'href': re.compile("^/wiki")}):
        if ':' not in urls.get('href'):
            final = "https://en.wikipedia.org" + urls.get('href')
            str1= final.split('#')[0]
            str2= str1.lower()
            next_depth_urls.append(str2)

    #print(len(next_depth_urls))
    next_depth_urls.reverse()
    return next_depth_urls


def dfs_crawler(url):

    stack = []
    current_depth = 1
    visited = []
    stack.append((url,current_depth))
    s = 0

    while(len(stack) >0):
        current_data = stack.pop()
        url = current_data[0]
        depth = current_data[1]
        urll=url.lower()
        if urll not in visited:
            visited.append(urll)
        if(len(visited) > 1000):
            return visited[0:1000]
        if(depth < 7):
            for next_url in get_url(url):
                if(next_url not in visited):
                    stack.append((next_url,depth+1))
    return visited
	
	
	
def main():
    result_urls =dfs_crawler(seed_url)
    write_to_file(result_urls)



if __name__ == "__main__":
    main()
