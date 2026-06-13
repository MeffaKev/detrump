const STORAGE_KEY = 'detrump_enabled';
const toggle = document.getElementById('toggle');
const status = document.getElementById('status');

chrome.storage.local.get(STORAGE_KEY, (result) => {
  const enabled = result[STORAGE_KEY] !== false;
  toggle.checked = enabled;
  updateStatus(enabled);
});

toggle.addEventListener('change', () => {
  const enabled = toggle.checked;
  chrome.storage.local.set({ [STORAGE_KEY]: enabled });
  updateStatus(enabled);

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]) {
      chrome.tabs.sendMessage(tabs[0].id, { type: 'SET_ENABLED', enabled });
    }
  });
});

function updateStatus(enabled) {
  status.textContent = enabled ? 'Active on this page' : 'Paused — images visible';
  status.style.color = enabled ? '#888' : '#e63946';
}
