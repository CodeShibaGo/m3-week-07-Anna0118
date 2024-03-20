from app import db
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

# 使用者可以「追蹤」其他使用者是「多對多」關係：一個使用者可以追蹤多個使用者，同時一個使用者也可以被多個使用者追蹤
# 並不需要去特別的定義一個 Model 來做中繼，而是透過Table的方法，來設罝MetaData
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer,
                               db.ForeignKey('user.id'))
                     )

class User(db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256), nullable=True)
    about_me = db.Column(db.String(140))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    following = relationship(
        'User', 
        secondary=followers,  # 作為關聯的中間表，儲存追蹤關係
        primaryjoin=(followers.c.follower_id == id),  # 定義如何找到user的追蹤者
        secondaryjoin=(followers.c.followed_id == id),  # 定義如何找到是誰們追蹤user
        # dynamic 非一次載入所有找到的資料，有利於處理大量資料
        # backref 反向引用, 代表誰們追蹤當前user
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'

        # following 找到user的追蹤者
        # followers 透過 backref 自動建立一個表，代表誰們追蹤user
        # primaryjoin 和 secondaryjoin 透過 followers 表將兩個 User 實例做關聯
    )

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(
            followers.c.followed_id == user.id).count() > 0
