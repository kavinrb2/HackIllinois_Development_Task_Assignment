document.addEventListener("DOMContentLoaded", function() {
    fetch('http://localhost:5000/get-combined-text')
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").textContent = data.combinedText;
    })
    .catch(error => {
        console.error('Error fetching combined text:', error);
        document.getElementById("output").textContent = 'Failed to load combined text.';
    });
});