from datetime import datetime
import os
from app.products import product_bp
from app.products.db import products_table
from app.products.forms import ProductForm
from flask import current_app, flash, redirect, render_template, request, url_for
from tinydb import Query
from werkzeug.utils import secure_filename
import uuid

def save_picture(file_data):
    filename = secure_filename(file_data.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f'{uuid.uuid4().hex}.{ext}'

    upload_folder = os.path.join(
        current_app.root_path, 'static', 'uploads', 'products'
    )
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, unique_filename)
    file_data.save(file_path)

    return f'uploads/products/{unique_filename}'

@product_bp.route('/')
def product_list():
    all_products = products_table.all()
    return render_template('main.html', products=all_products)

@product_bp.route('/add', methods=['GET', 'POST'])
@product_bp.route('/product/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        image_path = save_picture(form.image.data)

        all_items = products_table.all()
        new_id = (
                max([item.get('id', 0) for item in all_items], default=0) + 1
        )

        product_data = {
            'id': new_id,
            'name': form.name.data,
            'content': form.content.data,
            'price': float(form.price.data),
            'category': form.category.data,
            'quantity': form.quantity.data,
            'image': image_path,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        products_table.insert(product_data)
        flash('Товар успішно додано!', 'success')
        return redirect(url_for('products.product_list'))

    return render_template('add_product.html', form=form)

@product_bp.route('/<int:product_id>')
def product_detail(product_id):
    Product = Query()
    product = products_table.get(Product.id == product_id)
    if not product:
        flash('Товар не знайдено!', 'error')
        return redirect(url_for('products.product_list'))
    return render_template('detail.html', product=product)

@product_bp.route('/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    Product = Query()
    product = products_table.get(Product.id == product_id)
    if product:
        products_table.remove(Product.id == product_id)
        flash('Товар успішно видалено!', 'success')
    else:
        flash('Товар не знайдено!', 'error')
    return redirect(url_for('products.product_list'))