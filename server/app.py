from flask import Flask
from flask_restful import Resource, Api
# from models import User, Payment, Product, Cart, Sale, Brand
from models import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
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
    # 1. /login
    # 2. /register
    # 3. /
    # 4. /products
    # 6./makeup
    # 7./skincare
    # 8./haircare
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
    # 20. /brands


class Home(Resource):
    def get(self):
        return {'hello': 'Welcome to Flawless Faces API. Get crazy with Makeup, Skincare and Hair Care!!'}

api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run(debug=True)