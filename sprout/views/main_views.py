from flask import Blueprint, render_template, redirect, url_for
import requests
from deep_translator import GoogleTranslator

bp = Blueprint('main', __name__)

EXCHANGE_RATE = 1300

CATEGORY_KO = {
    "furniture": "가구",
    "home-decoration": "인테리어 소품",
    "lighting": "조명",
    "rug": "러그"
}

# 루트 → 목록 페이지로 자동 이동
@bp.route('/')
def index():
    return redirect(url_for('main.interior'))

# 가구/인테리어 목록 페이지
@bp.route('/interior')
def interior():
    url = "https://dummyjson.com/products"
    response = requests.get(url)

    if response.status_code != 200:
        return "API 호출 실패", 500

    products_data = response.json()
    products = []

    for item in products_data['products']:
        if item['category'] in ["furniture", "home-decoration", "rug", "lighting"]:
            try:
                price_krw = int(item['price'] * EXCHANGE_RATE)
                category_ko = CATEGORY_KO.get(item['category'], item['category'])
                title_ko = GoogleTranslator(source='en', target='ko').translate(item['title'])
                products.append({
                    "id": item['id'],
                    "title": item['title'],
                    "title_ko": title_ko,
                    "price_usd": item['price'],
                    "price_krw": price_krw,
                    "thumbnail": item.get('thumbnail')
                })
            except:
                continue

    return render_template("interior_cards.html", products=products)


# 가구/인테리어 상세페이지
@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    url = f"https://dummyjson.com/products/{product_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return "상품 정보를 불러올 수 없습니다.", 500

    item = response.json()
    try:
        price_krw = int(item['price'] * EXCHANGE_RATE)
        category_ko = CATEGORY_KO.get(item['category'], item['category'])
        title_ko = GoogleTranslator(source='en', target='ko').translate(item['title'])
        description_ko = GoogleTranslator(source='en', target='ko').translate(item['description'])

        product = {
            "id": item['id'],
            "title": item['title'],
            "title_ko": title_ko,
            "description": item['description'],
            "description_ko": description_ko,
            "price_usd": item['price'],
            "price_krw": price_krw,
            "category": item['category'],
            "category_ko": category_ko,
            "thumbnail": item.get('thumbnail')
        }
    except:
        return "상품 정보 처리 중 오류", 500

    return render_template("product_detail.html", product=product)
