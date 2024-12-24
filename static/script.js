fetch('/recipes')
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('recipes-container');
        data.forEach(recipe => {
            const div = document.createElement('div');
            div.innerHTML = `<h2>${recipe.name}</h2><p>${recipe.ingredients}</p>`;
            container.appendChild(div);
        });
    });

// Fetch recipes from the backend and display them
fetch('https://humble-pancake-x59qv56xx6pr2v6vq-5000.app.github.dev/recipes')
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('recipes-container');
        container.innerHTML = ''; // Clear the container
        data.forEach(recipe => {
            const recipeDiv = document.createElement('div');
            recipeDiv.className = 'recipe';
            recipeDiv.innerHTML = `
                <h2>${recipe.name}</h2>
                <p><strong>Ingredients:</strong> ${recipe.ingredients}</p>
                <p><strong>Instructions:</strong> ${recipe.instructions}</p>
            `;
            container.appendChild(recipeDiv);
        });
    })
    .catch(error => {
        console.error('Error fetching recipes:', error);
    });

    document.addEventListener("DOMContentLoaded", () => {
        const menuToggle = document.querySelector(".menu-toggle");
        const menu = document.getElementById("menu");

        menuToggle.addEventListener("click", () => {
            menu.classList.toggle("active"); // Toggle the 'active' class
        });
    });

    document.addEventListener("DOMContentLoaded", () => {
        const currentPath = window.location.pathname;
        const links = document.querySelectorAll(".menu-links li a");

        links.forEach(link => {
            if (link.getAttribute("href") === currentPath) {
                link.classList.add("active");
            }
        });
    });
