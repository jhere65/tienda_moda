# NOMA — Tienda Virtual de Moda

Tienda virtual de portafolio construida con **Python + Flask + HTML/CSS**.

## Características

- Catálogo de productos con filtros por categoría y búsqueda
- Slider horizontal con animaciones y drag-to-scroll
- Carrito de compras (sesión Flask)
- Sistema de autenticación (Login / Registro)
- Panel de administración completo (CRUD de productos, gestión de pedidos)
- Diseño oscuro y moderno con paleta de colores personalizada
- Responsive

## 🗂 Estructura del proyecto

```
tienda_moda/
├── app.py              # Punto de entrada + factory + seed de datos
├── config.py           # Configuración (DB, secret key)
├── models.py           # Modelos: User, Category, Product, Order, OrderItem
├── requirements.txt
├── .gitignore
├── routes/
│   ├── auth.py         # Login, registro, logout
│   ├── shop.py         # Inicio, catálogo, detalle, carrito (API JSON)
│   └── admin.py        # Dashboard, CRUD productos, pedidos
├── templates/
│   ├── base.html       # Layout base (navbar, footer, flash messages)
│   ├── index.html      # Página de inicio con hero + slider
│   ├── auth/           # login.html, register.html
│   ├── shop/           # catalog.html, product.html, cart.html
│   └── admin/          # dashboard.html, add_product.html, edit_product.html, orders.html
└── static/
    ├── css/style.css   # Todos los estilos (paleta, animaciones, responsive)
    └── js/
        ├── main.js     # Navbar scroll, flash dismiss, animaciones entrada
        ├── slider.js   # Carrusel horizontal con drag + momentum
        └── cart.js     # API del carrito (fetch)
```

##  Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/tienda_moda.git
cd tienda_moda

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python app.py
```

Abrir en el navegador: `http://127.0.0.1:5000`

##  Credenciales de demo

| Rol   | Email             | Contraseña |
|-------|-------------------|------------|
| Admin | admin@noma.com    | admin123   |

Los datos de ejemplo (10 productos, 5 categorías) se insertan automáticamente al primer arranque.

##  Paleta de colores

| Variable     | Hex       | Uso                   |
|--------------|-----------|-----------------------|
| `--dark-1`   | `#11091a` | Fondo principal       |
| `--dark-2`   | `#2f2f4d` | Tarjetas, sidebar     |
| `--mid`      | `#626970` | Texto secundario      |
| `--sand`     | `#bab195` | Texto intermedio      |
| `--gold`     | `#e8d18e` | Acentos, precios, CTA |

## 🛠 Tecnologías

- **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-Login
- **Base de datos:** SQLite (archivo local `store.db`)
- **Frontend:** HTML5, CSS3 (custom properties), JavaScript vanilla
- **Fuentes:** Cormorant Garamond + DM Sans (Google Fonts)
