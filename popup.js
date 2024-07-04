document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get('status', (data) => {
    document.getElementById('status').textContent = data.status || 'Page Waiting...';
  });
});
