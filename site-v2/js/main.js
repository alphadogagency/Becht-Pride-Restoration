/* ==========================================================================
   Becht Pride Restoration and Remodeling — Main JS
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initHeader();
  initMobileNav();
  initSmoothScroll();
  initTestimonialSlider();
  initGallery();
  initContactForm();
  initScrollAnimations();
});

/* --- Header Scroll Effect --- */
function initHeader() {
  const header = document.querySelector('.header');
  if (!header) return;

  function updateHeader() {
    if (window.scrollY > 60) {
      header.classList.add('scrolled');
      header.classList.remove('transparent');
    } else if (header.dataset.transparent === 'true') {
      header.classList.remove('scrolled');
      header.classList.add('transparent');
    }
  }

  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });
}

/* --- Mobile Navigation --- */
function initMobileNav() {
  const toggle = document.querySelector('.menu-toggle');
  const mobileNav = document.querySelector('.mobile-nav');
  if (!toggle || !mobileNav) return;

  toggle.addEventListener('click', () => {
    toggle.classList.toggle('open');
    mobileNav.classList.toggle('open');
    document.body.style.overflow = mobileNav.classList.contains('open') ? 'hidden' : '';
  });

  mobileNav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      toggle.classList.remove('open');
      mobileNav.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
}

/* --- Smooth Scroll --- */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (targetId === '#') return;

      const target = document.querySelector(targetId);
      if (!target) return;

      e.preventDefault();
      const headerHeight = document.querySelector('.header')?.offsetHeight || 0;
      const top = target.getBoundingClientRect().top + window.scrollY - headerHeight - 20;

      window.scrollTo({ top, behavior: 'smooth' });
    });
  });
}

/* --- Testimonial Slider --- */
function initTestimonialSlider() {
  const slides = document.querySelectorAll('.testimonial-slide');
  const dots = document.querySelectorAll('.testimonial-dot');
  if (slides.length === 0) return;

  let current = 0;
  let autoplayTimer;

  function show(index) {
    slides.forEach(s => s.classList.remove('active'));
    dots.forEach(d => d.classList.remove('active'));
    current = (index + slides.length) % slides.length;
    slides[current].classList.add('active');
    if (dots[current]) dots[current].classList.add('active');
  }

  function startAutoplay() {
    autoplayTimer = setInterval(() => show(current + 1), 6000);
  }

  function resetAutoplay() {
    clearInterval(autoplayTimer);
    startAutoplay();
  }

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      show(i);
      resetAutoplay();
    });
  });

  show(0);
  startAutoplay();
}

/* --- Gallery & Lightbox --- */
function initGallery() {
  // Tab filtering
  const tabs = document.querySelectorAll('.gallery-tab');
  const items = document.querySelectorAll('.gallery-item');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const filter = tab.dataset.filter;

      items.forEach(item => {
        if (filter === 'all' || item.dataset.category === filter) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });

  // Lightbox
  const lightbox = document.querySelector('.lightbox');
  if (!lightbox) return;

  const lightboxImg = lightbox.querySelector('img');
  const closeBtn = lightbox.querySelector('.lightbox-close');
  const prevBtn = lightbox.querySelector('.lightbox-prev');
  const nextBtn = lightbox.querySelector('.lightbox-next');

  let visibleImages = [];
  let lightboxIndex = 0;

  function getVisibleImages() {
    return Array.from(items).filter(item => item.style.display !== 'none');
  }

  function openLightbox(index) {
    visibleImages = getVisibleImages();
    lightboxIndex = index;
    const img = visibleImages[lightboxIndex]?.querySelector('img');
    if (!img) return;
    lightboxImg.src = img.src;
    lightboxImg.alt = img.alt;
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
  }

  function showPrev() {
    lightboxIndex = (lightboxIndex - 1 + visibleImages.length) % visibleImages.length;
    const img = visibleImages[lightboxIndex]?.querySelector('img');
    if (img) {
      lightboxImg.src = img.src;
      lightboxImg.alt = img.alt;
    }
  }

  function showNext() {
    lightboxIndex = (lightboxIndex + 1) % visibleImages.length;
    const img = visibleImages[lightboxIndex]?.querySelector('img');
    if (img) {
      lightboxImg.src = img.src;
      lightboxImg.alt = img.alt;
    }
  }

  items.forEach((item, i) => {
    item.addEventListener('click', () => {
      const visible = getVisibleImages();
      const idx = visible.indexOf(item);
      openLightbox(idx >= 0 ? idx : 0);
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
  if (prevBtn) prevBtn.addEventListener('click', showPrev);
  if (nextBtn) nextBtn.addEventListener('click', showNext);

  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
  });

  document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('open')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') showPrev();
    if (e.key === 'ArrowRight') showNext();
  });
}

