''' Utils for webpage parsing '''
from multiprocessing import Pool
from usp.tree import sitemap_tree_for_homepage
import requests
from bs4 import BeautifulSoup
from translate.database import DatabaseWrapper
import time

def check_sitemap(url: str) -> list:
    ''' Uses usp.tree to find the sitemap '''
    if url == 'test':
        return ['test_1', 'test_2', 'test_3']
    tree = sitemap_tree_for_homepage(format_url(url))
    urls = []
    for page in tree.all_pages():
        urls.append(page.url)
    return urls


def format_url(url: str) -> str:
    ''' usp.tree requires http:// at start '''
    if url.startswith('http'):
        return url
    return 'http://' + url

def parse_all_pages(db_ref: DatabaseWrapper, root_url: str, url_list: list) -> dict:
    db_ref.update_status(root_url, {'finished_parsing' : 0, 'currently_analyzed': root_url})
    pages = {}
    pool = Pool(processes=10)
    finished_counter = 0
    start = time.time()
    for res in pool.imap(parse_page, url_list):
        pages[res['url']] = res
        finished_counter += 1
        db_ref.set_page(root_url, res['url'], res)
        c_time = time.time()
        if c_time - start > 1.5:
            start = time.time()
            db_ref.update_status(root_url, {'finished_parsing' : finished_counter, 'currently_analyzed': res['url']})
    return pages


def parse_page(url: str) -> dict:
    ''' Parses a single page '''
    resp = requests.get(url)
    result = {'url': url, 'status_code': resp.status_code, 'words': []}
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, features="html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        text = text.strip('\t')
        text = text.strip('\n')
        result['words'] = text.split()
        # print(result)
    return result
