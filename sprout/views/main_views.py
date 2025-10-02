from flask import Blueprint, render_template, request
import json
import math

bp = Blueprint('main', __name__, url_prefix='/')

#json 데이터 페이지네이션 작동 클래스
class ProductPagination:
    def __init__(self, items, page, per_page, total):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = total
        self.pages = math.ceil(total / per_page) if total > 0 else 1

    @property
    def has_prev(self):
        return self.page > 1 #이전 페이지 존재 여부

    @property
    def has_next(self):
        return self.page < self.pages #다음 페이지 존재 여부

    @property
    def prev_num(self):
        return self.page - 1 if self.has_prev else None

    @property
    def next_num(self):
        return self.page + 1 if self.has_next else None

    def iter_pages(self, left_edge=1, right_edge=1, left_current=3, right_current=3):
        """최대 8개의 페이지 번호를 반환"""
        last = 0
        for num in range(1, self.pages + 1):
            if (num <= left_edge or
                    num > self.pages - right_edge or
                    (num >= self.page - left_current and num <= self.page + right_current)):
                if last + 1 != num:
                    yield None
                yield num
                last = num


def get_products_with_pagination(page):
    """제품 데이터를 페이지네이션하여 반환하는 공통 함수"""
    per_page = 25

    try:
        with open('data/products.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # products 키에서 배열 가져오기
            all_products = data.get('products', [])
    except FileNotFoundError:
        print("ERROR: data/products.json 파일을 찾을 수 없습니다!")
        all_products = []
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        all_products = []

    total = len(all_products)
    start = (page - 1) * per_page
    end = start + per_page
    current_products = all_products[start:end]

    return ProductPagination(current_products, page, per_page, total)

@bp.route('/')
def index():
    """메인 페이지 - 제품 목록"""
    page = request.args.get('page', 1, type=int)
    product_list = get_products_with_pagination(page)
    return render_template('main.html', product_list=product_list)


@bp.route('/products')
def products():
    """제품 페이지 - 제품 목록"""
    page = request.args.get('page', 1, type=int)
    product_list = get_products_with_pagination(page)
    return render_template('sub.html', product_list=product_list)

bp = Blueprint ('main',__name__, url_prefix='/')
@bp.route('/')
def index():
    return render_template('main.html')

