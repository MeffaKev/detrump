(function () {
  const STORAGE_KEY = 'detrump_enabled';
  const KEYWORDS = ['trump', 'donald j. trump', 'donald trump', 'president trump'];

  let enabled = true;

  function matchesKeyword(str) {
    if (!str) return false;
    const lower = str.toLowerCase();
    return KEYWORDS.some(kw => lower.includes(kw));
  }

  function isTrumpImage(img) {
    // Direct image attributes
    if (
      matchesKeyword(img.alt) ||
      matchesKeyword(img.title) ||
      matchesKeyword(img.getAttribute('aria-label')) ||
      matchesKeyword(img.src) ||
      matchesKeyword(img.dataset.src) ||
      matchesKeyword(img.dataset.lazySrc) ||
      matchesKeyword(img.dataset.originalSrc)
    ) {
      return true;
    }

    // figcaption inside the same <figure>
    const figure = img.closest('figure');
    if (figure) {
      const caption = figure.querySelector('figcaption');
      if (caption && matchesKeyword(caption.textContent)) return true;
    }

    // Check up to 3 ancestor elements for aria-label or data attributes
    let el = img.parentElement;
    for (let i = 0; i < 3; i++) {
      if (!el) break;
      if (
        matchesKeyword(el.getAttribute('aria-label')) ||
        matchesKeyword(el.getAttribute('data-alt'))
      ) {
        return true;
      }
      el = el.parentElement;
    }

    // Check <a> wrapping the image (some sites link to articles with trump in the href)
    const anchor = img.closest('a');
    if (anchor && matchesKeyword(anchor.getAttribute('href'))) return true;

    return false;
  }

  function blurImage(img) {
    if (img.dataset.detrumped) return;
    img.dataset.detrumped = 'true';

    const wrapper = document.createElement('span');
    wrapper.dataset.detrumpWrapper = 'true';
    wrapper.style.cssText = 'display:inline-block;position:relative;';

    img.parentNode.insertBefore(wrapper, img);
    wrapper.appendChild(img);

    img.style.filter = 'blur(20px)';
    img.style.transition = 'filter 0.3s ease';

    // Click to reveal temporarily
    wrapper.style.cursor = 'pointer';
    wrapper.title = 'DeTrump: click to reveal';
    wrapper.addEventListener('click', (e) => {
      if (img.dataset.revealed === 'true') {
        img.style.filter = 'blur(20px)';
        img.dataset.revealed = 'false';
        wrapper.title = 'DeTrump: click to reveal';
      } else {
        img.style.filter = 'none';
        img.dataset.revealed = 'true';
        wrapper.title = 'DeTrump: click to hide';
      }
      e.stopPropagation();
    });
  }

  function unblurAll() {
    document.querySelectorAll('img[data-detrumped]').forEach(img => {
      img.style.filter = '';
      img.style.transition = '';
      delete img.dataset.detrumped;
      delete img.dataset.revealed;

      // Unwrap if we wrapped it
      const wrapper = img.parentElement;
      if (wrapper && wrapper.dataset.detrumpWrapper) {
        wrapper.parentNode.insertBefore(img, wrapper);
        wrapper.remove();
      }
    });
  }

  function processImages() {
    if (!enabled) return;
    document.querySelectorAll('img:not([data-detrumped])').forEach(img => {
      if (isTrumpImage(img)) blurImage(img);
    });
  }

  const observer = new MutationObserver(() => processImages());

  function start() {
    processImages();
    observer.observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['src', 'alt'] });
  }

  // Listen for toggle messages from the popup
  chrome.runtime.onMessage.addListener((msg) => {
    if (msg.type === 'SET_ENABLED') {
      enabled = msg.enabled;
      if (enabled) {
        processImages();
      } else {
        unblurAll();
      }
    }
  });

  // Read stored preference then start
  chrome.storage.local.get(STORAGE_KEY, (result) => {
    enabled = result[STORAGE_KEY] !== false; // default on
    start();
  });
})();