/* --- Contact Form Validation --- */
function initContactForm() {
  const form = document.querySelector('#contact-form');
  if (!form) return;

  const successEl = form.closest('.contact-form-wrapper')?.querySelector('.form-success');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    let valid = true;

    // Clear previous errors
    form.querySelectorAll('.form-group').forEach(g => g.classList.remove('has-error'));

    // Validate required fields
    const name = form.querySelector('#name');
    const email = form.querySelector('#email');
    const phone = form.querySelector('#phone');
    const message = form.querySelector('#message');

    if (name && !name.value.trim()) {
      setError(name, 'Please enter your name');
      valid = false;
    }

    if (email && !isValidEmail(email.value)) {
      setError(email, 'Please enter a valid email address');
      valid = false;
    }

    if (phone && !phone.value.trim()) {
      setError(phone, 'Please enter your phone number');
      valid = false;
    }

    if (message && !message.value.trim()) {
      setError(message, 'Please enter a message');
      valid = false;
    }

    if (valid) {
      const submitBtn = form.querySelector('.form-submit');
      const btnText = submitBtn.textContent;
      submitBtn.textContent = 'Sending...';
      submitBtn.disabled = true;

      const service = form.querySelector('#service');

      fetch('https://becht-pride.adalandings.com/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          slug: 'becht-pride',
          name: name.value.trim(),
          email: email.value.trim(),
          phone: phone.value.trim(),
          service: service ? service.value : '',
          message: message.value.trim(),
        }),
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            form.style.display = 'none';
            if (successEl) successEl.style.display = 'block';
          } else {
            submitBtn.textContent = btnText;
            submitBtn.disabled = false;
            alert('Something went wrong. Please try again or call us directly.');
          }
        })
        .catch(() => {
          submitBtn.textContent = btnText;
          submitBtn.disabled = false;
          alert('Something went wrong. Please try again or call us directly.');
        });
    }
  });
}

function setError(input, msg) {
  const group = input.closest('.form-group');
  if (!group) return;
  group.classList.add('has-error');
  const errorEl = group.querySelector('.error-msg');
  if (errorEl) errorEl.textContent = msg;
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

/* --- Scroll Animations --- */
function initScrollAnimations() {
  // Tag elements with reveal classes
  const revealMap = [
    { selector: '.section-header', cls: 'reveal' },
    { selector: '.services-grid', cls: 'stagger-children' },
    { selector: '.about-image', cls: 'reveal-left' },
    { selector: '.about-content', cls: 'reveal-right' },
    { selector: '.about-features', cls: 'stagger-children' },
    { selector: '.gallery-tabs', cls: 'reveal' },
    { selector: '.gallery-grid', cls: 'stagger-children' },
    { selector: '.testimonial-slider', cls: 'reveal' },
    { selector: '.contact-info', cls: 'reveal-left' },
    { selector: '.contact-form-wrapper', cls: 'reveal-right' },
    { selector: '.service-awards', cls: 'reveal' },
    { selector: '.cta-banner h2', cls: 'reveal' },
    { selector: '.cta-banner p', cls: 'reveal' },
    { selector: '.footer-grid', cls: 'stagger-children' },
    { selector: '.service-main', cls: 'reveal' },
    { selector: '.service-sidebar-card', cls: 'reveal-right' },
    { selector: '.service-gallery', cls: 'reveal' },
    { selector: '.service-gallery-grid', cls: 'stagger-children' },
  ];

  revealMap.forEach(({ selector, cls }) => {
    document.querySelectorAll(selector).forEach(el => {
      if (!el.classList.contains(cls)) el.classList.add(cls);
    });
  });

  // Observe all reveal elements
  const targets = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .stagger-children');
  if (!targets.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.15,
    rootMargin: '0px 0px -40px 0px'
  });

  targets.forEach(el => observer.observe(el));
}
