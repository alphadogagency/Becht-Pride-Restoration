/* Exercise the actual shipped scripts without dialing a phone or firing ads. */
import { readFileSync } from 'node:fs';
import { strict as assert } from 'node:assert';
import { runInNewContext } from 'node:vm';
const root = new URL('../site-v2/', import.meta.url);
const read = name => readFileSync(new URL(name, root), 'utf8');
const classes = () => ({ values: new Set(), add(v) { this.values.add(v); }, toggle(v, on) { on ? this.values.add(v) : this.values.delete(v); } });
let variantsChecked = 0;

for (const slug of ['ppc-remodeling', 'ppc-restoration', 'ppc-insurance']) {
  const html = read(`${slug}.html`);
  const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  const boot = { window: {}, document: { documentElement: { dataset: {} } }, location: { search: '' }, URLSearchParams };
  runInNewContext(scripts[0], boot);
  const config = boot.window.bechtLanding;
  for (const svc of [...Object.keys(config.variants), '', 'unknown', '__proto__', 'constructor', '<img src=x onerror=alert(1)>']) {
    const textNode = text => ({ textContent: text });
    const title = { textContent: '', replaceChildren(...nodes) { this.textContent = nodes.map(n => n.textContent).join(''); } };
    const sub = {};
    const cards = [...html.matchAll(/<article class="service-card" data-matches="([^"]*)"/g)].map(m => ({ dataset: { matches: m[1] }, classList: classes() }));
    const grid = { children: cards, prepend(card) { this.children = [card, ...this.children.filter(c => c !== card)]; } };
    const context = { window: {}, location: { search: `?svc=${encodeURIComponent(svc)}&gclid=example` }, URLSearchParams,
      document: { documentElement: { dataset: {} }, getElementById: id => id === 'hero-title' ? title : sub,
        createElement: () => textNode(''), createTextNode: textNode, querySelector: () => grid } };
    scripts.forEach(script => runInNewContext(script, context));
    const valid = Object.hasOwn(config.variants, svc);
    const expected = valid ? svc : config.default;
    assert.equal(context.document.documentElement.dataset.service, expected);
    assert.equal(title.textContent, config.variants[expected][0]);
    assert.equal(sub.textContent, config.variants[expected][2]);
    const matched = cards.find(c => c.dataset.matches.split(' ').includes(svc));
    if (valid && matched) assert.equal(grid.children[0], matched);
    if (!valid) assert.equal(grid.children[0], cards[0]);
    assert.equal(context.location.search, `?svc=${encodeURIComponent(svc)}&gclid=example`);
    variantsChecked++;
  }
}

const listeners = {}, documentListeners = {}, observers = [];
const header = { classList: classes() }, bar = { classList: classes(), setAttribute(k,v) { this[k] = v; } }, final = {};
class Observer { constructor(callback) { this.callback = callback; observers.push(this); } observe(target) { this.target = target; } }
const context = { window: { bechtLanding: { id: 'remodeling', service: 'kitchen' }, scrollY: 0, IntersectionObserver: Observer, addEventListener: (k,v) => listeners[k] = v },
  document: { querySelector: s => ({ '.site-header':header, '.sticky-call':bar, '#final-call':final })[s], addEventListener: (k,v) => documentListeners[k] = v },
  IntersectionObserver: Observer, matchMedia: () => ({ matches:true }), requestAnimationFrame: fn => fn() };
runInNewContext(read('ppc/landing.js'), context);
assert.equal(bar.inert, true);
context.window.scrollY = 201; listeners.scroll();
assert.equal(bar.classList.values.has('visible'), true);
assert.equal(bar.inert, false);
observers[0].callback([{isIntersecting:true}]);
assert.equal(bar.classList.values.has('visible'), false);
assert.equal(bar['aria-hidden'], 'true');
observers[0].callback([{isIntersecting:false}]);
assert.equal(bar.inert, false);
context.window.scrollY = 0; listeners.scroll();
assert.equal(bar.inert, true);
documentListeners.click({ target: { closest: () => null } });
assert.equal(context.window.dataLayer, undefined);
const link = { dataset: { cta:'hero' }, getAttribute: () => 'tel:+14632384357' };
documentListeners.click({ target: { closest: () => link }, preventDefault() { throw new Error('Dialer must not be blocked'); } });
assert.equal(context.window.dataLayer.length, 1);
assert.deepEqual(JSON.parse(JSON.stringify(context.window.dataLayer[0])), {event:'click_to_call',landing_page:'remodeling',service:'kitchen',cta_location:'hero',link_url:'tel:+14632384357'});
console.log(`Passed ${variantsChecked} valid/invalid variant cases, reordering, safe fallback, sticky call states, and call-click payload.`);
