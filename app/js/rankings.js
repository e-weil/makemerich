/**
 * MakeMeRich Rankings Engine — by CIPHER
 * Handles country-specific rankings and income distribution analysis.
 */

const MRRankings = {

  // Find user's country based on income (best match)
  guessCountry(annualIncome, countries) {
    let bestMatch = null;
    let minDiff = Infinity;

    countries.forEach(c => {
      const diff = Math.abs(c.median_income - annualIncome);
      if (diff < minDiff) {
        minDiff = diff;
        bestMatch = c;
      }
    });

    return bestMatch;
  },

  // Get income bracket label
  getBracket(annualIncome) {
    if (annualIncome >= 500000) return { label: 'Ultra High Income', tier: 5, color: '#FFD700' };
    if (annualIncome >= 150000) return { label: 'High Income', tier: 4, color: '#00ff87' };
    if (annualIncome >= 75000) return { label: 'Upper Middle', tier: 3, color: '#00d4ff' };
    if (annualIncome >= 35000) return { label: 'Middle Income', tier: 2, color: '#a78bfa' };
    if (annualIncome >= 15000) return { label: 'Lower Middle', tier: 1, color: '#f59e0b' };
    return { label: 'Low Income', tier: 0, color: '#ef4444' };
  },

  // Calculate how income compares to world milestones
  milestones(annualIncome) {
    const milestones = [
      { threshold: 700, label: 'Global Poverty Line ($1.90/day)', pct: null },
      { threshold: 2920, label: 'World Median Income', pct: 50 },
      { threshold: 12000, label: 'US Poverty Line (single)', pct: 75 },
      { threshold: 37000, label: 'World Top 10%', pct: 90 },
      { threshold: 55000, label: 'US Median Income', pct: 93 },
      { threshold: 100000, label: 'World Top 3%', pct: 97 },
      { threshold: 250000, label: 'World Top 1%', pct: 99 },
      { threshold: 500000, label: 'World Top 0.5%', pct: 99.5 },
      { threshold: 1000000, label: 'World Top 0.1%', pct: 99.9 },
    ];

    const passed = milestones.filter(m => annualIncome >= m.threshold);
    const next = milestones.find(m => annualIncome < m.threshold);

    return { passed, next };
  },

  // Fun "time equivalents" — how long to earn certain amounts
  timeToEarn(annualIncome) {
    const perSecond = annualIncome / (365.25 * 86400);
    return [
      { item: 'a cup of coffee', amount: 5, time: formatTime(5 / perSecond) },
      { item: 'a nice dinner', amount: 80, time: formatTime(80 / perSecond) },
      { item: 'a new iPhone', amount: 1200, time: formatTime(1200 / perSecond) },
      { item: 'a used car', amount: 15000, time: formatTime(15000 / perSecond) },
      { item: 'a house down payment', amount: 60000, time: formatTime(60000 / perSecond) },
      { item: 'a million dollars', amount: 1000000, time: formatTime(1000000 / perSecond) },
    ];
  },
};

function formatTime(seconds) {
  if (seconds < 60) return Math.round(seconds) + ' seconds';
  if (seconds < 3600) return Math.round(seconds / 60) + ' minutes';
  if (seconds < 86400) return (seconds / 3600).toFixed(1) + ' hours';
  if (seconds < 86400 * 30) return Math.round(seconds / 86400) + ' days';
  if (seconds < 86400 * 365) return (seconds / (86400 * 30)).toFixed(1) + ' months';
  return (seconds / (86400 * 365.25)).toFixed(1) + ' years';
}

if (typeof module !== 'undefined') module.exports = MRRankings;
