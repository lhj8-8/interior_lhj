<<<<<<< HEAD
<<<<<<< HEAD
from sprout import create_app, db
from sprout.models import User, CartItem
from flask import render_template, request
import os, json
=======
from sprout import create_app, db
from sprout.models import User, CartItem
>>>>>>> upstream/develop

# sprout 패키지의 create_app() 사용
app = create_app()


# 더미 데이터 생성 함수 (필요시 사용)
def create_dummy_data():
    with app.app_context():
        db.create_all()
<<<<<<< HEAD
        print('데이터베이스 테이블 생성 완료!')


# 상세 페이지 라우트
@app.route("/product_detail")
def product_detail():
    product_id = request.args.get("product_id")

    # product_id가 없거나 정수가 아닐 때 처리
    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        return " 잘못된 product_id 형식입니다.", 400

    # JSON 파일 경로
    json_path = os.path.join(os.getcwd(), "data", "products.json")

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            products = data.get("products", [])
    except FileNotFoundError:
        return " products.json 파일을 찾을 수 없습니다.", 404
    except json.JSONDecodeError as e:
        return f" JSON 형식 오류: {e}", 400

    # id 일치하는 상품 찾기
    product = next((p for p in products if p.get("id") == product_id), None)

    if not product:
        return f" id={product_id}에 해당하는 상품을 찾을 수 없습니다.", 404

    return render_template("product_detail.html", product=product)


=======
        # User 테이블과 CartItem 테이블만 생성
        # 제품 데이터는 data/products.json에서
        print('데이터베이스 테이블 생성 완료!')


>>>>>>> upstream/develop
# 등록된 라우트 확인
with app.app_context():
    print("\n" + "=" * 70)
    print("📋 등록된 라우트 목록")
    print("=" * 70)
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
        print(f"{rule.endpoint:35s} {methods:15s} {rule.rule}")
    print("=" * 70 + "\n")

<<<<<<< HEAD

=======
>>>>>>> upstream/develop
if __name__ == '__main__':
    # 데이터베이스 테이블 생성
    create_dummy_data()

    # Flask 서버 실행
<<<<<<< HEAD
    app.run(debug=True)
=======
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)


# 제품 모델 예시
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100))
    price = db.Column(db.Integer)
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(50))

    def __repr__(self):
        return f'<Product {self.name}>'


@app.route('/products')
@app.route('/products/<int:page>')
def product_list(page=1):
    # 페이지당 25개 제품 (5x5)
    per_page = 25

    # 페이지네이션 적용
    product_list = Product.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template('sub.html', product_list=product_list)


# 더미 데이터 생성 함수 (테스트용)
def create_dummy_data():
    with app.app_context():
        db.create_all()

        # 이미 데이터가 있으면 리턴
        if Product.query.first():
            return

        brands = ['IKEA', 'MUJI', '한샘', 'HAY', '비트라']
        categories = ['소파', '테이블', '의자', '수납장', '조명']

        for i in range(100):
            product = Product(
                name=f'제품명 {i + 1} - 모던 디자인 가구',
                brand=brands[i % len(brands)],
                price=(i + 1) * 10000,
                image_url=f'https://via.placeholder.com/684x684?text=Product+{i + 1}',
                category=categories[i % len(categories)]
            )
            db.session.add(product)

        db.session.commit()
        print('더미 데이터 100개 생성 완료!')


if __name__ == '__main__':
    create_dummy_data()
    app.run(debug=True)
>>>>>>> upstream/main
=======
    app.run(debug=True)
>>>>>>> upstream/develop
