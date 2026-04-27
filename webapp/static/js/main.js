/* LeakSeeker main.js */
const BLOCKED_UPLOAD_EXTENSIONS = new Set(['.mp3', '.mp4', '.gif', '.png', '.jpeg', '.jpg']);
function uploadExt(name) {
  const i = (name || '').lastIndexOf('.');
  return i >= 0 ? name.slice(i).toLowerCase() : '';
}
function blockedUploads(files) {
  return Array.from(files || []).filter(f => BLOCKED_UPLOAD_EXTENSIONS.has(uploadExt(f.name)));
}
function rejectBlockedUploads(files) {
  const blocked = blockedUploads(files);
  if (!blocked.length) return false;
  alert('Blocked file type: ' + blocked.map(f => f.name).join(', '));
  return true;
}
// ============================================================
// Mode toggle (upload vs path)
// ============================================================
function setMode(mode) {
  const uploadSection = document.getElementById('upload-section');
  const pathSection = document.getElementById('path-section');
  const githubSection = document.getElementById('github-section');
  const modeInput = document.getElementById('scan_mode');
  const buttons = document.querySelectorAll('.mode-btn');

  if (!uploadSection) return;

  buttons.forEach(b => b.classList.toggle('active', b.dataset.mode === mode));

  uploadSection.style.display = mode === 'upload' ? '' : 'none';
  pathSection.style.display = mode === 'path' ? '' : 'none';
  if (githubSection) githubSection.style.display = mode === 'github' ? '' : 'none';

  modeInput.value = mode;
}

// ============================================================
// Drag-and-drop file zone
// ============================================================
(function initDropZone() {
  const zone = document.getElementById('drop-zone');
  const fileInput = document.getElementById('upload_file');
  if (!zone || !fileInput) return;

  zone.addEventListener('dragover', e => {
    e.preventDefault();
    zone.classList.add('drag-over');
  });

  zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));

  zone.addEventListener('drop', e => {
    e.preventDefault();
    zone.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length) {
      const dt = new DataTransfer();
      for (const f of files) dt.items.add(f);
      fileInput.files = dt.files;
      showFileList(fileInput.files);
    }
  });

  fileInput.addEventListener('change', () => {
    if (fileInput.files.length) { if (rejectBlockedUploads(fileInput.files)) { clearFiles(); return; } showFileList(fileInput.files); }
  });
})();

function showFileList(files) {
  const zone = document.getElementById('drop-zone');
  const listContainer = document.getElementById('file-list');
  const listItems = document.getElementById('file-list-items');
  const countLabel = document.getElementById('file-list-count');
  if (!zone || !listContainer || !listItems || !countLabel) return;

  zone.style.display = 'none';
  listContainer.style.display = '';

  const count = files.length;
  countLabel.textContent = count === 1 ? '1 file selected' : `${count} files selected`;

  listItems.innerHTML = '';
  Array.from(files).forEach(f => {
    const li = document.createElement('li');
    li.className = 'file-list-item';
    const sizeKB = (f.size / 1024).toFixed(1);
    li.innerHTML = `<span class="file-item-icon">[FILE]</span><span class="file-item-name">${f.name}</span><span class="file-item-size">${sizeKB} KB</span>`;
    listItems.appendChild(li);
  });
}

function clearFiles() {
  const zone = document.getElementById('drop-zone');
  const listContainer = document.getElementById('file-list');
  const fileInput = document.getElementById('upload_file');
  if (!zone || !listContainer || !fileInput) return;
  fileInput.value = '';
  zone.style.display = '';
  listContainer.style.display = 'none';
}

// ============================================================
// Scan form -- loading state
// ============================================================
(function initScanForm() {
  const form = document.getElementById('scan-form');
  if (!form) return;

  form.addEventListener('submit', e => {
    const fileInput = document.getElementById('upload_file');
    if (fileInput && fileInput.files && rejectBlockedUploads(fileInput.files)) { e.preventDefault(); return; }
    const btn = document.getElementById('scan-btn');
    if (!btn) return;
    const btnText = btn.querySelector('.btn-text');
    const btnLoader = btn.querySelector('.btn-loader');
    const btnIcon = btn.querySelector('.btn-icon');
    if (btnText) btnText.style.display = 'none';
    if (btnLoader) btnLoader.style.display = 'inline-flex';
    if (btnIcon) btnIcon.style.display = 'none';
    btn.disabled = true;
  });
})();

// ============================================================
// Results -- filter by risk level or type
// ============================================================
let activeFilter = 'all';
let searchTerm = '';

function filterFindings(filter, btn) {
  activeFilter = filter;

  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');

  applyFilters();
}

function searchFindings(value) {
  searchTerm = value.toLowerCase().trim();
  applyFilters();
}

function applyFilters() {
  const cards = document.querySelectorAll('.finding-card');
  let visible = 0;

  cards.forEach(card => {
    const risk = card.dataset.risk || '';
    const type = card.dataset.type || '';
    const file = (card.dataset.file || '').toLowerCase();

    const matchesFilter = (
      activeFilter === 'all' ||
      activeFilter === risk ||
      (activeFilter === 'endpoint' && type === 'endpoint')
    );

    const matchesSearch = !searchTerm || (
      file.includes(searchTerm) ||
      type.toLowerCase().includes(searchTerm)
    );

    const show = matchesFilter && matchesSearch;
    card.style.display = show ? '' : 'none';
    if (show) visible++;
  });

  const noMatch = document.getElementById('no-match-msg');
  if (noMatch) noMatch.style.display = visible === 0 ? '' : 'none';
}

// ============================================================
// AI explanation panel (calls /api/explain)
// ============================================================
async function loadExplanation(btn, secretType, matchedText) {
  const card = btn.closest('.finding-card');
  if (!card) return;

  const panel = card.querySelector('.ai-panel');
  const content = card.querySelector('.ai-content');
  if (!panel || !content) return;

  // Toggle off
  if (panel.style.display !== 'none') {
    panel.style.display = 'none';
    btn.textContent = '[AI] Explain';
    return;
  }

  btn.textContent = '⏳ Loading...';
  btn.disabled = true;
  panel.style.display = '';
  content.textContent = 'Fetching analysis...';

  try {
    const resp = await fetch('/api/explain', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ secret_type: secretType, matched_text: matchedText })
    });

    const data = await resp.json();
    content.textContent = data.explanation || 'No analysis available.';
  } catch (err) {
    content.textContent = 'Could not load explanation.';
  } finally {
    btn.textContent = '[AI] Explain';
    btn.disabled = false;
  }
}

// ============================================================
// Animate risk meter bar on load
// ============================================================
(function animateRiskMeter() {
  const fill = document.querySelector('.risk-meter-fill');
  if (!fill) return;

  const target = parseFloat(fill.dataset.score || '0');
  fill.style.width = '0%';
  requestAnimationFrame(() => {
    setTimeout(() => {
      fill.style.width = target + '%';
    }, 100);
  });
})();

// ============================================================
// Stagger finding cards on load
// ============================================================
(function staggerCards() {
  document.querySelectorAll('.finding-card').forEach((card, i) => {
    card.style.animationDelay = `${i * 40}ms`;
  });
})();
