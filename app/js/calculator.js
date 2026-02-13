/**
 * MakeMeRich Calculator Engine — by ATLAS
 * Pure math. No AI. No API calls. Just numbers that change perspectives.
 */

const MRCalculator = {

  // Calculate earnings per time unit
  perSecond(annualIncome) {
    return annualIncome / (365.25 * 24 * 3600);
  },

  perMinute(annualIncome) {
    return annualIncome / (365.25 * 24 * 60);
  },

  perHour(annualIncome) {
    return annualIncome / (365.25 * 24);
  },

  perDay(annualIncome) {
    return annualIncome / 365.25;
  },

  // Global percentile ranking
  // Based on World Bank income distribution data
  // Uses log-normal distribution approximation
  globalPercentile(annualIncome) {
    // World median income ~$2,920/year (PPP adjusted ~$8,500)
    // We use nominal USD for dramatic effect
    const worldMedian = 2920;
    const logIncome = Math.log(annualIncome);
    const logMedian = Math.log(worldMedian);
    const sigma = 1.15; // approximate log-normal std dev of global income

    // CDF of log-normal
    const z = (logIncome - logMedian) / sigma;
    const percentile = 0.5 * (1 + erf(z / Math.sqrt(2)));
    return Math.min(percentile * 100, 99.99);
  },

  // Country ranking — what percentile within a country
  countryPercentile(annualIncome, medianIncome) {
    const sigma = 0.85;
    const z = (Math.log(annualIncome) - Math.log(medianIncome)) / sigma;
    const percentile = 0.5 * (1 + erf(z / Math.sqrt(2)));
    return Math.min(percentile * 100, 99.99);
  },

  // How many people you're richer than (out of 8 billion)
  richerThan(percentile) {
    return Math.floor((percentile / 100) * 8000000000);
  },

  // Time for a billionaire to earn your annual income
  billionaireTime(annualIncome, billionairePerSecond) {
    const seconds = annualIncome / billionairePerSecond;
    if (seconds < 60) return `${seconds.toFixed(1)} seconds`;
    if (seconds < 3600) return `${(seconds / 60).toFixed(1)} minutes`;
    if (seconds < 86400) return `${(seconds / 3600).toFixed(1)} hours`;
    return `${(seconds / 86400).toFixed(1)} days`;
  },

  // Purchasing power in different countries
  purchasingPower(annualIncome, costIndex) {
    return annualIncome / costIndex;
  },

  // Years to reach a target net worth (with compound growth)
  yearsToTarget(annualIncome, savingsRate, targetAmount, annualReturn = 0.07) {
    const annualSavings = annualIncome * savingsRate;
    if (annualSavings <= 0) return Infinity;

    // FV = PMT * ((1 + r)^n - 1) / r
    // Solve for n: n = log(FV * r / PMT + 1) / log(1 + r)
    const n = Math.log((targetAmount * annualReturn) / annualSavings + 1) / Math.log(1 + annualReturn);
    return Math.ceil(n);
  },

  // Lifetime earnings estimate
  lifetimeEarnings(annualIncome, currentAge, retirementAge = 65, annualRaise = 0.03) {
    let total = 0;
    let salary = annualIncome;
    for (let age = currentAge; age < retirementAge; age++) {
      total += salary;
      salary *= (1 + annualRaise);
    }
    return total;
  },

  // What your money buys (fun comparisons)
  whatItBuys(annualIncome) {
    const items = [
      { name: "Big Macs", price: 5.50, emoji: "🍔" },
      { name: "iPhone 16 Pros", price: 1199, emoji: "📱" },
      { name: "Tesla Model 3s", price: 42000, emoji: "🚗" },
      { name: "round-the-world flights", price: 3500, emoji: "✈️" },
      { name: "years of Netflix", price: 180, emoji: "🎬" },
      { name: "Bitcoin (at current ~$100k)", price: 100000, emoji: "₿" },
      { name: "Starbucks lattes", price: 6, emoji: "☕" },
      { name: "months of NYC rent", price: 3500, emoji: "🏠" },
      { name: "college semesters (US avg)", price: 22000, emoji: "🎓" },
    ];
    return items.map(item => ({
      ...item,
      quantity: Math.floor(annualIncome / item.price),
    }));
  },

  // Format number with commas
  formatNumber(num) {
    if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
    if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
    if (num >= 1e3) return num.toLocaleString('en-US', { maximumFractionDigits: 0 });
    return num.toFixed(4);
  },

  formatCurrency(num) {
    if (num >= 1e9) return '$' + (num / 1e9).toFixed(2) + 'B';
    if (num >= 1e6) return '$' + (num / 1e6).toFixed(2) + 'M';
    return '$' + num.toLocaleString('en-US', { maximumFractionDigits: 2 });
  },
};

// Error function (erf) — needed for normal distribution CDF
function erf(x) {
  const a1 =  0.254829592;
  const a2 = -0.284496736;
  const a3 =  1.421413741;
  const a4 = -1.453152027;
  const a5 =  1.061405429;
  const p  =  0.3275911;

  const sign = x < 0 ? -1 : 1;
  x = Math.abs(x);
  const t = 1.0 / (1.0 + p * x);
  const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
  return sign * y;
}

// Export for use in other modules
if (typeof module !== 'undefined') module.exports = MRCalculator;
