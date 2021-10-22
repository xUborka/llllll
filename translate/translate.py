from flask import redirect, request, Blueprint, jsonify, render_template
from usp.tree import sitemap_tree_for_homepage
import requests
from bs4 import BeautifulSoup

translate_page = Blueprint('translate', __name__, template_folder='templates')

@translate_page.route('/translate', methods=['GET'])
def translate_main_page():
    return render_template('translate.html')

@translate_page.route('/url_parser', methods=['POST'])
def form_post_endpoint():
    url = request.form['url']
    return redirect('/single_page_parser/' + url)

@translate_page.route('/single_page_parser/<url>')
def single_page_parser(url):
    if url == 'test':
        return render_template('dummy_template.html', data={'b': ['a', 'b', 'c']})

    tree = sitemap_tree_for_homepage('http://' + url)
    urls = {}
    summ = 0
    for page in tree.all_pages():
        urls[page.url] = None
        resp = requests.get(page.url)
        print(resp.encoding)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, features="html.parser")
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            text = text.strip('\t')
            text = text.strip('\n')
            urls[page.url] = text.split()
            summ += len(urls[page.url])
            print(urls[page.url])
    print(summ)
    return render_template('dummy_template.html', data=urls)
