# DeTrump

A Chrome extension that automatically blurs Donald Trump's face on any web page.

## How it works

DeTrump scans every image on a page and blurs any that are identified as being of Donald Trump. Detection checks:

- Image `alt` text
- Image `src` URL
- `<figcaption>` captions
- `aria-label` attributes on parent elements
- Anchor `href` links wrapping images

A [MutationObserver](https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver) watches for dynamically loaded images (infinite scroll, lazy loading, etc.) and blurs them as they appear.

**Click any blurred image** to temporarily reveal it. Click again to re-blur.

## Installation

Chrome Web Store submission is pending. In the meantime, load it manually:

1. Download or clone this repo
2. Open Chrome and go to `chrome://extensions`
3. Enable **Developer mode** (toggle in the top-right corner)
4. Click **Load unpacked**
5. Select the `detrump` folder

The extension activates immediately on all pages.

## Usage

| Action | Result |
|---|---|
| Browse any page | Trump images are blurred automatically |
| Click a blurred image | Reveals the image temporarily |
| Click again | Re-blurs the image |
| Click the extension icon | Opens the popup toggle |
| Toggle in popup | Enable or disable blurring globally |

## Limitations

Detection is text-based, so it works best on sites that properly label their images (most major news sites, Google Image Search, etc.). Images with no alt text or surrounding context mentioning Trump will not be caught. True face-recognition support would require bundling a ~30 MB ML model — that may come in a future version.

## Development

The extension is built with vanilla JavaScript and the Chrome Extensions Manifest V3 API — no build step required.

```
detrump/
├── manifest.json   # Extension config and permissions
├── content.js      # Core detection and blur logic (runs on every page)
├── popup.html      # Toggle UI
├── popup.js        # Popup logic
└── icons/          # Extension icons
```
