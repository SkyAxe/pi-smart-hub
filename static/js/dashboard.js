function updateDashboard() {
    fetch('/api/data')
        .then(r => r.json())
        .then(data => {
            // Weather
            document.getElementById('temp').innerText = data.temp;
            document.getElementById('feels').innerText = data.feels_like;
            document.getElementById('humidity').innerText = data.humidity;
            document.getElementById('weather-desc').innerText = data.news;

            if (data.icon) {
                const icon = document.getElementById('weather-icon');
                icon.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
                icon.style.display = 'block';
            }

            // Indoor
            document.getElementById('indoor-temp').innerText = data.indoor_temp;
            document.getElementById('indoor-hum').innerText =
                data.indoor_hum === '--' ? '--' : data.indoor_hum + '%';

            // Calendar
            renderCalendar(data.events);
        })
        .catch(err => console.error('Update error:', err));
}

setInterval(updateDashboard, 30000);
updateDashboard();