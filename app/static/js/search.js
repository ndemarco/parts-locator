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