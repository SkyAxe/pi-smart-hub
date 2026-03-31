function updateClock() {
    const now = new Date();
    document.getElementById('clock').innerText =
        now.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' });
    document.getElementById('date').innerText =
        now.toLocaleDateString('de-DE', { weekday: 'long', day: 'numeric', month: 'long' });
}

setInterval(updateClock, 1000);
updateClock();