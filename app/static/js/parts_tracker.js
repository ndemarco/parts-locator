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

// Populates Parts HTML table.
function renderParts(parts) {
  const tbody = document.querySelector('#parts-table tbody');
  
  // Is there a table?
  if (!tbody) return;

  // Clear records from table
  tbody.innerHTML = '';

  parts.forEach(part => {
    tbody.insertAdjacentHTML('beforeend', `
      <tr data-id="${part.id}" class="parts-row">
        <td><input type="checkbox" class="row-select"></td>
        <td>${part.id}</td>
        <td>${part.description}</td>
        <td>${part.location}</td>
        <td>${part.date_created}</td>
      </tr>
    `);
  });
  // After rendering, wire up click handlers for the new rows
  bindRowEvents();
}


function bindRowEvents() {
  $$('.parts-row').forEach(row => {
    const checkbox = row.querySelector('.row-select');

    // Clicking the checkbox -> activate row & toggle selection
    checkbox.addEventListener('click', (e) => {
      e.stopPropagation();  // prevents row click from firing
      setActiveRow(row);
    });

    // Clicking anywhere on the row should highlight it
    row.addEventListener('click', () => {
      setActiveRow(row);
    });
  });
}

function setActiveRow(row) {
  $$('.parts-row').forEach(r => r.classList.remove('active-row'));
  row.classList.add('active-row');
}


async function doSearch(q = '') {
  const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
  if (!res.ok) {
    alert("Failed to fetch parts.");
    return;
  }
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

// Initial load
window.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const query = params.get ('q') || '';
    searchInput.value = query;
    doSearch(query);
});

// Handle Add Part clicks
addPartBtn.addEventListener("click", () => {
  const activeRow = $('.parts-row.active-row');
  if (activeRow) {
    const descriptionCell = activeRow.querySelector('td:nth-child(3)');
    const desc = descriptionCell ? descriptionCell.textContent : '';
    window.location.href = `/parts/new?default_description=${encodeURIComponent(desc)}`;
  } else {
    window.location.href = '/parts/new';
  }
});

// Handle Edit Selected clicks
editBtn.addEventListener("click", () => {
    const selectedRow = $('.row-select:checked').closest('tr');
    if (!selectedRow) return alert("No part selected.");
    const id = selectedRow.dataset.id;
    sessionStorage.setItem('returnTo', window.location.href);
    window.location.href = `/update/${id}`;
});

// Handle Show Deleted clicks
showDeletedBtn.addEventListener("click", () => {
      window.location.href = showDeletedBtn.dataset.url;
});

deleteBtn.addEventListener("click", () => {
  const idsToDelete = Array.from($$('.row-select:checked')).map(cb => cb.closest('tr').dataset.id);

  if (confirm(`Delete ${idsToDelete.length} part(s)?`)) {
    fetch('/parts/bulk-delete', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ ids: idsToDelete })
    }).then(r => r.ok ? doSearch(searchInput.value) : alert('Deletion failed'));
  }
});