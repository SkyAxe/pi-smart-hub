const socket = io();
const claudeStatus = document.getElementById('claude-status');
const claudePulse = document.querySelector('.claude-pulse');
const claudeZone = document.querySelector('.claude-zone');

let audioCtx = null;

function unlockAudio() {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    // Stiller Ton um Audio zu entsperren
    const buf = audioCtx.createBuffer(1, 1, 22050);
    const src = audioCtx.createBufferSource();
    src.buffer = buf;
    src.connect(audioCtx.destination);
    src.start(0);
    document.getElementById('audio-unlock').style.display = 'none';
    console.log('Audio entsperrt');
}

function playConfirmSound() {
    if (!audioCtx) return;
    [0, 0.15].forEach((delay, i) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.frequency.value = i === 0 ? 880 : 1100;
        gain.gain.setValueAtTime(0.15, audioCtx.currentTime + delay);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + delay + 0.2);
        osc.start(audioCtx.currentTime + delay);
        osc.stop(audioCtx.currentTime + delay + 0.2);
    });
}

socket.on('connect', () => {
    console.log('WebSocket connected');
});

socket.on('claude_thinking', () => {
    claudePulse.style.background = '#f59e0b';
    claudePulse.style.animationDuration = '0.5s';
    claudeStatus.textContent = 'Denke nach...';
    claudeStatus.style.color = '#f59e0b';
    claudeStatus.style.fontStyle = 'normal';
    claudeZone.style.alignItems = 'flex-start';
});

socket.on('claude_response', (data) => {
    claudePulse.style.background = '#8b5cf6';
    claudePulse.style.animationDuration = '3s';
    claudeStatus.style.color = 'var(--text)';
    claudeStatus.style.fontStyle = 'normal';
    claudeStatus.style.fontSize = '0.85rem';
    claudeStatus.style.lineHeight = '1.5';
    claudeStatus.textContent = data.text;
    claudeZone.style.alignItems = 'flex-start';

    // Ton über ALSA direkt
    playConfirmSound();

    setTimeout(() => {
        claudeStatus.textContent = 'Bereit · Sag "Hey Claude"';
        claudeStatus.style.color = 'var(--text-dim)';
        claudeStatus.style.fontStyle = 'italic';
        claudeStatus.style.fontSize = '0.78rem';
        claudeZone.style.alignItems = 'center';
    }, 20000);
});

socket.on('claude_listening', () => {
    claudePulse.style.background = '#2ecc71';
    claudePulse.style.animationDuration = '0.8s';
    claudeStatus.textContent = 'Höre zu...';
    claudeStatus.style.color = '#2ecc71';
    claudeStatus.style.fontStyle = 'normal';
});

function playConfirmSound() {
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        
        // Kurzer doppelter Ton
        [0, 0.15].forEach((delay, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.frequency.value = i === 0 ? 880 : 1100;
            gain.gain.setValueAtTime(0.15, ctx.currentTime + delay);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + delay + 0.2);
            osc.start(ctx.currentTime + delay);
            osc.stop(ctx.currentTime + delay + 0.2);
        });
    } catch(e) {
        console.log('Audio nicht verfügbar:', e);
    }
}