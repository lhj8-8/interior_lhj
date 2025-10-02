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