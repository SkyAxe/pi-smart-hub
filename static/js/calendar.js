function renderCalendar(events) {
  var list = document.getElementById('calendar-list');
  list.innerHTML = '';

  var entries = Object.entries(events || {});
  if (entries.length === 0) {
    list.innerHTML = '<div style="color:var(--text-mid);font-size:13px;margin-top:8px;">Keine bevorstehenden Termine</div>';
    return;
  }

  entries.forEach(function (entry) {
    var day = entry[0];
    var dayEvents = entry[1];

    var group = document.createElement('div');
    group.className = 'cal-day';

    var header = document.createElement('div');
    header.className = 'cal-day-header';
    header.textContent = day;
    group.appendChild(header);

    dayEvents.forEach(function (ev) {
      var row = document.createElement('div');
      row.className = 'cal-event';

      var time = document.createElement('div');
      time.className = 'event-time';
      time.textContent = ev.time || 'Ganztag';

      var right = document.createElement('div');

      var title = document.createElement('div');
      title.className = 'event-title';
      title.textContent = ev.title;
      right.appendChild(title);

      if (ev.partner) {
        var sub = document.createElement('div');
        sub.className = 'event-sub';
        sub.textContent = '♥';
        right.appendChild(sub);
      }

      if (ev.day_info) {
        var sub = document.createElement('div');
        sub.className = 'event-sub';
        sub.textContent = ev.day_info;
        right.appendChild(sub);
      }

      row.appendChild(time);
      row.appendChild(right);
      group.appendChild(row);
    });

    list.appendChild(group);
  });
}
