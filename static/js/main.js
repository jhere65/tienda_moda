/* ============================================================
   main.js — Scripts generales de la tienda
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  // --- Navbar: efecto scroll ---
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    const onScroll = () => navbar.classList.toggle('scrolled', window.scrollY > 40);
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // --- Flash messages: auto-dismiss ---
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach(flash => {
    setTimeout(() => {
      flash.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      flash.style.opacity    = '0';
      flash.style.transform  = 'translateX(20px)';
      setTimeout(() => flash.remove(), 500);
    }, 4000);
  });

  // --- Animación de entrada para tarjetas de producto ---
  const observer = new IntersectionObserver(entries => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity    = '1';
          entry.target.style.transform  = 'translateY(0)';
        }, i * 60);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.product-card').forEach(card => {
    card.style.opacity   = '0';
    card.style.transform = 'translateY(24px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
  });

  // --- Animar stat cards del admin ---
  document.querySelectorAll('.stat-card__value').forEach(el => {
    const target = parseInt(el.textContent) || 0;
    if (target === 0 || isNaN(target)) return;
    let current = 0;
    const step  = Math.ceil(target / 30);
    const timer = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = current;
      if (current >= target) clearInterval(timer);
    }, 40);
  });

  // --- Confirmar eliminación de productos ---
  document.querySelectorAll('[data-confirm]').forEach(btn => {
    btn.addEventListener('click', e => {
      const msg = btn.dataset.confirm || '¿Estás seguro de esta acción?';
      if (!confirm(msg)) e.preventDefault();
    });
  });

});
