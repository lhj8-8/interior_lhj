from sprout import db

#회원 모델 생성
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) #필수 입력 아니면 nullable=True 가능


