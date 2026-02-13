/**
 * MakeMeRich Wealth Card Generator — by PULSE
 * Creates beautiful, shareable images that drive virality.
 * Uses HTML5 Canvas — no external dependencies.
 */

const MRCards = {

  // Generate a wealth card as a canvas element
  generate(data) {
    const canvas = document.createElement('canvas');
    canvas.width = 1200;
    canvas.height = 630; // OG image ratio
    const ctx = canvas.getContext('2d');

    // Background gradient
    const bgGrad = ctx.createLinearGradient(0, 0, 1200, 630);
    bgGrad.addColorStop(0, '#0a0a0a');
    bgGrad.addColorStop(0.5, '#0d1117');
    bgGrad.addColorStop(1, '#0a0a0a');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, 1200, 630);

    // Subtle grid pattern
    ctx.strokeStyle = 'rgba(0, 255, 135, 0.03)';
    ctx.lineWidth = 1;
    for (let x = 0; x < 1200; x += 40) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, 630);
      ctx.stroke();
    }
    for (let y = 0; y < 630; y += 40) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(1200, y);
      ctx.stroke();
    }

    // Glow circle behind the percentile
    const glowGrad = ctx.createRadialGradient(600, 250, 0, 600, 250, 300);
    glowGrad.addColorStop(0, 'rgba(0, 255, 135, 0.08)');
    glowGrad.addColorStop(1, 'rgba(0, 255, 135, 0)');
    ctx.fillStyle = glowGrad;
    ctx.fillRect(0, 0, 1200, 630);

    // Border glow
    ctx.strokeStyle = 'rgba(0, 255, 135, 0.3)';
    ctx.lineWidth = 2;
    roundRect(ctx, 20, 20, 1160, 590, 20);
    ctx.stroke();

    // Title: MakeMeRich
    ctx.fillStyle = '#ffffff';
    ctx.font = '700 28px "Space Grotesk", "Segoe UI", sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('MakeMeRich', 60, 75);

    // Subtitle
    ctx.fillStyle = 'rgba(255,255,255,0.5)';
    ctx.font = '400 16px "Space Grotesk", "Segoe UI", sans-serif';
    ctx.fillText('Know Your Worth', 60, 100);

    // Main percentile — BIG
    const percentileText = `Top ${data.topPercent}%`;
    const textGrad = ctx.createLinearGradient(200, 200, 1000, 300);
    textGrad.addColorStop(0, '#00ff87');
    textGrad.addColorStop(1, '#00d4ff');
    ctx.fillStyle = textGrad;
    ctx.font = '700 120px "Space Grotesk", "Segoe UI", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(percentileText, 600, 280);

    // "Richer than X people"
    ctx.fillStyle = 'rgba(255,255,255,0.7)';
    ctx.font = '400 24px "Space Grotesk", "Segoe UI", sans-serif';
    ctx.fillText(`Richer than ${data.richerThan} people on Earth`, 600, 330);

    // Stats row
    const stats = [
      { label: 'Per Second', value: data.perSecond },
      { label: 'Per Hour', value: data.perHour },
      { label: 'Per Day', value: data.perDay },
    ];

    const startX = 200;
    const spacing = 300;

    stats.forEach((stat, i) => {
      const x = startX + i * spacing;

      // Value
      ctx.fillStyle = '#00ff87';
      ctx.font = '700 36px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillText(stat.value, x + 100, 430);

      // Label
      ctx.fillStyle = 'rgba(255,255,255,0.5)';
      ctx.font = '400 16px "Space Grotesk", "Segoe UI", sans-serif';
      ctx.fillText(stat.label, x + 100, 460);
    });

    // Progress bar
    const barY = 500;
    const barWidth = 1000;
    const barHeight = 8;
    const barX = 100;

    // Bar background
    ctx.fillStyle = 'rgba(255,255,255,0.1)';
    roundRect(ctx, barX, barY, barWidth, barHeight, 4);
    ctx.fill();

    // Bar fill
    const fillWidth = (data.percentile / 100) * barWidth;
    const barGrad = ctx.createLinearGradient(barX, 0, barX + fillWidth, 0);
    barGrad.addColorStop(0, '#00ff87');
    barGrad.addColorStop(1, '#00d4ff');
    ctx.fillStyle = barGrad;
    roundRect(ctx, barX, barY, fillWidth, barHeight, 4);
    ctx.fill();

    // Bar labels
    ctx.fillStyle = 'rgba(255,255,255,0.3)';
    ctx.font = '400 12px "Space Grotesk", "Segoe UI", sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('Poorest', barX, barY + 25);
    ctx.textAlign = 'right';
    ctx.fillText('Richest', barX + barWidth, barY + 25);

    // Marker dot
    ctx.beginPath();
    ctx.arc(barX + fillWidth, barY + barHeight / 2, 6, 0, Math.PI * 2);
    ctx.fillStyle = '#ffffff';
    ctx.fill();

    // Footer
    ctx.fillStyle = 'rgba(255,255,255,0.3)';
    ctx.font = '400 14px "Space Grotesk", "Segoe UI", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('makemerich.app — How rich are you?', 600, 580);

    return canvas;
  },

  // Download the card as PNG
  download(canvas) {
    const link = document.createElement('a');
    link.download = 'my-wealth-card.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
  },

  // Get data URL for preview
  toDataURL(canvas) {
    return canvas.toDataURL('image/png');
  },
};

// Helper: rounded rectangle
function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

if (typeof module !== 'undefined') module.exports = MRCards;
