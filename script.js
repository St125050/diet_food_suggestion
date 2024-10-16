// script.js

document.getElementById('diet-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const protein = document.getElementById('protein').value;
    const carbs = document.getElementById('carbs').value;
    const fat = document.getElementById('fat').value;

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ protein, carbs, fat })
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';

        if (data.length === 0) {
            resultsDiv.innerHTML = '<p>No suggestions found. Try increasing the values.</p>';
        } else {
            data.forEach(recipe => {
                const recipeDiv = document.createElement('div');
                recipeDiv.innerHTML = `
                    <h3>${recipe.Recipe_name}</h3>
                    <p>Diet Type: ${recipe.Diet_type}</p>
                    <p>Cuisine Type: ${recipe.Cuisine_type}</p>
                    <p>Protein: ${recipe['Protein(g)']}g</p>
                    <p>Carbs: ${recipe['Carbs(g)']}g</p>
                    <p>Fat: ${recipe['Fat(g)']}g</p>
                `;
                resultsDiv.appendChild(recipeDiv);
            });
        }
    })
    .catch(error => console.error('Error:', error));
});
