// B Printing and Wraps - mobile menu, scroll reveals, gallery filter
// Mobile menu
const burger = document.querySelector('.burger');
if (burger) {
  const toggle = (open) => document.body.classList.toggle('menu-open', open);
  burger.addEventListener('click', () => toggle(!document.body.classList.contains('menu-open')));
  document.querySelectorAll('.mobile-menu a').forEach(a => a.addEventListener('click', () => toggle(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') toggle(false); });
}

// Scroll reveals
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Gallery filter
const filters = document.querySelectorAll('.gfilter');
if (filters.length) {
  const tiles = document.querySelectorAll('#gal .tile');
  filters.forEach(btn => btn.addEventListener('click', () => {
    filters.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cat = btn.getAttribute('data-cat');
    tiles.forEach(t => t.classList.toggle('hide', cat !== 'all' && t.getAttribute('data-cat') !== cat));
  }));
}
