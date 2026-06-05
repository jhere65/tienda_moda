/* ============================================================
   slider.js — Carrusel horizontal con drag y botones
   ============================================================ */

class Slider {
  constructor(wrapperSelector) {
    this.wrapper = document.querySelector(wrapperSelector);
    if (!this.wrapper) return;

    this.track   = this.wrapper.querySelector('.slider-track');
    this.btnPrev = this.wrapper.querySelector('.slider-btn--prev');
    this.btnNext = this.wrapper.querySelector('.slider-btn--next');

    // Estado del drag
    this.isDragging  = false;
    this.startX      = 0;
    this.startScroll = 0;
    this.velocity    = 0;
    this.lastX       = 0;
    this.rafID       = null;

    this._bindEvents();
  }

  _bindEvents() {
    // Botones de navegación
    if (this.btnPrev) {
      this.btnPrev.addEventListener('click', () => this._slide(-1));
    }
    if (this.btnNext) {
      this.btnNext.addEventListener('click', () => this._slide(1));
    }

    // Drag con mouse
    this.track.addEventListener('mousedown',  e => this._onDragStart(e));
    this.track.addEventListener('mousemove',  e => this._onDragMove(e));
    this.track.addEventListener('mouseup',    ()  => this._onDragEnd());
    this.track.addEventListener('mouseleave', ()  => this._onDragEnd());

    // Touch (móvil)
    this.track.addEventListener('touchstart', e => this._onDragStart(e.touches[0]), { passive: true });
    this.track.addEventListener('touchmove',  e => this._onDragMove(e.touches[0]),  { passive: true });
    this.track.addEventListener('touchend',   ()  => this._onDragEnd());

    // Prevenir click en links durante drag
    this.track.addEventListener('click', e => {
      if (Math.abs(this.startX - (e.clientX || 0)) > 5) {
        e.preventDefault();
      }
    });
  }

  _slide(direction) {
    const cardWidth = this._getCardWidth();
    this.track.scrollBy({ left: cardWidth * direction * 2, behavior: 'smooth' });
  }

  _getCardWidth() {
    const firstCard = this.track.querySelector('.product-card');
    if (!firstCard) return 320;
    const style = getComputedStyle(this.track);
    const gap   = parseFloat(style.gap) || 24;
    return firstCard.offsetWidth + gap;
  }

  _onDragStart(e) {
    this.isDragging  = true;
    this.startX      = e.clientX;
    this.lastX       = e.clientX;
    this.startScroll = this.track.scrollLeft;
    this.velocity    = 0;
    this.track.style.cursor = 'grabbing';
    cancelAnimationFrame(this.rafID);
  }

  _onDragMove(e) {
    if (!this.isDragging) return;
    const dx        = e.clientX - this.startX;
    this.velocity   = e.clientX - this.lastX;
    this.lastX      = e.clientX;
    this.track.scrollLeft = this.startScroll - dx;
  }

  _onDragEnd() {
    if (!this.isDragging) return;
    this.isDragging = false;
    this.track.style.cursor = 'grab';
    this._applyMomentum();
  }

  _applyMomentum() {
    let velocity = this.velocity * -2.5;

    const step = () => {
      if (Math.abs(velocity) < 0.5) return;
      this.track.scrollLeft += velocity;
      velocity *= 0.92;
      this.rafID = requestAnimationFrame(step);
    };

    this.rafID = requestAnimationFrame(step);
  }
}

// Inicializar todos los sliders de la página
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.slider-wrapper').forEach(wrapper => {
    new Slider(null);
  });

  // Inicialización directa por wrapper
  new Slider('#featured-slider');
});
