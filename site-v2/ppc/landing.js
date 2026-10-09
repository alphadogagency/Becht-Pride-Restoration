/* Shared behavior for the standalone call-only landing pages. */
(() => {
  'use strict';
  const page = window.bechtLanding || {};
  const header = document.querySelector('.site-header');
  const bar = document.querySelector('.sticky-call');
  const final = document.querySelector('#final-call');
  let finalVisible = false;
  let ticking = false;

  function updateScroll() {
    header?.classList.toggle('is-scrolled', window.scrollY > 50);
    const show = window.scrollY > 200 && !finalVisible;
    if (bar) {
      bar.classList.toggle('visible', show);
      bar.inert = !show;
      bar.setAttribute('aria-hidden', String(!show));
    }
    ticking = false;
  }
  window.addEventListener('scroll', () => {
    if (!ticking) { ticking = true; requestAnimationFrame(updateScroll); }
  }, { passive: true });
  window.addEventListener('resize', updateScroll, { passive: true });
  if (final && 'IntersectionObserver' in window) {
    new IntersectionObserver(entries => {
      finalVisible = entries[0].isIntersecting;
      updateScroll();
    }, { threshold: 0 }).observe(final);
  }
  updateScroll();

  // A click expresses intent to call; it is not proof of a connected call.
  // No Google Ads/GA4 ID is invented and no external tracker is loaded here.
  // The account manager can connect this event to the approved GTM container.
  document.addEventListener('click', event => {
    const link = event.target.closest('a.call-cta');
    if (!link) return;
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'click_to_call',
      landing_page: page.id,
      service: page.service,
      cta_location: link.dataset.cta,
      link_url: link.getAttribute('href')
    });
    // Do not preventDefault, delay the dialer, persist ad IDs, or rewrite the URL.
  });

  // Progressive enhancement: all content remains visible without JavaScript.
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const sections = [...document.querySelectorAll('.reveal')];
    sections.forEach(section => {
      if (section.getBoundingClientRect().top < window.innerHeight) section.classList.add('is-visible');
    });
    document.documentElement.classList.add('motion-ready');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
      });
    }, { rootMargin: '80px 0px', threshold: 0.02 });
    sections.forEach(section => observer.observe(section));
  }
})();
