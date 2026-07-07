var WEATHER_EMOJI = {
  '01': '☀',
  '02': '⛅',
  '03': '☁',
  '04': '☁',
  '09': '🌧',
  '10': '🌦',
  '11': '⛈',
  '13': '🌨',
  '50': '🌫'
};

function weatherEmoji(icon) {
  return WEATHER_EMOJI[String(icon).substring(0, 2)] || '☁';
}

function set(id, value) {
  var el = document.getElementById(id);
  if (el) el.textContent = value;
}

function updateDashboard() {
  fetch('/api/data')
    .then(function (r) { return r.json(); })
    .then(function (d) {
      set('w-temp',   d.temp   !== '--' ? Math.round(d.temp)   : '--');
      set('w-feels',  d.feels_like !== '--' ? Math.round(d.feels_like) + ' °C' : '--');
      set('w-hum',    d.humidity !== '--' ? d.humidity + ' %'  : '--');
      set('w-wind',   d.wind   !== '--' ? d.wind + ' m/s'      : '--');

      var descEl = document.getElementById('w-desc');
      if (descEl) {
        descEl.textContent = weatherEmoji(d.icon) + ' ' + d.desc;
      }

      set('s-temp', d.indoor_temp !== '--' ? d.indoor_temp : '--');
      set('s-hum',  d.indoor_hum  !== '--' ? d.indoor_hum  : '--');

      renderCalendar(d.events);
    })
    .catch(function (err) {
      console.error('Dashboard update error:', err);
    });
}

updateDashboard();
setInterval(updateDashboard, 30000);
