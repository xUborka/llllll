""" Endpoints for the translation API """
from urllib.parse import urlparse
from flask import request, Blueprint, render_template, redirect
from translate.database import DatabaseWrapper
from translate.utils import check_sitemap, parse_all_pages

translate_page = Blueprint('translate', __name__, template_folder='templates')


@translate_page.route('/translate', methods=['GET'])
def translate_main_page():
    ''' Landing Page '''
    return render_template('translate.html')


@translate_page.route('/progress/<url>', methods=['GET'])
def progress_check(url: str):
    database_reference = DatabaseWrapper()
    status = database_reference.get_status(url)
    print(status)
    resp = {'status_message': '',
            'message': status['currently_analyzed'],
            'status': int(100*status['finished_parsing'] / status['num_pages'])
            }
    return resp


@translate_page.route('/page-analysis/<url>', methods=['GET'])
def page_analysis(url: str):
    ''' Remove cached results, run analysis and update cache'''
    database_reference = DatabaseWrapper()
    database_reference.remove_status_document(url)
    return redirect(f'/url_parser/{url}')


@translate_page.route('/page-word-analysis/<url>', methods=['GET'])
def page_word_analysis(url: str):
    ''' Remove cached results, run analysis and update cache'''
    database_reference = DatabaseWrapper()
    database_reference.remove_pages_document(url)
    return redirect(f'/analyze/{url}')


@translate_page.route('/url_parser', methods=['POST'])
def form_post_endpoint():
    ''' Endpoint for posting the url '''
    url = urlparse(request.form['url'])
    if url.netloc != '':
        url = url.netloc
    else:
        url = url.path
    return redirect(f'/url_parser/{url}')


@translate_page.route('/url_parser/<url>', methods=['GET'])
def form_post_url(url: str):
    database_reference = DatabaseWrapper()
    resp = database_reference.get_status(url)
    site_data = {'url': url, 'pages': [], 'cached': False}
    if resp is None:
        # If there is no entry in the database --> Collect pages
        sites = check_sitemap(url)
        database_reference.set_status(
            url, {'url': url, 'pages': sites, 'num_pages': len(sites)})
    else:
        # If there is an entry --> Check if pages are collected already
        if 'pages' in resp and len(resp['pages']) > 0:
            site_data['cached'] = True
            sites = resp['pages']
        else:
            sites = check_sitemap(url)
            database_reference.set_status(
                url, {'url': url, 'pages': sites, 'num_pages': len(sites)})

    site_data['pages'] = sites
    return render_template('pages_overview.html', data=site_data)


@translate_page.route('/analyze/<url>', methods=['GET'])
def analyze_pages(url: str):
    database_reference = DatabaseWrapper()
    status_resp = database_reference.get_status(url)
    pages_resp = database_reference.get_pages(url)
    pages = status_resp['pages']
    page_data = {'url': url, 'num_pages': len(
        pages), 'sum_words': 0, 'cached': False}
    if pages_resp is None:
        result = parse_all_pages(database_reference, url, pages)
        page_data['sum_words'] = sum([len(i['words'])
                                     for i in result.values()])
    else:
        if len(pages_resp) > 0:
            page_data['sum_words'] = sum(
                [len(i['words']) for i in pages_resp.values()])
            page_data['cached'] = True
        else:
            result = parse_all_pages(database_reference, url, pages)
            page_data['sum_words'] = sum(
                [len(i['words']) for i in result.values()])
    return render_template('analysis_overview.html', data=page_data)
