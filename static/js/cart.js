/* ============================================================
   cart.js — Manejo del carrito (sesión Flask)
   ============================================================ */

const Cart = {
  badge: null,

  init() {
    this.badge = document.querySelector('.cart-badge');
    this._updateCount();

    // Delegar evento en todos los botones "agregar al carrito"
    document.addEventListener('click', e => {
      const btn = e.target.closest('[data-add-to-cart]');
      if (btn) {
        e.preventDefault();
        const productId = btn.dataset.addToCart;
        const quantity  = parseInt(btn.dataset.quantity || '1');
        this.add(productId, quantity, btn);
      }

      const removeBtn = e.target.closest('[data-remove-from-cart]');
      if (removeBtn) {
        e.preventDefault();
        const productId = removeBtn.dataset.removeFromCart;
        this.remove(productId);
      }
    });
  },

  async add(productId, quantity = 1, btnEl = null) {
    if (btnEl) {
      btnEl.disabled = true;
      btnEl.textContent = 'Agregando…';
    }

    try {
      const res  = await fetch('/api/cart/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, quantity })
      });
      const data = await res.json();

      if (data.success) {
        this._updateBadge(data.cart_count);
        this._showFeedback(btnEl, '✓ Agregado');
        this._animateBadge();
      }
    } catch (err) {
      console.error('Error al agregar al carrito:', err);
    } finally {
      setTimeout(() => {
        if (btnEl) {
          btnEl.disabled = false;
          btnEl.textContent = 'Agregar al carrito';
        }
      }, 1500);
    }
  },

  async remove(productId) {
    try {
      const res  = await fetch('/api/cart/remove', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId })
      });
      const data = await res.json();

      if (data.success) {
        this._updateBadge(data.cart_count);
        // Eliminar fila de la tabla sin recargar
        const row = document.querySelector(`[data-cart-row="${productId}"]`);
        if (row) {
          row.style.opacity = '0';
          row.style.transition = 'opacity 0.3s ease';
          setTimeout(() => { row.remove(); location.reload(); }, 300);
        }
      }
    } catch (err) {
      console.error('Error al eliminar del carrito:', err);
    }
  },

  async _updateCount() {
    try {
      const res  = await fetch('/api/cart/count');
      const data = await res.json();
      this._updateBadge(data.count);
    } catch (err) { /* silencioso */ }
  },

  _updateBadge(count) {
    if (!this.badge) return;
    this.badge.textContent = count;
    this.badge.style.display = count > 0 ? 'flex' : 'none';
  },

  _animateBadge() {
    if (!this.badge) return;
    this.badge.classList.add('bump');
    setTimeout(() => this.badge.classList.remove('bump'), 300);
  },

  _showFeedback(btn, text) {
    if (!btn) return;
    const original = btn.textContent;
    btn.textContent = text;
    btn.style.background = 'rgba(100, 200, 120, 0.2)';
    setTimeout(() => {
      btn.textContent = original;
      btn.style.background = '';
    }, 1500);
  }
};

document.addEventListener('DOMContentLoaded', () => Cart.init());
