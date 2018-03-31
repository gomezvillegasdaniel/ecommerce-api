from db import db
import datetime


class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    npc = db.Column(db.String(80))
    stock = db.Column(db.Integer)
    price = db.Column(db.Float(precision=2))
    likes = db.Column(db.Integer, default=0)
    last_update = db.Column(db.DateTime)

    def __init__(self, name, npc, stock, price):
        self.name = name
        self.npc = npc
        self.stock = stock
        self.price = price
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name, *order_by, **pagination):
        return cls.query.filter_by(name=name).order_by(*order_by).paginate(**pagination)

    @classmethod
    def all_items(cls, *order_by, **pagination):
        return cls.query.order_by(*order_by).paginate(**pagination)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'npc': self.npc,
            'stock': self.stock,
            'price': self.price,
            'likes': self.likes,
            'last_update': str(self.last_update)
        }

    def save_to_db(self):
        self.last_update = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
