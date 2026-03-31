function renderCalendar(events) {
    const list = document.getElementById('calendar-list');
    list.innerHTML = '';

    const entries = Object.entries(events);
    if (entries.length === 0) {
        list.innerHTML = '<div style="color:var(--text-dim);margin-top:20px;font-size:0.85rem;">Keine bevorstehenden Termine</div>';
        return;
    }

    for (const [day, dayEvents] of entries) {
        const header = document.createElement('div');
        header.className = 'day-header';
        header.innerText = day;
        list.appendChild(header);

        dayEvents.forEach(ev => {
            const item = document.createElement('div');
            item.className = 'event-item';
            item.innerHTML = `
                <div class="event-bar" style="background:${ev.color}"></div>
                <div class="event-time">${ev.time}</div>
                <div class="event-title">${ev.title}</div>
            `;
            list.appendChild(item);
        });
    }
}