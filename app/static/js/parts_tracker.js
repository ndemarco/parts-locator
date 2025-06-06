// Query selector shorthand aliases
const $ = selector => document.querySelector(selector);
const $$ = selector => document.querySelectorAll(selector);

// Quick aliases
const searchInput = $('#search-input');
const partsTableBody = $('#parts-table tbody');
const addPartBtn = $('#add-part-btn');
const editBtn = $('#edit-btn');
const deleteBtn = $('#delete-btn');
const showDeletedBtn = $('#show-deleted-btn')

// Initial load
window.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const query = params.get('q') || '';
    searchInput.value = query;
    doSearch(query);
});

function bindRowEvents() {
    $$('.parts-row').forEach(row => {
        const checkbox = row.querySelector('.row-select');
        if (!checkbox) return;

        // Clicking the row activates the row
        row.addEventListener('click', () => {
            setActiveRow(row);
        });
        
        // Clicking the checkbox -> activate row & toggle selection
        checkbox.addEventListener('click', (e) => {
            e.stopPropagation();  // prevents row click from firing
            setActiveRow(row);
        });
    });
}

function setActiveRow(row) {
    $$('.parts-row').forEach(r => {
        r.classList.remove('active-row')
    });
    row.classList.add('active-row');
}

searchInput.addEventListener('input', () => {
    const query = searchInput.value;
    updateSearch(query);
});

// Handle Add Part clicks
addPartBtn.addEventListener("click", () => {
    const activeRow = $('.parts-row.active-row');
    if (activeRow) {
        console.log("Active row found");
        const partId = activeRow.dataset.id;
        window.location.href = `/parts/new@copy_from=${partId}`;
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
        })
        .then(r => r.ok ? doSearch(searchInput.value) : alert('Deletion failed'))
        .catch(err => alert('Network error: ' + err));
    }
});