function renderCalendar(events) {
    const list = document.getElementById('calendar-list');
    list.innerHTML = '';

    const entries = Object.entries(events);
    if (entries.length === 0) {
        list.innerHTML = '<div style="color:var(--text-dim);margin-top:20px;font-size:0.85rem;">Keine bevorstehenden Termine</div>';
        return;
    }

    for (const [day, dayEvents] of entries) {
        // Split "Samstag, 05.04." into name + date
        const parts = day.split(', ');
        const dayName = parts[0];
        const dayDate = parts[1] || '';

        const row = document.createElement('div');
        row.className = 'cal-row';

        const labelCol = document.createElement('div');
        labelCol.className = 'cal-day-label';
        labelCol.innerHTML = `
            <div class="cal-day-name">${dayName}</div>
            ${dayDate ? `<div class="cal-day-date">${dayDate}</div>` : ''}
        `;

        const eventsCol = document.createElement('div');
        eventsCol.className = 'cal-events';

        dayEvents.forEach(ev => {
            const item = document.createElement('div');
            item.className = 'event-item';
            item.innerHTML = `
                <div class="event-time">${ev.time}</div>
                <div class="event-title">${ev.title}</div>
            `;
            eventsCol.appendChild(item);
        });

        row.appendChild(labelCol);
        row.appendChild(eventsCol);
        list.appendChild(row);
    }
}