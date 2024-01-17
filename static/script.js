// Function to load products and add them to the index page
function loadProducts() {
    fetch('/api/products')
        .then(response => response.json())
        .then(data => {
            const productsContainer = document.getElementById('products');
            productsContainer.innerHTML = '';
            data.forEach((product, index) => {
                const productDiv = document.createElement('div');
                productDiv.className = 'product';
                productDiv.innerHTML = `
                    <h3>${product.Name}</h3>
                    <p>Brand: ${product.Brand}, Price: $${product.Price}</p>
                    <button onclick="viewDetails(${index})">View Details</button>
                `;
                productsContainer.appendChild(productDiv);
            });
        });
}

// Function to handle product search
function searchProducts() {
    const searchBox = document.getElementById('searchBox');
    searchBox.addEventListener('input', function () {
        const query = searchBox.value.toLowerCase();
        const products = document.getElementsByClassName('product');
        Array.from(products).forEach(function (product) {
            const title = product.querySelector('h3').textContent;
            if (title.toLowerCase().indexOf(query) !== -1) {
                product.style.display = '';
            } else {
                product.style.display = 'none';
            }
        });
    });
}

// function viewDetails(index) {
//     fetch(`/api/products/${index}`)
//         .then(response => response.json())
//         .then(data => {
//             const detailsContainer = document.getElementById('itemDetails');
//             detailsContainer.innerHTML = `
//                 <h2>${data.Name}</h2>
//                 <p>Brand: ${data.Brand}</p>
//                 <p>Price: $${data.Price}</p>
//                 <!-- Add more product details here -->
//             `;
//             // Load recommendations if needed
//         });
// }
function viewDetails(index) {
    window.location.href = `/products/${index}`; // Redirect to the item details page
}


// Function to load recommendations for a product
function loadRecommendations(productId) {
    fetch(`/api/recommendations/${productId}`) // Adjust this endpoint
        .then(response => response.json())
        .then(data => {
            const recommendationsContainer = document.getElementById('recommendations');
            recommendationsContainer.innerHTML = '<h3>Recommended Products</h3>';
            data.forEach(recommendation => {
                const recDiv = document.createElement('div');
                recDiv.className = 'recommendation';
                recDiv.innerHTML = `<p>${recommendation.name}</p>`;
                recommendationsContainer.appendChild(recDiv);
            });
        });
}

document.addEventListener("DOMContentLoaded", function () {
    loadProducts();
    searchProducts();
});

function loadItemDetails() {
    const productId = window.location.pathname.split('/').pop();
    // Fetch and display item details
    // After displaying item details, call loadRecommendations
    loadRecommendations(productId);
}

if (window.location.pathname.startsWith('/products/')) {
    loadItemDetails();
}


function loadRecommendations(productId) {
    const recommendationsContainer = document.getElementById('recommendations');
    fetch(`/api/recommendations/${productId}`)
        .then(response => response.json())
        .then(data => {
            recommendationsContainer.innerHTML = '<h3>Recommended Products</h3>';
            data.forEach(product => {
                const productDiv = document.createElement('div');
                productDiv.className = 'recommendation';
                productDiv.innerHTML = `
                    <h4>${product.Name}</h4>
                    <p>Brand: ${product.Brand}</p>
                    <p>Price: $${product.Price}</p>
                    <!-- Add other product details as needed -->
                `;
                recommendationsContainer.appendChild(productDiv);
            });
        })
        .catch(error => {
            console.error('Error fetching recommendations:', error);
            recommendationsContainer.innerHTML = '<p>Failed to load recommendations.</p>';
        });
}

function trackProductSelection(productId, userId) {
    let selections = JSON.parse(localStorage.getItem('userSelections')) || {};

    if (!selections[userId]) {
        selections[userId] = {};
    }

    if (!selections[userId][productId]) {
        selections[userId][productId] = 0;
    }

    selections[userId][productId] += 1; // Increment the count
    localStorage.setItem('userSelections', JSON.stringify(selections));
}

function sendSelectionsToServer() {
    const selections = localStorage.getItem('userSelections');
    if (selections) {
        fetch('/api/save-selections', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: selections
        }).then(response => {
            if (response.ok) {
                localStorage.removeItem('userSelections'); // Clear local storage on successful send
            }
        });
    }
}



