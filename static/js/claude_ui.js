const socket = io();
const claudeStatus = document.getElementById('claude-status');
const claudePulse = document.querySelector('.claude-pulse');
const claudeZone = document.querySelector('.claude-zone');

let audioCtx = null;
let resetTimer = null;

function unlockAudio() {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const buf = audioCtx.createBuffer(1, 1, 22050);
    const src = audioCtx.createBufferSource();
    src.buffer = buf;
    src.connect(audioCtx.destination);
    src.start(0);
    document.getElementById('audio-unlock').style.display = 'none';
    console.log('Audio entsperrt');
}

function playConfirmSound() {
    try {
        const ctx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
        [0, 0.12].forEach((delay, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.frequency.value = i === 0 ? 880 : 1100;
            gain.gain.setValueAtTime(0.12, ctx.currentTime + delay);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + delay + 0.18);
            osc.start(ctx.currentTime + delay);
            osc.stop(ctx.currentTime + delay + 0.2);
        });
    } catch (e) {
        console.log('Audio nicht verfügbar:', e);
    }
}

function setClaudeState(state, text) {
    clearTimeout(resetTimer);
    claudeZone.dataset.state = state;

    const configs = {
        idle: {
            dot: '#8b5cf6',
            duration: '3s',
            color: 'var(--text-dim)',
            italic: true,
            fontSize: '0.78rem',
            align: 'center',
        },
        listening: {
            dot: '#2ecc71',
            duration: '0.6s',
            color: '#2ecc71',
            italic: false,
            fontSize: '0.82rem',
            align: 'center',
        },
        thinking: {
            dot: '#f59e0b',
            duration: '0.4s',
            color: '#f59e0b',
            italic: false,
            fontSize: '0.82rem',
            align: 'flex-start',
        },
        response: {
            dot: '#8b5cf6',
            duration: '2s',
            color: 'var(--text)',
            italic: false,
            fontSize: '0.85rem',
            align: 'flex-start',
        },
    };

    const cfg = configs[state] || configs.idle;
    claudePulse.style.background = cfg.dot;
    claudePulse.style.animationDuration = cfg.duration;
    claudeStatus.textContent = text;
    claudeStatus.style.color = cfg.color;
    claudeStatus.style.fontStyle = cfg.italic ? 'italic' : 'normal';
    claudeStatus.style.fontSize = cfg.fontSize;
    claudeZone.style.alignItems = cfg.align;
}

socket.on('connect', () => console.log('WebSocket connected'));

socket.on('claude_listening', () => {
    setClaudeState('listening', 'Höre zu…');
});

socket.on('claude_thinking', () => {
    setClaudeState('thinking', 'Denke nach…');
});

socket.on('claude_response', (data) => {
    setClaudeState('response', data.text);
    playConfirmSound();
    resetTimer = setTimeout(() => {
        setClaudeState('idle', 'Bereit · Sag "Hey Claude"');
    }, 20000);
});
