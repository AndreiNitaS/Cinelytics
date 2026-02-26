// Cinelytics Web App JavaScript

// ===== Rating Slider =====
const slider = document.getElementById('rating-slider');
const ratingValueDisplay = document.getElementById('rating-value');

// Update rating display with stars
function updateRating(val) {
    ratingValueDisplay.textContent = val.toFixed(1);
    updateStars(val);
}

// Update star display
function updateStars(val) {
    const starsContainer = document.querySelector('.rating-stars');
    if (!starsContainer) return;
    
    let starsHTML = '';
    for (let i = 1; i <= 5; i++) {
        if (val >= i) {
            starsHTML += '<span class="star filled">★</span>';
        } else if (val >= i - 0.5) {
            starsHTML += '<span class="star half">★</span>';
        } else {
            starsHTML += '<span class="star">★</span>';
        }
    }
    starsContainer.innerHTML = starsHTML;
}

// Slider change handler
if (slider) {
    slider.addEventListener('input', (e) => {
        updateRating(parseFloat(e.target.value));
    });
    
    // Initialize
    updateRating(3.0);
}

// Keyboard support for rating
document.addEventListener('keydown', (e) => {
    if (!slider) return;
    
    const step = 0.5;
    let val = parseFloat(slider.value);
    
    if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
        val = Math.max(1.0, val - step);
        slider.value = val;
        updateRating(val);
        e.preventDefault();
    } else if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
        val = Math.min(5.0, val + step);
        slider.value = val;
        updateRating(val);
        e.preventDefault();
    }
});

// ===== Submit Rating =====
async function submitRating() {
    const titleInput = document.getElementById('movie-title');
    const title = titleInput.value.trim();
    const rating = parseFloat(slider.value);
    
    if (!title) {
        alert('Please enter a movie title');
        return;
    }
    
    const outputTitle = document.getElementById('output-title');
    const outputText = document.getElementById('output-text');
    
    outputTitle.textContent = 'Rating Movie...';
    outputText.innerHTML = '<div class="flex justify-center items-center py-12"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>';
    
    try {
        const response = await fetch('/api/rate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, rating })
        });
        
        const data = await response.json();
        
        if (data.success) {
            outputTitle.textContent = 'Success!';
            
            // Fetch poster for rated movie
            const posterResponse = await fetch(`/api/movie-details/${encodeURIComponent(data.movie_title)}`);
            const posterData = await posterResponse.json();
            const posterUrl = posterData.success ? (posterData.poster_url || 'https://via.placeholder.com/200x300?text=No+Poster') : 'https://via.placeholder.com/200x300?text=No+Poster';
            
            let html = `
                <div class="bg-emerald-50 dark:bg-emerald-900/20 border-l-4 border-emerald-500 p-4 rounded-r mb-6">
                    <div class="flex items-start gap-4">
                        <img src="${posterUrl}" alt="${data.movie_title}" class="w-20 h-28 object-cover rounded-lg shadow-md flex-shrink-0"/>
                        <div class="flex-1">
                            <div class="flex items-start justify-between">
                                <div>
                                    <h4 class="font-semibold text-emerald-800 dark:text-emerald-200 mb-1">${data.movie_title}</h4>
                                    <p class="text-sm text-emerald-700 dark:text-emerald-300">Your rating: ${data.user_rating} ⭐ • TMDb: ${data.tmdb_rating} ⭐</p>
                                </div>
                                <button onclick="showMovieDetails('${data.movie_title.replace(/'/g, "\\'")}')" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-medium transition-colors">
                                    View Details
                                </button>
                            </div>
                        </div>
                    </div>
                </div>`;
            
            if (data.recommendations && data.recommendations.length > 0) {
                html += `
                    <div class="mb-4">
                        <h4 class="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                            <span class="material-icons-round text-secondary mr-2">auto_awesome</span>
                            Recommended for you
                        </h4>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">`;
                
                // Fetch posters for recommendations in parallel
                const posterPromises = data.recommendations.map(rec => 
                    fetch(`/api/movie-details/${encodeURIComponent(rec.title)}`)
                        .then(r => r.json())
                        .then(d => ({
                            ...rec,
                            poster: d.success ? (d.poster_url || 'https://via.placeholder.com/150x225?text=No+Poster') : 'https://via.placeholder.com/150x225?text=No+Poster'
                        }))
                        .catch(() => ({
                            ...rec,
                            poster: 'https://via.placeholder.com/150x225?text=No+Poster'
                        }))
                );
                
                const recsWithPosters = await Promise.all(posterPromises);
                
                recsWithPosters.forEach((rec, index) => {
                    html += `
                        <div class="flex items-center gap-4 p-4 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg transition-colors border border-gray-100 dark:border-gray-700 group">
                            <img src="${rec.poster}" alt="${rec.title}" class="w-16 h-24 object-cover rounded-lg shadow-md flex-shrink-0 group-hover:scale-105 transition-transform"/>
                            <div class="flex-1 min-w-0">
                                <div class="flex items-start justify-between gap-2">
                                    <div class="flex-1 min-w-0">
                                        <h5 class="font-semibold text-gray-900 dark:text-white truncate">${rec.title}</h5>
                                        <p class="text-sm text-gray-500 dark:text-gray-400">TMDb: ${rec.rating} ⭐</p>
                                    </div>
                                    <button onclick="showMovieDetails('${rec.title.replace(/'/g, "\\'")}')" class="px-3 py-1 bg-primary/10 text-primary hover:bg-primary/20 rounded-lg transition-colors text-xs font-medium whitespace-nowrap">
                                        Details
                                    </button>
                                </div>
                            </div>
                        </div>`;
                });
                
                html += `</div></div>`;
            }
            
            outputText.innerHTML = html;
            titleInput.value = '';
        } else {
            outputTitle.textContent = 'Error';
            outputText.innerHTML = `
                <div class="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 p-4 rounded-r">
                    <div class="flex items-start">
                        <span class="material-icons-round text-red-500 mr-3">error</span>
                        <div>
                            <h4 class="font-semibold text-red-800 dark:text-red-200">Error</h4>
                            <p class="text-sm text-red-700 dark:text-red-300">${data.error}</p>
                        </div>
                    </div>
                </div>`;
        }
    } catch (error) {
        outputTitle.textContent = 'Network Error';
        outputText.innerHTML = `
            <div class="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 p-4 rounded-r">
                <div class="flex items-start">
                    <span class="material-icons-round text-red-500 mr-3">wifi_off</span>
                    <div>
                        <h4 class="font-semibold text-red-800 dark:text-red-200">Network Error</h4>
                        <p class="text-sm text-red-700 dark:text-red-300">${error.message}</p>
                    </div>
                </div>
            </div>`;
    }
}

