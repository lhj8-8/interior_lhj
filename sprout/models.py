from sprout import db
from datetime import datetime

#회원 모델 생성
class User(db.Model):
    __tablename__ = 'user'
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) #필수 입력 아니면 nullable=True 가능
    phone = db.Column(db.String(20), nullable=True)
    # address = db.Column(db.String(300)) #배송지 필요할 때 추가
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

def __repr__(self):
    return f'<User {self.username}>'

    # 이용자(user)와 연결된 식별자
class CartItem(db.Model):
    __tablename__ = 'cart_item'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # 이용자(user)시 접근 허용 가능
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))

    def __repr__(self):
        return f'<CartItem user_id={self.user_id} product_id={self.product_id}>'


