async function doSearch(q = '') {
    try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
        if (!res.ok) {
            alert("Failed to fetch parts.");
            return [];
        }
    
        const parts = await res.json();
        renderParts(parts);
        return parts;

    } catch (err) {
        console.error("Search failed:", err);
        return [];
    }
}

function updateSearch(query) {
    const newUrl = `${window.location.pathname}?q=${encodeURIComponent(query)}`;
    window.history.replaceState({ path: newUrl }, '', newUrl);
    return doSearch(query)
}

// Populates rows in Parts HTML table.
function renderParts(parts) {
    if (!partsTableBody) return;

    // Clear existing records from table
    partsTableBody.innerHTML = '';

    // Populate the table
    parts.forEach(part => {
        partsTableBody.insertAdjacentHTML('beforeend', `
            <tr data-id="${part.id}" class="parts-row">
                <td><input type="checkbox" class="row-select"></td>
                <td>${part.id}</td>
                <td>${part.description}</td>
                <td>${part.location}</td>
                <td>${part.location_id}</td>
                <td>${part.date_created}</td>
            </tr>
        `);
    });

    bindRowEvents();
}
