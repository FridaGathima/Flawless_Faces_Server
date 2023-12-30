from faker import Faker
from models import *
from models import Product
from app import app, db
import random
from random import randint
from datetime import datetime

fake = Faker()

all_products = ['Maybelline FitMe Foundation', 'Revlon Foundation', 'Fenty Beauty Foundation', 'Biw Biw Allure Eyeshadow Pallet', 'Nouba Reflecta Liptstick', 'Maybelline Superstay Ink Liquid Lipstick', 'Revlon ColorStay 16hr Eyeshadow', 'Maybelline Great Lash Mascara - Black', 'Neutrogena Hydroboost Sunscreen SPF 50', 'Acnes UV Tint Sunscreen SPF 30', 'Cetaphil Sheer Mineral Sunscreen SPF 50', 'Neutrogena Acne Wash Pink Grape Fruit', 'Cetaphil Gentle Skin Cleanser', 'Acnes Creamy Wash Cleanser', 'Neutrogena Hydroboost Water Gel Moisturizer', 'Cetaphil Intensive Moisturizing Cream', 'Neutrogena Oil Free Acne Stress Control Toner', 'Cetaphil Healthy Radiance Brightness Toner', 'Acnes Soothing Toner', 'African Pride Miracle Moisture Shampoo', 'Shea Moisture Butter Shampoo', 'Mizani Moisture Fusion Shampoo', 'African Pride Miracle Moisture Conditioner', 'Shea Moisture Restorative Conditioner', 'Mizani Miracle Leave-in Conditioner', 'African Pride Aloe Defining Gel', 'Shea Moisture Frizz Control Curling Gel', 'Mizani Rose Hair Dress']

all_brands = ['Maybelline', 'Nouba', 'Fenty Beauty', 'Biw Biw', 'Acnes', 'Cetaphil', 'Neutrogena', 'African Pride', 'Shea Moisture', 'Mizani']

sub_categories = ['Lip Makeup', 'Face Makeup', 'Eye Makeup', 'Sunscreen', 'Cleansers', 'Moisturizers','Face Toners','Shampoo','Conditioners','Hair_Gels', 'Hair Food']

images = ['https://media.licdn.com/dms/image/C4D12AQFv-Ujn1DXmgg/article-cover_image-shrink_600_2000/0/1616730007484?e=2147483647&v=beta&t=gnmFKh62P6cbki6kMh74QJIgvVVPeP0Kgj72iEXsRUc', 'https://i.pinimg.com/originals/f4/33/53/f43353b010b808fdca85bbb11fdad8d4.jpg']

all_payments = ["Mpesa", "Paypal", "Equity"]

def seed_data():
    # create users
    users = []
    for _ in range(8):
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            password=fake.password()
            
        )
        users.append(user)
        db.session.add(user)

    # create products
    products = []
    for _ in range(10):
        product = Product(
            product_name=random.choice(all_products),
            brand_name=random.choice(all_brands),
            category=fake.random_element(elements=('Makeup', 'SkinCare', 'HairCare')),
            sub_category=random.choice(sub_categories),
            price=random.randint(5, 100),
            image=random.choice(images),
            description=fake.text(),
            date_uploaded=datetime.now()
        )
        products.append(product)
        db.session.add(product)

    # create brands
    brands = []
    for _ in range(10):
        brandd=Brand(   
            product_id=random.randint(1, 10)
        )

        brands.append(brandd)
        db.session.add(brandd)

    # create cart
    carts = []
    for _ in range(10):
        cart = Cart(
            user_id=random.randint(1, 10),
            product_id=random.randint(1, 10),
            quantity=random.randint(1, 30),
            total_amount=random.randint(1, 200)
        )
        carts.append(cart)
        db.session.add(cart)

    # create payments
    payments = []
    for _ in range(10):
        payment = Payment(
            cart_id=random.randint(1, 10),
            payment_method=random.choice(all_payments),
            payment_date=datetime.now()
        )
        payments.append(payment)
        db.session.add(payment)


    
    # create sales
    sales = []
    for _ in range(10):
        sale = Sale(
            payment_id=random.randint(1, 10),
            date_of_sale=datetime.now(),
        
        )
        sales.append(sale)
        db.session.add(sale)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        db.create_all()

        # Seed data into the database
        seed_data()
