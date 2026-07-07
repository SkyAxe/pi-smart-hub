var WEATHER_EMOJI = {
  '01': '☀', '02': '⛅', '03': '☁', '04': '☁',
  '09': '🌧', '10': '🌦', '11': '⛈', '13': '🌨', '50': '🌫'
};

function weatherEmoji(icon) {
  return WEATHER_EMOJI[String(icon).substring(0, 2)] || '☁';
}

function val(v, suffix) {
  if (v === null || v === undefined) return '--';
  return v + (suffix || '');
}

function set(id, value) {
  var el = document.getElementById(id);
  if (el) el.textContent = value;
}

function updateDashboard() {
  fetch('/api/data')
    .then(function(r) { return r.json(); })
    .then(function(d) {
      set('w-temp',  val(d.temp));
      set('w-feels', val(d.feels_like, ' °C'));
      set('w-hum',   val(d.humidity,   ' %'));
      set('w-wind',  val(d.wind,       ' m/s'));

      var descEl = document.getElementById('w-desc');
      if (descEl) descEl.textContent = weatherEmoji(d.icon) + ' ' + (d.desc || '--');

      set('s-temp', val(d.indoor_temp));
      set('s-hum',  val(d.indoor_hum));

      renderCalendar(d.events);
    })
    .catch(function(err) { console.error('Dashboard error:', err); });
}

updateDashboard();
setInterval(updateDashboard, 30000);
