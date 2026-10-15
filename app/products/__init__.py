from flask import Blueprint

product_bp = Blueprint(
    'products', __name__, template_folder='templates/products', url_prefix='/products'
)

from app.products import views