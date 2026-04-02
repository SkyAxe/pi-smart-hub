const socket = io();

const claudeStatus = document.getElementById('claude-status');
const claudePulse = document.querySelector('.claude-pulse');

socket.on('connect', () => {
    console.log('WebSocket connected');
});

socket.on('claude_thinking', () => {
    claudePulse.style.background = '#f59e0b';
    claudePulse.style.animationDuration = '0.5s';
    claudeStatus.textContent = 'Denke nach...';
    claudeStatus.style.color = '#f59e0b';
});

socket.on('claude_response', (data) => {
    // Reset pulse
    claudePulse.style.background = '#8b5cf6';
    claudePulse.style.animationDuration = '3s';
    claudeStatus.style.color = 'var(--text-mid)';

    // Show response
    claudeStatus.textContent = data.text;

    // Play confirmation sound
    playConfirmSound();

    // Reset after 15 seconds
    setTimeout(() => {
        claudeStatus.textContent = 'Bereit · Sag "Hey Claude"';
        claudeStatus.style.color = 'var(--text-dim)';
    }, 15000);
});

function playConfirmSound() {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = ctx.createOscillator();
    const gainNode = ctx.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(ctx.destination);
    
    oscillator.frequency.setValueAtTime(880, ctx.currentTime);
    oscillator.frequency.setValueAtTime(1100, ctx.currentTime + 0.1);
    gainNode.gain.setValueAtTime(0.1, ctx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);
    
    oscillator.start(ctx.currentTime);
    oscillator.stop(ctx.currentTime + 0.3);
}