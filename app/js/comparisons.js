/**
 * MakeMeRich Comparisons Engine — by CIPHER
 * The viral sauce. These comparisons are what people screenshot and share.
 */

const MRComparisons = {

  // Generate mind-blowing comparisons
  generate(annualIncome, billionaires) {
    const comparisons = [];
    const perSecond = annualIncome / (365.25 * 86400);

    // vs each billionaire
    billionaires.forEach(b => {
      const ratio = b.per_second / perSecond;
      const timeForYourSalary = annualIncome / b.per_second;

      comparisons.push({
        type: 'billionaire',
        name: b.name,
        emoji: b.emoji,
        company: b.company,
        ratio: ratio,
        time: formatDuration(timeForYourSalary),
        mindBlower: generateMindBlower(ratio, b.name, annualIncome),
      });
    });

    return comparisons;
  },

  // "Dropped money" comparison
  // A billionaire literally shouldn't pick up a $100 bill — they earn more in the time it takes
  droppedMoney(annualIncome, billionairePerSecond) {
    const userPerSecond = annualIncome / (365.25 * 86400);
    const pickUpTime = 5; // seconds to bend down and pick up money
    const userEarnsDuringPickup = userPerSecond * pickUpTime;
    const billionaireEarnsDuringPickup = billionairePerSecond * pickUpTime;

    return {
      worthPickingUp: {
        user: userEarnsDuringPickup < 0.01 ? '$0.01' : '$' + Math.floor(userEarnsDuringPickup),
        billionaire: '$' + Math.floor(billionaireEarnsDuringPickup),
      },
      insight: billionaireEarnsDuringPickup > 100
        ? `They earn $${Math.floor(billionaireEarnsDuringPickup)} in the 5 seconds it takes to pick up a $100 bill. It's literally not worth their time.`
        : `They earn $${billionaireEarnsDuringPickup.toFixed(2)} in 5 seconds.`,
    };
  },

  // Scale comparison — if your income was a height
  scaleComparison(annualIncome, billionaireNetWorth) {
    // If your income = 1 meter, billionaire net worth = ?
    const ratio = (billionaireNetWorth * 1e9) / annualIncome;

    if (ratio > 1e6) return `${(ratio / 1000).toFixed(0)} km (${(ratio / 1000 * 0.621).toFixed(0)} miles) — past the International Space Station`;
    if (ratio > 1e4) return `${(ratio).toFixed(0)} meters — taller than Mount Everest`;
    if (ratio > 1000) return `${(ratio).toFixed(0)} meters — a skyscraper`;
    return `${ratio.toFixed(0)} meters`;
  },
};

function generateMindBlower(ratio, name, income) {
  if (ratio > 100000) {
    return `${name} earns your entire annual income every ${formatDuration(income / (ratio * income / (365.25 * 86400)))}.`;
  }
  if (ratio > 10000) {
    return `You'd need to work ${Math.round(ratio)} years to earn what ${name} makes in one year.`;
  }
  if (ratio > 1000) {
    return `${name} makes in a single day what takes you ${Math.round(ratio / 365)} years.`;
  }
  return `${name} earns ${Math.round(ratio)}x what you make.`;
}

function formatDuration(seconds) {
  if (seconds < 1) return 'less than a second';
  if (seconds < 60) return Math.round(seconds) + ' seconds';
  if (seconds < 3600) return (seconds / 60).toFixed(1) + ' minutes';
  if (seconds < 86400) return (seconds / 3600).toFixed(1) + ' hours';
  if (seconds < 86400 * 30) return (seconds / 86400).toFixed(1) + ' days';
  if (seconds < 86400 * 365.25) return (seconds / (86400 * 30)).toFixed(1) + ' months';
  return (seconds / (86400 * 365.25)).toFixed(1) + ' years';
}

if (typeof module !== 'undefined') module.exports = MRComparisons;
