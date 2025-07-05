import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS

# Import database
from src.models.user import db

# Import all models to ensure they're registered with SQLAlchemy
from src.models.user import User
from src.models.grocery_chain import GroceryChain
from src.models.store import Store
from src.models.product_category import ProductCategory
from src.models.product import Product
from src.models.price import Price

# Import all blueprints
from src.routes.user import user_bp
from src.routes.stores import stores_bp
from src.routes.products import products_bp
from src.routes.prices import prices_bp
from src.routes.locations import locations_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# Register all blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(stores_bp, url_prefix='/api')
app.register_blueprint(products_bp, url_prefix='/api')
app.register_blueprint(prices_bp, url_prefix='/api')
app.register_blueprint(locations_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create all tables
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return {
        'status': 'healthy',
        'message': 'Grocery Price Comparison API is running',
        'version': '1.0.0'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
