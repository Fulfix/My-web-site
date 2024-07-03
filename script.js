// script.js

document.addEventListener('DOMContentLoaded', (event) => {
    // Sélectionne toutes les divs avec la classe clickable-div
    const clickableDivs = document.querySelectorAll('.clickable-div');

    clickableDivs.forEach(div => {
        div.addEventListener('click', () => {
            const url = div.getAttribute('data-url');
            if (url) {
                window.open(url, '_blank');
            }
        });
    });
});
