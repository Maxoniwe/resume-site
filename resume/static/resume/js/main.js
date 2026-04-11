'use strict';

// ── Constants ─────────────────────────────────────────────────────────────────
const NAV_HEIGHT   = 64;
const STAGGER_STEP = 80; // ms delay between staggered elements

// ── Utils ─────────────────────────────────────────────────────────────────────
const $  = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

function prefersReducedMotion() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

// ── Navbar scroll state ───────────────────────────────────────────────────────
function initNavbar() {
  const nav = $('.nav');
  if (!nav) return;

  function update() {
    nav.classList.toggle('scrolled', window.scrollY > 10);
  }

  update(); // set correct state on load (e.g. page refresh mid-scroll)
  window.addEventListener('scroll', update, { passive: true });
}

// ── Mobile menu ───────────────────────────────────────────────────────────────
function initMobileMenu() {
  const toggle = $('.nav-toggle');
  const menu   = $('.nav-menu');
  if (!toggle || !menu) return;

  function openMenu() {
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Закрыть меню');
    menu.setAttribute('aria-hidden', 'false');
    document.body.classList.add('menu-open');
  }

  function closeMenu() {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Открыть меню');
    menu.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('menu-open');
  }

  toggle.addEventListener('click', () => {
    toggle.getAttribute('aria-expanded') === 'true' ? closeMenu() : openMenu();
  });

  // Close on nav link click
  $$('.nav-menu-link', menu).forEach(link => {
    link.addEventListener('click', closeMenu);
  });

  // Close on Escape key
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      toggle.focus();
    }
  });
}

// ── Scroll reveal ─────────────────────────────────────────────────────────────
function initReveal() {
  const elements = $$('.reveal');
  if (!elements.length) return;

  // Set stagger delays before observer fires (so CSS transition picks them up)
  elements.forEach(el => {
    const index = parseInt(el.dataset.revealIndex || '0', 10);
    const delay = prefersReducedMotion() ? 0 : index * STAGGER_STEP;
    el.style.setProperty('--reveal-delay', `${delay}ms`);
  });

  if (prefersReducedMotion()) {
    // Show all immediately — CSS already handles the overrides
    elements.forEach(el => el.classList.add('visible'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.08,
    rootMargin: `-${NAV_HEIGHT}px 0px -32px 0px`
  });

  elements.forEach(el => observer.observe(el));
}

// ── Active nav highlight ──────────────────────────────────────────────────────
function initActiveNav() {
  const sections = $$('section[id]');
  const navLinks = $$('.nav-link');
  if (!sections.length || !navLinks.length) return;

  const setActive = (id) => {
    navLinks.forEach(a => {
      const matches = a.getAttribute('href') === `#${id}`;
      a.classList.toggle('active', matches);
    });
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        setActive(entry.target.id);
      }
    });
  }, {
    // Top margin: just below the navbar. Bottom margin: trigger in upper half of viewport.
    rootMargin: `-${NAV_HEIGHT + 16}px 0px -55% 0px`,
    threshold: 0
  });

  sections.forEach(s => observer.observe(s));
}

// ── Typing effect ─────────────────────────────────────────────────────────────
function initTyping(el) {
  const text = el.dataset.typingText || '';
  if (!text) return;

  // If user prefers no motion — just show the full text statically
  if (prefersReducedMotion()) {
    el.textContent = text;
    return;
  }

  const TYPE_SPEED   = 80;   // ms per character when typing
  const DELETE_SPEED = 40;   // ms per character when deleting
  const PAUSE_END    = 2400; // ms pause at end of word
  const PAUSE_START  = 600;  // ms pause before retyping

  let i = 0;
  let deleting = false;

  function tick() {
    if (!deleting) {
      el.textContent = text.slice(0, ++i);
      if (i === text.length) {
        setTimeout(() => { deleting = true; tick(); }, PAUSE_END);
        return;
      }
      setTimeout(tick, TYPE_SPEED);
    } else {
      el.textContent = text.slice(0, --i);
      if (i === 0) {
        deleting = false;
        setTimeout(tick, PAUSE_START);
        return;
      }
      setTimeout(tick, DELETE_SPEED);
    }
  }

  tick();
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initMobileMenu();
  initReveal();
  initActiveNav();

  const typingEl = $('.typing-target');
  if (typingEl) initTyping(typingEl);
});
