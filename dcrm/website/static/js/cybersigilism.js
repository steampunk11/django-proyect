/**
 * CYBERSIGILISM CRM — Animations & Interactions
 * Handles: particle canvas, glitch effects, fade-in observer, cursor trail,
 *          table row entrance, sigil hover sparks, counter animation.
 */

;(function () {
  'use strict';

  /* ── CONFIG ────────────────────────────────────────────────── */
  const CFG = {
    particles: {
      count:      60,
      color:      '#8350C4',
      colorAlt:   '#7392B5',
      minRadius:  1,
      maxRadius:  3,
      minSpeed:   0.08,
      maxSpeed:   0.35,
      connectDist:130,
      connectAlpha:0.18,
    },
    glitch: {
      interval: 6500,   // ms between random glitch bursts
      duration: 300,
    },
    fadeInDelay: 80,    // ms stagger between observed elements
    cursorTrail: {
      enabled: true,
      maxDots: 20,
      color:  'rgba(131,80,196,',
    },
  };

  /* ══════════════════════════════════════════════════════════
     1. PARTICLE CANVAS BACKGROUND
  ══════════════════════════════════════════════════════════ */
  function initParticles() {
    const canvas = document.getElementById('csig-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let W, H, particles = [], raf;

    function resize() {
      W = canvas.width  = window.innerWidth;
      H = canvas.height = window.innerHeight;
    }

    function rand(min, max) { return Math.random() * (max - min) + min; }

    class Particle {
      constructor() { this.reset(true); }

      reset(init) {
        const c = CFG.particles;
        this.x  = rand(0, W);
        this.y  = init ? rand(0, H) : -10;
        this.r  = rand(c.minRadius, c.maxRadius);
        this.vx = rand(-c.maxSpeed, c.maxSpeed);
        this.vy = rand(c.minSpeed,  c.maxSpeed * 0.6);
        this.alpha = rand(0.3, 0.85);
        this.color = Math.random() > 0.5 ? c.color : c.colorAlt;
        // Occasional 4-point star shape flag
        this.isStar = Math.random() < 0.18;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;
        if (this.y > H + 10 || this.x < -10 || this.x > W + 10) this.reset(false);
      }

      draw() {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.fillStyle   = this.color;
        ctx.shadowColor = this.color;
        ctx.shadowBlur  = 6;

        if (this.isStar) {
          drawSigilStar(ctx, this.x, this.y, this.r * 2.2);
        } else {
          ctx.beginPath();
          ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
          ctx.fill();
        }
        ctx.restore();
      }
    }

    function drawSigilStar(ctx, cx, cy, size) {
      // 4-pointed star (cybersigilism style)
      const s = size;
      ctx.beginPath();
      ctx.moveTo(cx,      cy - s);
      ctx.lineTo(cx + s*0.25, cy - s*0.25);
      ctx.lineTo(cx + s,  cy);
      ctx.lineTo(cx + s*0.25, cy + s*0.25);
      ctx.lineTo(cx,      cy + s);
      ctx.lineTo(cx - s*0.25, cy + s*0.25);
      ctx.lineTo(cx - s,  cy);
      ctx.lineTo(cx - s*0.25, cy - s*0.25);
      ctx.closePath();
      ctx.fill();
    }

    function drawConnections() {
      const c = CFG.particles;
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < c.connectDist) {
            const alpha = c.connectAlpha * (1 - dist / c.connectDist);
            ctx.save();
            ctx.globalAlpha = alpha;
            ctx.strokeStyle = c.color;
            ctx.lineWidth   = 0.5;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
            ctx.restore();
          }
        }
      }
    }

    function loop() {
      ctx.clearRect(0, 0, W, H);
      particles.forEach(p => { p.update(); p.draw(); });
      drawConnections();
      raf = requestAnimationFrame(loop);
    }

    resize();
    for (let i = 0; i < CFG.particles.count; i++) particles.push(new Particle());

    window.addEventListener('resize', () => {
      resize();
      cancelAnimationFrame(raf);
      loop();
    });

    loop();
  }

  /* ══════════════════════════════════════════════════════════
     2. SCROLL FADE-IN (Intersection Observer)
  ══════════════════════════════════════════════════════════ */
  function initFadeIn() {
    const elements = document.querySelectorAll('.csig-fade-in');
    if (!elements.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, idx) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.classList.add('visible');
          }, idx * CFG.fadeInDelay);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });

    elements.forEach(el => observer.observe(el));
  }

  /* ══════════════════════════════════════════════════════════
     3. TABLE ROW STAGGER ENTRANCE
  ══════════════════════════════════════════════════════════ */
  function initTableStagger() {
    const rows = document.querySelectorAll('.csig-table tbody tr, .table tbody tr');
    rows.forEach((row, i) => {
      row.style.opacity   = '0';
      row.style.transform = 'translateX(-16px)';
      row.style.transition = `opacity 0.35s ease ${i * 45}ms, transform 0.35s ease ${i * 45}ms`;
      setTimeout(() => {
        row.style.opacity   = '1';
        row.style.transform = 'translateX(0)';
      }, 120 + i * 45);
    });
  }

  /* ══════════════════════════════════════════════════════════
     4. GLITCH TEXT EFFECT
  ══════════════════════════════════════════════════════════ */
  function initGlitch() {
    const targets = document.querySelectorAll('.csig-glitch, h1, h2');

    function triggerGlitch(el) {
      const text = el.textContent || el.innerText;
      el.setAttribute('data-text', text);
      el.classList.add('csig-glitch', 'active');
      // Remove 'active' after animation, then clean up 'csig-glitch' so
      // the pseudo-element forwards-fill doesn't leave the element shifted.
      setTimeout(() => {
        el.classList.remove('active');
        setTimeout(() => el.classList.remove('csig-glitch'), 50);
      }, CFG.glitch.duration);
    }

    function scheduleRandom() {
      targets.forEach(el => {
        if (Math.random() < 0.4) triggerGlitch(el);
      });
      setTimeout(scheduleRandom, CFG.glitch.interval + rand(-1500, 1500));
    }

    function rand(min, max) { return Math.random() * (max - min) + min; }

    // Initial delay
    setTimeout(scheduleRandom, 3000);

    // Hover glitch on nav links and brand
    document.querySelectorAll('.csig-nav-link, .csig-brand').forEach(el => {
      el.addEventListener('mouseenter', () => {
        const target = el.querySelector('.brand-text') || el;
        triggerGlitch(target);
      });
    });
  }

  /* ══════════════════════════════════════════════════════════
     5. CURSOR TRAIL
  ══════════════════════════════════════════════════════════ 
  function initCursorTrail() {
    if (!CFG.cursorTrail.enabled) return;
    // Only on non-touch devices
    if (window.matchMedia('(hover: none)').matches) return;

    const dots = [];
    const maxDots = CFG.cursorTrail.maxDots;
    const color   = CFG.cursorTrail.color;

    for (let i = 0; i < maxDots; i++) {
      const dot = document.createElement('div');
      dot.style.cssText = `
        position: fixed;
        width: ${4 + (maxDots - i) * 0.4}px;
        height: ${4 + (maxDots - i) * 0.4}px;
        background: ${color}${(0.6 * (i / maxDots)).toFixed(2)});
        border-radius: 50%;
        pointer-events: none;
        z-index: 9999;
        top: -20px; left: -20px;
        transform: translate(-50%, -50%);
        transition: top 0.${12 + i * 3}s ease, left 0.${12 + i * 3}s ease;
        mix-blend-mode: screen;
      `;
      document.body.appendChild(dot);
      dots.push(dot);
    }

    document.addEventListener('mousemove', e => {
      dots.forEach(dot => {
        dot.style.top  = e.clientY + 'px';
        dot.style.left = e.clientX + 'px';
      });
    });

    document.addEventListener('mouseleave', () => {
      dots.forEach(dot => { dot.style.top = '-20px'; dot.style.left = '-20px'; });
    });
  }
  */
  /* ══════════════════════════════════════════════════════════
     6. SIGIL HOVER SPARK (button / link ripple)
  ══════════════════════════════════════════════════════════ */
  function initRipple() {
    document.querySelectorAll('.btn, button').forEach(btn => {
      btn.addEventListener('click', function (e) {
        const rect   = this.getBoundingClientRect();
        const ripple = document.createElement('span');
        const size   = Math.max(rect.width, rect.height) * 1.8;
        const x      = e.clientX - rect.left - size / 2;
        const y      = e.clientY - rect.top  - size / 2;

        ripple.style.cssText = `
          position: absolute;
          width: ${size}px;
          height: ${size}px;
          border-radius: 50%;
          background: rgba(131, 80, 196, 0.3);
          top: ${y}px;
          left: ${x}px;
          pointer-events: none;
          animation: csigRipple 0.55s ease-out forwards;
        `;

        this.style.position = 'relative';
        this.style.overflow = 'hidden';
        this.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
      });
    });

    // Inject @keyframes if not already present
    if (!document.getElementById('csig-ripple-style')) {
      const style = document.createElement('style');
      style.id = 'csig-ripple-style';
      style.textContent = `
        @keyframes csigRipple {
          0%   { transform: scale(0); opacity: 1; }
          100% { transform: scale(1); opacity: 0; }
        }
      `;
      document.head.appendChild(style);
    }
  }

  /* ══════════════════════════════════════════════════════════
     7. ANIMATED PAGE TITLE (typing caret effect on h1)
  ══════════════════════════════════════════════════════════ */
  function initTypewriterTitle() {
    const h1 = document.querySelector('.csig-page-header h1, .csig-login-box h1, .csig-login-box h2');
    if (!h1) return;

    const original = h1.textContent.trim();
    h1.textContent = '';
    h1.style.borderRight = '3px solid var(--color-deep-lilac)';
    h1.style.display = 'inline-block';

    let i = 0;
    const speed = 45;

    function type() {
      if (i < original.length) {
        h1.textContent += original[i++];
        setTimeout(type, speed);
      } else {
        // Blinking caret stops after 3s
        setTimeout(() => { h1.style.borderRight = 'none'; }, 3000);
      }
    }

    // Delay slightly for visual impact
    setTimeout(type, 400);
  }

  /* ══════════════════════════════════════════════════════════
     8. NAVBAR SCROLL EFFECT
  ══════════════════════════════════════════════════════════ */
  function initNavbarScroll() {
    const navbar = document.querySelector('.csig-navbar, .navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
      if (window.scrollY > 30) {
        navbar.style.boxShadow = '0 4px 40px rgba(131, 80, 196, 0.35)';
      } else {
        navbar.style.boxShadow = '0 2px 30px rgba(131, 80, 196, 0.25)';
      }
    }, { passive: true });
  }

  /* ══════════════════════════════════════════════════════════
     9. FORM FIELD FOCUS LABEL FLOAT
  ══════════════════════════════════════════════════════════ */
  function initInputEffects() {
    document.querySelectorAll('input, select, textarea').forEach(input => {
      input.addEventListener('focus', () => {
        const label = input.previousElementSibling;
        if (label && (label.tagName === 'LABEL' || label.classList.contains('csig-label'))) {
          label.style.color = 'var(--color-deep-lilac)';
          label.style.textShadow = '0 0 8px rgba(131,80,196,0.5)';
          label.style.transition = 'color 0.3s ease, text-shadow 0.3s ease';
        }
      });
      input.addEventListener('blur', () => {
        const label = input.previousElementSibling;
        if (label && (label.tagName === 'LABEL' || label.classList.contains('csig-label'))) {
          label.style.color = '';
          label.style.textShadow = '';
        }
      });
    });
  }

  /* ══════════════════════════════════════════════════════════
     10. ALERT AUTO-DISMISS
  ══════════════════════════════════════════════════════════ */
  function initAlertDismiss() {
    document.querySelectorAll('.alert').forEach(alert => {
      setTimeout(() => {
        alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        alert.style.opacity    = '0';
        alert.style.transform  = 'translateY(-10px)';
        setTimeout(() => alert.remove(), 500);
      }, 5000);
    });
  }

  /* ══════════════════════════════════════════════════════════
     INIT — DOMContentLoaded
  ══════════════════════════════════════════════════════════ */
  document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    initFadeIn();
    initTableStagger();
    initGlitch();
    initRipple();
    initTypewriterTitle();
    initNavbarScroll();
    initInputEffects();
    initAlertDismiss();
  });

})();
