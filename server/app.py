from flask import Flask, jsonify, make_response, request, session
from flask_restful import Resource, Api
# from models import User, Payment, Product, Cart, Sale, Brand
from models import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import bcrypt
from flask_cors import CORS

class CaseInsensitiveApi(Api):
    def url_for(self, resource, **values):
        target = resource.endpoint
        for rule in self.app.url_map.iter_rules():
            if target == rule.endpoint:
                for arg in rule.arguments:
                    if arg in values:
                        values[arg] = values[arg].lower()
                if "path" in values:
                    values["path"] = values["path"].lower()
        return super(CaseInsensitiveApi, self).url_for(resource, **values)


app = Flask(__name__)
api = CaseInsensitiveApi(app) 
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flawless_faces.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']='1OH1BiZEkLSoN9rQkIb52sO5AC0vTV9LoyQ3vXY0g0g'

# db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)
jwt = JWTManager(app)
db.init_app(app)
with app.app_context():
    db.create_all()


# Routes that I need:
    # **GET
    # **POST
    # **PATCH/PUT
    # **DELETE

    # 1. /login
    # 2. /register
    # 3. / **DONE
    # 4. /products/category *GET-DONE
    # 9. /makeup/lipmakeup
    # 10. /makeup/facemakeup
    # 11. /makeup/eyemakeup 
    # 12. /skincare/sunscreen 
    # 13. /skincare/cleansers
    # 14. /skincare/moisturizers
    # 15. /skincare/facetoners
    # 16. /haircare/shampoo
    # 17. /haircare/conditioners
    # 18. /haircare/hairgels
    # 19. /haircare/hairfood
    # 20. /brands ***DONE 
    # 21. /login
    # 22. /register
    # 23. /cart

# Cart Management
    # what happens when a user clicks on cart
    # cart to be added +1 and added to cart db
    # when items goes to checkout the item should reduce in the db and added in purchases
    # customer clicked add to cart - db cart increases in item - clicks checkout/pay item deleted from cart and added to payments and deleted in products
    # customer clicks on delete from cart removes item from cart delete cart db 
    # cart table purchases table


class Home(Resource):
    def get(self):
        return {'hello': 'Welcome to Flawless Faces API. Get crazy with Makeup, Skincare and Hair Care!!'}
    
class ProductsList(Resource):
    def get(self):
        products=Product.query.all()
        return jsonify({"products": [product.to_dict() for product in products]}, 200)

class ProductByCategory(Resource):
    def get(self, category):
        category_list = Product.query.filter_by(category=category).all()
        if category_list:
            return jsonify({"products": [product.to_dict() for product in category_list]}, 200)

            # products = []
            # for product in category_list:
            #     product_dict = {
            #         "product_id": product.product_id,
            #         "product_name": product.product_name,
            #         "brand_name": product.brand_name,
            #         "category": product.category,
            #         "sub_category": product.sub_category,
            #         "price": product.price,
            #         "image": product.image,
            #         "description": product.description,
            #         "date_uploaded": product.date_uploaded
            #     }
            #     products.append(product_dict)

            # return jsonify({"products": products}, 200)
        else:
            return jsonify({"error": "category not found"})
        
class ProductBySubCategory(Resource):
    def get(self, sub_category):
        sub_category_list=Product.query.filter_by(sub_category=sub_category).all()

        if sub_category_list:
            return jsonify({"products": [product.to_dict() for product in sub_category_list]}, 200)
        else:
            return jsonify({"error": "sub-category not found"})
        
class ProductByBrands(Resource):
    def get(self,brand_name):
        brand_list=Product.query.filter_by(brand_name=brand_name)

        if brand_list:
            return jsonify({"products": [product.to_dict() for product in brand_list]}, 200)
        else:
            return jsonify({"error": "brand not found"})
        
class UserList(Resource):
    def get(self):
        user_list = User.query.all()

        if user_list:
            return jsonify({"users": [product.to_dict() for product in user_list]}, 200)
        else:
            return jsonify({"error": "user not found"})
        
class UserLogin(Resource):
    def post(self):
        data=request.get_json()
        email = data.get('email')
        password = data.get('password')
      
        user = User.query.filter_by(email=email, password=password).first()
            
        if user:
            access_token = create_access_token(identity=user.user_id)
            response=make_response(jsonify(access_token=access_token), 200)
        elif not email or not password:
            response = make_response({"message": "Missing email or password"}, 400)
            return response
        else:
            return make_response({"message":"Invalid email or password"})
        return response
    
class UserRegistration(Resource):
    def post(self):
        data=request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            return make_response({"message":"User already exists"}, 400)
        else:
            new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            
            return make_response({"message": "User created successfully"}, 201)

# Cart Management
    # what happens when a user clicks on cart
    # cart to be added +1 and added to cart db
    # when items goes to checkout the item should reduce in the  cart db and added in purchases
    # customer clicked add to cart - db cart increases in item - clicks checkout/pay item deleted from cart and added to payments and deleted in products
    # customer clicks on delete from cart removes item from cart delete cart db 
    # cart table purchases table
    

class CartManagement(Resource):
    def post(self):
        data = request.get_json()
        user_id=data.get('user_id')
        product_id=data.get('product_id')
        quantity=data.get('quantity')
        total_amount=data.get('total_amount')

        user = User.query.filter_by(user_id=user_id).first() 

        if not user:
            return {'message': 'User not found'}, 404
        else:
            # cart=Cart.query.filter_by(user_id=user_id).first()
             
            # if not cart:
            cart=Cart(user_id=user_id, product_id=product_id, quantity=quantity, total_amount=total_amount)
            db.session.add(cart)
            db.session.commit()
        
            return make_response({'message': 'Items added to the cart successfully'}, 200)
        
class PaymentCheckoutManagement(Resource):
    def post(self):
        data = request.get_json()
        cart_id = data.get('cart_id')
        payment_method= data.get('payment_method')
        payment_id=data.get('payment_id')
        product_id=data.get('product_id')

        # purchase_item=Payment.query.filter_by(cart_id=cart_id).first()
        cart_item=Cart.query.filter_by(cart_id=cart_id).first()
        new_purchase_item=Payment(cart_id=cart_id, payment_method=payment_method)
        new_sales_item=Sale(cart_id=cart_id, payment_id=payment_id)
        # deleted_product_item=Product(product_id=product_id)
        # item should be deleted from product quantity. infact there should be another column for product quantity in products table

        if cart_item:
            db.session.delete(cart_item)
            # db.session.delete(deleted_product_item)
            db.session.add(new_purchase_item)
            db.session.add(new_sales_item)
            db.session.commit()

            return {'message': 'payment successful. check sales'}, 200
        else:
            # new_purchase_item=Payment(cart_id=cart_id, payment_method=payment_method)
            # db.session.add(new_purchase_item)
            # db.session.commit()
            return {'message': 'payment was not successful. please try again.'}, 200

   
        



api.add_resource(Home, '/')
api.add_resource(ProductsList, '/products')
api.add_resource(ProductByCategory, '/products/<string:category>')
api.add_resource(ProductBySubCategory, '/products/category/<string:sub_category>')
api.add_resource(ProductByBrands, '/<string:brand_name>')
api.add_resource(UserList, '/users')
api.add_resource(UserLogin, '/login')
api.add_resource(UserRegistration, '/register')
api.add_resource(CartManagement, '/cart')
api.add_resource(PaymentCheckoutManagement, '/payments')




if __name__ == '__main__':
    app.run(debug=True)