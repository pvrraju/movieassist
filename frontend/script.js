document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('recommendation-form');
    const resultsSection = document.getElementById('results-section');
    const loader = document.getElementById('loader');
    const recommendationsContainer = document.getElementById('recommendations');
    const errorContainer = document.getElementById('error');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 1. Clear previous results and show loader
        resultsSection.classList.remove('hidden');
        loader.classList.remove('hidden');
        recommendationsContainer.innerHTML = '';
        errorContainer.classList.add('hidden');
        errorContainer.textContent = '';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        // 2. Get form data
        const mood = document.getElementById('user-mood').value;
        const pastMovies = document.getElementById('past-movies').value;
        const request = document.getElementById('user-request').value;

        // 3. Construct the request payload
        const payload = {
            user_mood: mood,
            past_movies: pastMovies ? pastMovies.split(',').map(item => item.trim()) : [],
            user_request: request,
        };

        // 4. Make the API call
        try {
            const response = await fetch('http://127.0.0.1:8000/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // 5. Display the results
            displayRecommendations(data.recommendations);

        } catch (error) {
            displayError(error.message);
        } finally {
            // 6. Hide loader
            loader.classList.add('hidden');
        }
    });

    function displayRecommendations(recommendationsText) {
        // The model's output separates recommendations with double newlines.
        // We split by the actual newline characters.
        const recommendations = recommendationsText.trim().split(/\n\s*\n/);
        
        recommendations.forEach(rec => {
            const item = document.createElement('div');
            item.className = 'recommendation-item';
            
            // Convert markdown-style bolding (e.g., **Title**) to <h3> tags.
            // Replace any remaining single newlines with <br> for proper line breaks.
            let html = rec.replace(/\*\*(.*?)\*\*/g, '<h3>$1</h3>');
            html = html.replace(/\n/g, '<br>');

            item.innerHTML = html;
            recommendationsContainer.appendChild(item);
        });
    }

    function displayError(message) {
        errorContainer.textContent = `Sorry, something went wrong: ${message}`;
        errorContainer.classList.remove('hidden');
    }
});
