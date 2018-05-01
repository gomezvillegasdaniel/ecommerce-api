from db import db
import datetime


class PurchaseLogModel(db.Model):
    __tablename__ = 'purchase_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = db.relationship('ProductModel')
    purchase_quantity = db.Column(db.Integer)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user, product_id, purchase_quantity):
        self.user = user
        self.product_id = product_id
        self.purchase_quantity = purchase_quantity

    @classmethod
    def find_by_user(cls, user):
        return cls.query.filter_by(user=user).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_product(cls, product):
        return cls.query.filter_by(product=product).all()

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'product': self.product.to_dict(),
            'datetime': str(self.datetime)
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()