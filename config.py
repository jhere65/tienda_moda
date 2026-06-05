import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Clave secreta para sesiones — cambiar en producción
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-cambiar-en-produccion')

    # Base de datos SQLite local
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'store.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Nombre de la tienda
    STORE_NAME = 'NOMA'
    STORE_TAGLINE = 'Moda que define tu esencia'
