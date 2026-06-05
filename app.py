from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User, Category, Product


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Inicia sesión para continuar.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar blueprints
    from routes.auth  import auth_bp
    from routes.shop  import shop_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp,  url_prefix='/auth')
    app.register_blueprint(shop_bp,  url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Crear tablas y datos semilla si no existen
    with app.app_context():
        db.create_all()
        _seed_data()

    return app


def _seed_data():
    """Inserta datos de ejemplo la primera vez que se ejecuta."""
    from werkzeug.security import generate_password_hash

    # Admin por defecto
    if not User.query.filter_by(email='admin@noma.com').first():
        admin = User(
            username='admin',
            email='admin@noma.com',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)

    # Categorías
    cats = ['Vestidos', 'Camisas', 'Pantalones', 'Accesorios', 'Calzado']
    for cat_name in cats:
        if not Category.query.filter_by(name=cat_name).first():
            slug = cat_name.lower().replace(' ', '-')
            db.session.add(Category(name=cat_name, slug=slug))

    db.session.flush()

    # Productos de ejemplo con imágenes de Unsplash (ropa)
    sample_products = [
        {
            'name': 'Vestido Nocturno',
            'description': 'Elegancia en cada hilo. Perfecto para veladas especiales.',
            'price': 189.90,
            'image_url': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=600&q=80',
            'stock': 12, 'featured': True, 'category': 'Vestidos'
        },
        {
            'name': 'Vestido Soleil',
            'description': 'Fluido y etéreo. Diseñado para brillar bajo el sol.',
            'price': 145.00,
            'image_url': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600&q=80',
            'stock': 8, 'featured': True, 'category': 'Vestidos'
        },
        {
            'name': 'Camisa Línea Blanca',
            'description': 'Corte impecable. El básico que nunca falla.',
            'price': 79.90,
            'image_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&q=80',
            'stock': 20, 'featured': True, 'category': 'Camisas'
        },
        {
            'name': 'Camisa Lino Natural',
            'description': 'Textura artesanal. Fresca y sofisticada.',
            'price': 95.00,
            'image_url': 'https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=600&q=80',
            'stock': 15, 'featured': False, 'category': 'Camisas'
        },
        {
            'name': 'Pantalón Wide Leg',
            'description': 'Silueta de impacto con máxima comodidad.',
            'price': 120.00,
            'image_url': 'https://images.unsplash.com/photo-1594938298603-c8148c4b8e5f?w=600&q=80',
            'stock': 10, 'featured': True, 'category': 'Pantalones'
        },
        {
            'name': 'Pantalón Sastre',
            'description': 'Corte recto clásico en gabardina premium.',
            'price': 135.00,
            'image_url': 'https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=600&q=80',
            'stock': 7, 'featured': False, 'category': 'Pantalones'
        },
        {
            'name': 'Bolso Cuero Crudo',
            'description': 'Artesanía italiana. Pieza que dura generaciones.',
            'price': 220.00,
            'image_url': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&q=80',
            'stock': 5, 'featured': True, 'category': 'Accesorios'
        },
        {
            'name': 'Cinturón Trenzado',
            'description': 'El detalle que define el look completo.',
            'price': 55.00,
            'image_url': 'https://images.unsplash.com/photo-1624222247344-550fb60583dc?w=600&q=80',
            'stock': 18, 'featured': False, 'category': 'Accesorios'
        },
        {
            'name': 'Mocasines Crema',
            'description': 'Comodidad sin sacrificar estilo. Cuero suave.',
            'price': 175.00,
            'image_url': 'https://images.unsplash.com/photo-1560343090-f0409e92791a?w=600&q=80',
            'stock': 9, 'featured': True, 'category': 'Calzado'
        },
        {
            'name': 'Sandalia Minimalista',
            'description': 'Diseño limpio para días perfectos.',
            'price': 98.00,
            'image_url': 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=600&q=80',
            'stock': 14, 'featured': False, 'category': 'Calzado'
        },
    ]

    for p in sample_products:
        if not Product.query.filter_by(name=p['name']).first():
            cat = Category.query.filter_by(name=p['category']).first()
            product = Product(
                name=p['name'],
                description=p['description'],
                price=p['price'],
                image_url=p['image_url'],
                stock=p['stock'],
                featured=p['featured'],
                category_id=cat.id if cat else None
            )
            db.session.add(product)

    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
