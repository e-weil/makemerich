/**
 * MakeMeRich Share Engine — by PULSE
 * Every share = 10 new users. This is the growth engine.
 */

const MRShare = {

  init() {
    // Download card button
    document.getElementById('download-card')?.addEventListener('click', () => {
      this.downloadCard();
    });

    // Copy link button
    document.getElementById('copy-link')?.addEventListener('click', () => {
      this.copyLink();
    });

    // Share on Twitter/X button
    document.getElementById('share-twitter')?.addEventListener('click', () => {
      this.shareTwitter();
    });
  },

  // Generate and show the wealth card preview
  showPreview() {
    if (!currentIncome) return;

    const percentile = MRCalculator.globalPercentile(currentIncome);
    const topPercent = (100 - percentile).toFixed(2);
    const richerThan = MRCalculator.formatNumber(MRCalculator.richerThan(percentile));
    const perSecond = '$' + MRCalculator.perSecond(currentIncome).toFixed(4);
    const perHour = '$' + MRCalculator.perHour(currentIncome).toFixed(2);
    const perDay = '$' + MRCalculator.perDay(currentIncome).toFixed(2);

    const data = {
      topPercent,
      percentile,
      richerThan,
      perSecond,
      perHour,
      perDay,
    };

    const canvas = MRCards.generate(data);
    const preview = document.getElementById('wealth-card-preview');
    if (preview) {
      preview.innerHTML = '';
      const img = document.createElement('img');
      img.src = MRCards.toDataURL(canvas);
      img.alt = 'Your Wealth Card';
      img.style.width = '100%';
      img.style.borderRadius = '12px';
      preview.appendChild(img);
    }

    // Store canvas for download
    this._canvas = canvas;
  },

  downloadCard() {
    if (!this._canvas) this.showPreview();
    if (this._canvas) {
      MRCards.download(this._canvas);
    }
  },

  copyLink() {
    const url = window.location.href.split('?')[0];
    navigator.clipboard.writeText(url).then(() => {
      const btn = document.getElementById('copy-link');
      const original = btn.textContent;
      btn.textContent = 'Copied!';
      btn.style.background = 'rgba(0, 255, 135, 0.2)';
      setTimeout(() => {
        btn.textContent = original;
        btn.style.background = '';
      }, 2000);
    });
  },

  shareTwitter() {
    if (!currentIncome) return;

    const percentile = MRCalculator.globalPercentile(currentIncome);
    const topPercent = (100 - percentile).toFixed(2);
    const richerThan = MRCalculator.formatNumber(MRCalculator.richerThan(percentile));

    const text = encodeURIComponent(
      `I just found out I'm in the top ${topPercent}% globally — richer than ${richerThan} people on Earth.\n\nHow about you? \u{1F440}\n\nmakemerich.app`
    );

    window.open(`https://twitter.com/intent/tweet?text=${text}`, '_blank', 'width=600,height=400');
  },
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  MRShare.init();
});

// Hook into the calculate flow — generate card after results are shown
const originalCalculate = typeof calculate !== 'undefined' ? calculate : null;
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('calculate-btn');
  if (btn) {
    btn.addEventListener('click', () => {
      // Small delay to let results render first
      setTimeout(() => MRShare.showPreview(), 800);
    });
  }
});
