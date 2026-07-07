(function () {
  var DAYS   = ['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag'];
  var MONTHS = ['Januar','Februar','März','April','Mai','Juni','Juli','August',
                'September','Oktober','November','Dezember'];

  function pad(n) { return String(n).padStart(2, '0'); }

  function tick() {
    var now = new Date();
    var h = pad(now.getHours());
    var m = pad(now.getMinutes());
    var s = now.getSeconds();

    document.getElementById('clock-h').textContent = h;
    document.getElementById('clock-m').textContent = m;
    document.getElementById('colon').style.opacity = s % 2 === 0 ? '1' : '0.15';

    document.getElementById('date-display').textContent =
      DAYS[now.getDay()] + ' · ' + now.getDate() + '. ' +
      MONTHS[now.getMonth()] + ' ' + now.getFullYear();

    var el = document.getElementById('last-update');
    if (el) {
      el.textContent = 'Aktualisiert ' + h + ':' + m + ':' + pad(s);
    }
  }

  tick();
  setInterval(tick, 1000);
})();
