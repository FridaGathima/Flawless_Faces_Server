from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
# from app import db

db = SQLAlchemy()

class User (db.Model, SerializerMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    # does nullable= false eliminate the need for @validates??

    # Database relationships
    cart = db.relationship('Cart', back_populates = 'user')

    # to convert a sqlalchemy row to Python dict
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            'email': self.email,
            'password': self.password
        }

    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if first_name == '' or first_name == int:
            raise ValueError('first_name is required/ enter a valid first namde')
        return first_name
        
    @validates('last_name')
    def validate_first_name(self, key, last_name):
        if last_name == '' or last_name == int:
            raise ValueError('last_name is required/ enter a valid last name')
        return last_name
        

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError('invalid email address')
        return email
    

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String, nullable=False)
    brand_name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    sub_category = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    date_uploaded = db.Column(db.DateTime, default=datetime.utcnow)

    # Database relationships
    brand = db.relationship('Brand', back_populates = 'product')
    cart = db.relationship('Cart', back_populates = 'product')

    def to_dict(self):
        return {
            "product_id":self.product_id,
            "product_name":self.product_name,
            "brand_name":self.brand_name,
            "category":self.category,
            "sub_category":self.sub_category,
            "price":self.price,
            "image":self.image,
            "description":self.description,
            "date_uploaded":self.date_uploaded
        }
    
    @validates('category')
    def validate_category(self, key, category):
        if category not in ["Makeup", "SkinCare", "HairCare"]:
            raise ValueError("Invalid category")
        return category
    
    @validates('sub_category')
    def validate_sub_category(self, key, sub_category):
        if sub_category not in ["Lip Makeup", "Face Makeup", "Eye Makeup", "Sunscreen", "Cleansers", "Moisturizers","Face Toners","Shampoo","Conditioners","Hair_Gels", "Hair Food" ]:
            raise ValueError("Invalid sub_category")
        return sub_category
    
    @validates('price')
    def validate_price(self, key, price):
        if price <=0:
            raise ValueError ("Enter a valid price")
        return price
    
class Brand(db.Model, SerializerMixin):
    __tablename__ = 'brands'
    brand_id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))

    # Database relationships
    product = db.relationship('Product', back_populates = 'brand')

    def to_dict(self):
        return {
            "brand_id":self.brand_id,
            "product_id":self.product_id
        }

class Cart(db.Model, SerializerMixin):
    __tablename__ = 'carts'

    cart_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    
    # Database relationships
    user = db.relationship('User', back_populates = 'cart')
    product = db.relationship('Product', back_populates = 'cart')
    # one to one relationship
    payment = db.relationship('Payment', back_populates = 'cart', uselist=False)

    def to_dict(self):
        return {
            "cart_id":self.cart_id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "total_amount":self.total_amount
        }

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        if quantity <=0:
            raise ValueError ("Enter valid quantity")
        return quantity
    
class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key = True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.cart_id'))
    payment_method = db.Column(db.String, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Database relationships
    # one to many relationship
    cart = db.relationship('Cart', back_populates = 'payment')
    sale = db.relationship('Sale', back_populates = 'payment')

    def to_dict(self):
        return {
            "payment_id":self.payment_id,
            "cart_id":self.cart_id,
            "payment_method":self.payment_method,
            "payment_date":self.payment_date
        }

    @validates('payment_method')
    def validate_payment_method(self, key, payment_method):
        if payment_method not in ["Mpesa", "Paypal", "Equity"]:
            raise ValueError("Invalid payment method")
        return payment_method
    
class Sale(db.Model, SerializerMixin):
    __tablename__ = 'sales'

    sales_id =  payment_id = db.Column(db.Integer, primary_key = True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.payment_id'))
    date_of_sale = db.Column(db.DateTime, default=datetime.utcnow)

    # Database relationship
    # one to one relationship
    payment = db.relationship('Payment', back_populates = 'sale', uselist=False)

    def to_dict(self):
        return { 
           "sales_id" :self.sales_id,
           "payment_id":self.payment_id,
           "date_of_sale":self.date_of_sale
        }

    
    
