from flask import Flask, jsonify
from flask_restful import Resource, Api
# from models import User, Payment, Product, Cart, Sale, Brand
from models import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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

# db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
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
                
    

api.add_resource(Home, '/')
api.add_resource(ProductsList, '/products')
api.add_resource(ProductByCategory, '/products/<string:category>')
api.add_resource(ProductBySubCategory, '/products/category/<string:sub_category>')
api.add_resource(ProductByBrands, '/<string:brand_name>')



if __name__ == '__main__':
    app.run(debug=True)