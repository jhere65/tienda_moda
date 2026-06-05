from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import db, Product, Category, Order, User

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """Decorador: solo usuarios con is_admin=True pueden acceder."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return login_required(decorated)


@admin_bp.route('/')
@admin_required
def dashboard():
    stats = {
        'total_products': Product.query.count(),
        'total_users':    User.query.filter_by(is_admin=False).count(),
        'total_orders':   Order.query.count(),
        'categories':     Category.query.count(),
    }
    recent_products = Product.query.order_by(Product.created.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, recent_products=recent_products)


@admin_bp.route('/productos')
@admin_required
def products():
    all_products = Product.query.order_by(Product.created.desc()).all()
    return render_template('admin/dashboard.html',
                           products=all_products,
                           view='products',
                           stats={
                               'total_products': Product.query.count(),
                               'total_users':    User.query.filter_by(is_admin=False).count(),
                               'total_orders':   Order.query.count(),
                               'categories':     Category.query.count(),
                           })


@admin_bp.route('/producto/nuevo', methods=['GET', 'POST'])
@admin_required
def add_product():
    categories = Category.query.all()

    if request.method == 'POST':
        name        = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price       = request.form.get('price', 0, type=float)
        image_url   = request.form.get('image_url', '').strip()
        stock       = request.form.get('stock', 0, type=int)
        featured    = request.form.get('featured') == 'on'
        category_id = request.form.get('category_id', type=int)

        if not name or price <= 0:
            flash('Nombre y precio son obligatorios.', 'error')
            return render_template('admin/add_product.html', categories=categories)

        product = Product(
            name=name,
            description=description,
            price=price,
            image_url=image_url,
            stock=stock,
            featured=featured,
            category_id=category_id
        )
        db.session.add(product)
        db.session.commit()
        flash(f'Producto "{name}" agregado correctamente.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/add_product.html', categories=categories)


@admin_bp.route('/producto/editar/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product    = Product.query.get_or_404(product_id)
    categories = Category.query.all()

    if request.method == 'POST':
        product.name        = request.form.get('name', '').strip()
        product.description = request.form.get('description', '').strip()
        product.price       = request.form.get('price', 0, type=float)
        product.image_url   = request.form.get('image_url', '').strip()
        product.stock       = request.form.get('stock', 0, type=int)
        product.featured    = request.form.get('featured') == 'on'
        product.category_id = request.form.get('category_id', type=int)

        db.session.commit()
        flash(f'Producto "{product.name}" actualizado.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit_product.html', product=product, categories=categories)


@admin_bp.route('/producto/eliminar/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    name    = product.name
    db.session.delete(product)
    db.session.commit()
    flash(f'Producto "{name}" eliminado.', 'info')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/pedidos')
@admin_required
def orders():
    all_orders = Order.query.order_by(Order.created.desc()).all()
    return render_template('admin/orders.html', orders=all_orders)


@admin_bp.route('/pedido/estado/<int:order_id>', methods=['POST'])
@admin_required
def update_order_status(order_id):
    order  = Order.query.get_or_404(order_id)
    status = request.form.get('status')
    if status in ('pendiente', 'procesando', 'enviado', 'entregado'):
        order.status = status
        db.session.commit()
        flash('Estado del pedido actualizado.', 'success')
    return redirect(url_for('admin.orders'))