// ===== Load My Movies =====
async function loadMyMovies() {
    const outputTitle = document.getElementById('output-title');
    const outputText = document.getElementById('output-text');
    
    outputTitle.textContent = 'Loading Your Movies...';
    outputText.innerHTML = '<div class="flex justify-center items-center py-12"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>';
    
    try {
        const response = await fetch('/api/my-movies');
        const data = await response.json();
        
        if (data.success) {
            outputTitle.textContent = `Your Movie Collection (${data.movies.length})`;
            
            if (data.movies.length === 0) {
                outputText.innerHTML = `
                    <div class="text-center py-12">
                        <span class="material-icons-round text-gray-300 dark:text-gray-600 text-6xl mb-4">movie</span>
                        <p class="text-gray-500 dark:text-gray-400">You haven't rated any movies yet.</p>
                        <p class="text-sm text-gray-400 dark:text-gray-500 mt-2">Start rating to build your collection! 🎬</p>
                    </div>`;
            } else {
                let html = '<div class="space-y-3">';
                data.movies.forEach((movie, index) => {
                    html += `
                        <div class="flex items-center justify-between p-4 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg transition-colors border border-gray-100 dark:border-gray-700">
                            <div class="flex items-center flex-1">
                                <span class="text-lg font-bold text-gray-300 dark:text-gray-600 mr-4">${index + 1}</span>
                                <div class="flex-1">
                                    <h5 class="font-semibold text-gray-900 dark:text-white">${movie.title}</h5>
                                    <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">${movie.timestamp}</p>
                                </div>
                            </div>
                            <div class="flex items-center space-x-4">
                                <span class="px-3 py-1 bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 rounded-full text-sm font-semibold flex items-center">
                                    <span class="material-icons-round text-xs mr-1">star</span>
                                    ${movie.rating}
                                </span>
                            </div>
                        </div>`;
                });
                html += '</div>';
                outputText.innerHTML = html;
            }
        } else {
            outputTitle.textContent = 'Error';
            outputText.innerHTML = `
                <div class="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 p-4 rounded-r">
                    <div class="flex items-start">
                        <span class="material-icons-round text-red-500 mr-3">error</span>
                        <div>
                            <h4 class="font-semibold text-red-800 dark:text-red-200">Error</h4>
                            <p class="text-sm text-red-700 dark:text-red-300">${data.error}</p>
                        </div>
                    </div>
                </div>`;
        }
    } catch (error) {
        outputTitle.textContent = 'Network Error';
        outputText.innerHTML = `
            <div class="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 p-4 rounded-r">
                <div class="flex items-start">
                    <span class="material-icons-round text-red-500 mr-3">wifi_off</span>
                    <div>
                        <h4 class="font-semibold text-red-800 dark:text-red-200">Network Error</h4>
                        <p class="text-sm text-red-700 dark:text-red-300">${error.message}</p>
                    </div>
                </div>
            </div>`;
    }
}

// ===== Logout =====
function logout() {
    window.location.href = '/logout';
}

// ===== Enter Key Support =====
const titleInput = document.getElementById('movie-title');
if (titleInput) {
    titleInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            submitRating();
        }
    });
}
