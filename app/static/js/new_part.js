document.addEventListener('DOMContentLoaded', function () {
    // Focus the description field
    const locationInput = document.getElementById('location');
    const descriptionInput = document.getElementById('description');
    // const suggestionsContainer = document.getElementById('description-suggestions');

    // Focus the location field
    if (locationInput) locationInput.focus();

    // If sessionStorage has returnTo, add it to the form
    const returnTo = sessionStorage.getItem('returnTo');
    if (returnTo) {
        const form = document.querySelector('form');
        const returnToInput = document.createElement('input');
        returnToInput.type = 'hidden';
        returnToInput.name = 'returnTo';
        returnToInput.value = returnTo;
        form.appendChild(returnToInput);
        sessionStorage.removeItem('returnTo');
    }

    // Debounce for API search
    let debounceTimer;
    descriptionInput.addEventListener('input', function() {
        const query = this.value.trim();
        clearTimeout(debounceTimer);

        if (query.length < 2) {
            // suggestionsContainer.innerHTML = '';
            renderParts([]);    // Clear the table
            return;
        }

        debounceTimer = setTimeout(() => {
            fetch(`/api/search?q=${encodeURIComponent(query)}&limit=10`)
                .then(res => res.ok ? res.json() : Promise.reject('Search failed'))
                .then(parts => {
                    console.log("Parts data received", parts);
                //     suggestionsContainer.innerHTML = parts.map(part =>
                //         `<div class="suggestion-item" data-value="${part.description}">${part.description}</div>`
                //     ).join('');

                    renderParts(parts);
                })
            .catch(err => console.error(err));
        }, 200);
    });

    // // Click suggestion to fill input
    // suggestionsContainer.addEventListener('click', function(e) {
    //     if (e.target.classList.contains('suggestion-item')) {
    //         descriptionInput.value = e.target.dataset.value;
    //         suggestionsContainer.innerHTML = '';
    //     }
    // });
});