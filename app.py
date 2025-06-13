from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Kategorie-Codes von Amazon DE
CATEGORY_MAP = {
    'books': 'n:186606',
    'electronics': 'n:562066',
    'toys': 'n:12950651',
    'home': 'n:227937031',
    'kitchen': 'n:3045261',
    'beauty': 'n:56680031',
    'sports': 'n:1824020031',
}

@app.route('/')
def index():
    return render_template('index.html', categories=CATEGORY_MAP.keys())

@app.route('/search')
def search():
    query = request.args.get('query', '')
    category = request.args.get('category', '')
    base_url = "https://www.amazon.de/s"
    rh = 'p_85:2470955011'
    if category in CATEGORY_MAP:
        rh += ',' + CATEGORY_MAP[category]

    params = {'k': query, 'rh': rh}
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = []

    for item in soup.select('div.s-result-item'):
        title_el = item.select_one('span.a-text-normal')
        link_el = item.select_one('a.a-link-normal')
        img_el = item.select_one('img.s-image')
        if title_el and link_el and img_el:
            title = title_el.text.strip()
            link = "https://www.amazon.de" + link_el['href'].split("?")[0]
            img = img_el['src']
            results.append({'title': title, 'link': link, 'img': img})
    return jsonify(results)
