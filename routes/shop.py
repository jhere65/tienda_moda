from flask import Blueprint, render_template, jsonify, request, session
from models import Product, Category

shop_bp = Blueprint('shop', __name__)


def get_cart():
    """Devuelve el carrito de la sesión actual."""
    return session.get('cart', {})


@shop_bp.route('/')
def index():
    featured   = Product.query.filter_by(featured=True).limit(8).all()
    categories = Category.query.all()
    return render_template('index.html', featured=featured, categories=categories)


@shop_bp.route('/catalogo')
def catalog():
    category_slug = request.args.get('categoria')
    query = request.args.get('q', '').strip()
    page  = request.args.get('page', 1, type=int)

    products_q = Product.query

    if category_slug:
        cat = Category.query.filter_by(slug=category_slug).first_or_404()
        products_q = products_q.filter_by(category_id=cat.id)
    else:
        cat = None

    if query:
        products_q = products_q.filter(Product.name.ilike(f'%{query}%'))

    products   = products_q.paginate(page=page, per_page=9, error_out=False)
    categories = Category.query.all()

    return render_template(
        'shop/catalog.html',
        products=products,
        categories=categories,
        current_cat=cat,
        query=query
    )


@shop_bp.route('/producto/<int:product_id>')
def product_detail(product_id):
    product  = Product.query.get_or_404(product_id)
    related  = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id
    ).limit(4).all()
    return render_template('shop/product.html', product=product, related=related)


@shop_bp.route('/carrito')
def cart():
    cart_data = get_cart()
    items = []
    total = 0.0

    for product_id, quantity in cart_data.items():
        p = Product.query.get(int(product_id))
        if p:
            subtotal = p.price * quantity
            total   += subtotal
            items.append({'product': p, 'quantity': quantity, 'subtotal': subtotal})

    return render_template('shop/cart.html', items=items, total=total)


# --- API JSON para el carrito (llamada desde JS) ---

@shop_bp.route('/api/cart/add', methods=['POST'])
def cart_add():
    data       = request.get_json()
    product_id = str(data.get('product_id'))
    quantity   = int(data.get('quantity', 1))

    product = Product.query.get(int(product_id))
    if not product:
        return jsonify({'error': 'Producto no encontrado'}), 404

    cart = get_cart()
    cart[product_id] = cart.get(product_id, 0) + quantity
    session['cart'] = cart

    return jsonify({'success': True, 'cart_count': sum(cart.values())})


@shop_bp.route('/api/cart/remove', methods=['POST'])
def cart_remove():
    data       = request.get_json()
    product_id = str(data.get('product_id'))

    cart = get_cart()
    cart.pop(product_id, None)
    session['cart'] = cart

    return jsonify({'success': True, 'cart_count': sum(cart.values())})


@shop_bp.route('/api/cart/count')
def cart_count():
    cart = get_cart()
    return jsonify({'count': sum(cart.values())})
