// Utility function: querySelector shorthand
const $ = selector => document.querySelector(selector);
// Utility function: querySelectorAll shorthand, returns a NodeList
const $$ = selector => document.querySelectorAll(selector);

const searchInput = $('#search-input');
const partsTableBody = $('#parts-table tbody');
const addPartBtn = $('#add-part-btn');
const editBtn = $('#edit-btn');
const deleteBtn = $('#delete-btn');
const showDeletedBtn = $('#show-deleted-btn')

// Populates Parts HTML table 
function renderParts(parts) {
  partsTableBody.innerHTML = '';

  parts.forEach(part => {
    partsTableBody.insertAdjacentHTML('beforeend', `
      <tr data-id="${part.id}">
        <td><input type="checkbox" class="row-select"></td>
        <td>${part.id}</td>
        <td>${part.description}</td>
        <td>${part.location}</td>
        <td>${part.date_created}</td>
      </tr>
    `);
  });
  attachSelectionListeners();
}

async function doSearch(q = '') {
  const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
  const parts = await res.json();
  renderParts(parts);
}

function updateSearch(query) {
    const newUrl = `${window.location.pathname}?q=${encodeURIComponent(query)}`;
    window.history.replaceState({ path: newUrl }, '', newUrl);
    doSearch(query)
}

searchInput.addEventListener('input', () => {
    const query = $('#search-input').value;
    updateSearch(query);
});

function updateActionButtons() {
    const selected = $$('.row-select:checked');
    editBtn.style.display = selected.length ===1 ? 'inline-block' : 'none';
    deleteBtn.style.display = selected.length ? 'inline-block' : 'none';
}

function attachSelectionListeners() {
  $$('.row-select').forEach(cb => {
    cb.addEventListener('change', () => {
      cb.closest('tr').classList.toggle('selected', cb.checked);
      updateActionButtons();
    });
  });
}

// Initial load
window.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const query = params.get ('q') || '';
    searchInput.value = query;
    doSearch(query);
});

addPartBtn.addEventListener("click", () => {
  const searchValue = searchInput?.value || "";
  const url = new URL("/parts/new", window.location.origin);
  url.searchParams.set("default_description", searchValue);
  sessionStorage.setItem('returnTo', window.location.href)
  window.location.href = url.toString();
});

editBtn.onclick = () => {
    const selectedRow = $('.row-select:checked').closest('tr');
    const id = selectedRow.dataset.id;
    sessionStorage.setItem('returnTo', window.location.href);
    window.location.href = `/update/${id}`;
};

showDeletedBtn.onclick = () => {
      window.location.href = "{{ url_for('parts.view_deleted') }}";
}

deleteBtn.onclick = () => {
  const idsToDelete = Array.from($$('.row-select:checked')).map(cb => cb.closest('tr').dataset.id);

  if (confirm(`Delete ${idsToDelete.length} part(s)?`)) {
    fetch('/parts/bulk-delete', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ ids: idsToDelete })
    }).then(r => r.ok ? doSearch(searchInput.value) : alert('Deletion failed'));
  }
};