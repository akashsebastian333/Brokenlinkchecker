from bs4 import BeautifulSoup as bs
import requests,sys,re,ssl,argparse
from urllib.parse import urlparse, urljoin

def process_tags(tags):
    for tag in soup.find_all(tags):
        src = tag.attrs.get('src') or tag.attrs.get('href')
        if src == "" or src is None:
            continue
        src = urljoin(url, src)
        if samedomain not in src:
            if src not in all_urls:
                all_urls.append(src)
                try:
                    status = session.get(src).status_code
                    if status == 200:
                        print(f'\033[1;32;40m{src} {status}\033[0m')
                    else:
                        print(f'\033[1;31;40m{src} {status}\033[0m')
                except requests.exceptions.SSLError:
                    print(f'\033[1;31;40m{src} SSL error\033[0m')
                except requests.exceptions.ConnectionError:
                    print(f'\033[1;31;40m{src} Connection error\033[0m')
    return all_urls

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan webpage')
    parser.add_argument('-d', '--domain', help='the domain name to scan')
    args = parser.parse_args()

    url = args.domain
    if url:
        parsed_url = urlparse(url)
        if parsed_url.netloc and parsed_url.scheme:
            all_urls = []
            session = requests.Session()
            session.headers["User-Agent"] = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
            try:
                html = session.get(url).content
                soup = bs(html, "html.parser")
                samedomain = parsed_url.netloc
                process_tags(['a', 'base', 'link', 'base', 'area'])
                process_tags(['script', 'img', 'style', 'audio', 'embed', 'iframe', 'source', 'track', 'video'])
            except ssl.CertificateError:
                print(f'\033[1;31;40m{url} SSL certificate error\033[0m')
            except requests.exceptions.ConnectionError:
                print(f'\033[1;31;40m{url} Connection error\033[0m')
        else:
            print("Not valid url please check the protocol")
    else:
        parser.print_usage()
