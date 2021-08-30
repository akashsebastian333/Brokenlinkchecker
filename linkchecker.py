from bs4 import BeautifulSoup as bs
import requests,sys,re
from urllib.parse import urlparse, urljoin

def start():
    script_links(url)
    href(url)
    status(all_urls)

def status(al):
    print("\n\nprinting status")
    for a in al:
        try:
            code = session.get(a)
            print(a , code.status_code)
        except requests.exceptions.ConnectionError:
            print(a, "\033[1;31;40m check this \033[0m")

def checkurl(url):
    checkurl = urlparse(url)
    return bool(checkurl.netloc) and bool(checkurl.scheme)

def href(url):
    tags = ['a','base','link','base','area']
    for a_tag in soup.findAll(tags):
        href = a_tag.attrs.get('href')
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        if samedomain not in href:
            if href not in all_urls:
                all_urls.append(href)
    return urls


def script_links(url):
    tags = ['script','img','style','audio','embed','iframe','source','track','video']
    for script_tag in soup.find_all(tags):
        src = script_tag.attrs.get('src')
        if src == "" or src is None:
            continue
        if checkurl(src) == False:
            continue
        src = urljoin(url, src)
        if samedomain not in src:
            if src not in all_urls:
                all_urls.append(src)
    return urls


if __name__ == "__main__":
    try:
        while(True):
            url = input("Enter the url to scan: ")
            #url = sys.argv[1]

            if checkurl(url)==True:
                all_urls = []
                urls = []
                session = requests.Session()
                session.headers["User-Agent"] = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
                html = session.get(url).content
                soup = bs(html, "html.parser")
                samedomain = urlparse(url).netloc
                start()
                break
            else:
                print("Not valid url please check the protocol")
    except KeyboardInterrupt:
            pass
