/**
 * MakeMeRich App — Main Controller — by CIPHER
 * Wires up the UI to the calculation engine.
 */

// Global state
let currentIncome = 0;
let pageOpenTime = 0;
let liveCounterInterval = null;
let countriesData = [];
let billionairesData = [];
let tipsData = [];

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
  // Load data files
  await loadData();

  // Setup input handling
  setupInput();

  // Setup buttons
  setupButtons();
});

async function loadData() {
  try {
    const [countries, billionaires, tips] = await Promise.all([
      fetch('data/countries.json').then(r => r.json()),
      fetch('data/billionaires.json').then(r => r.json()),
      fetch('data/tips.json').then(r => r.json()),
    ]);
    countriesData = countries;
    billionairesData = billionaires;
    tipsData = tips;
  } catch (e) {
    console.error('Failed to load data:', e);
  }
}

function setupInput() {
  const input = document.getElementById('income-input');
  const btn = document.getElementById('calculate-btn');

  // Format input as user types (add commas)
  input.addEventListener('input', (e) => {
    let value = e.target.value.replace(/[^0-9]/g, '');
    if (value) {
      value = parseInt(value).toLocaleString('en-US');
      btn.disabled = false;
    } else {
      btn.disabled = true;
    }
    e.target.value = value;
  });

  // Enter key triggers calculate
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !btn.disabled) {
      calculate();
    }
  });

  // Focus input on page load
  setTimeout(() => input.focus(), 500);
}

function setupButtons() {
  document.getElementById('calculate-btn').addEventListener('click', calculate);
  document.getElementById('reset-btn').addEventListener('click', reset);
}

function calculate() {
  const input = document.getElementById('income-input');
  currentIncome = parseInt(input.value.replace(/[^0-9]/g, ''));

  if (!currentIncome || currentIncome <= 0) return;

  // Calculate everything
  renderRanking();
  renderMoneyClock();
  renderBillionaires();
  renderPurchasingPower();
  renderWhatItBuys();
  renderDailyTip();

  // Start live counter
  startLiveCounter();

  // Show results with animation
  document.getElementById('hero').classList.add('collapsed');
  const results = document.getElementById('results');
  results.classList.remove('hidden');

  // Scroll to results
  setTimeout(() => {
    results.scrollIntoView({ behavior: 'smooth' });
  }, 300);

  // Animate cards appearing one by one
  const cards = results.querySelectorAll('.result-card');
  cards.forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(40px)';
    setTimeout(() => {
      card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 200 + i * 150);
  });
}

function renderRanking() {
  const percentile = MRCalculator.globalPercentile(currentIncome);
  const topPercent = (100 - percentile).toFixed(2);
  const richerThan = MRCalculator.richerThan(percentile);

  document.getElementById('percentile').textContent = topPercent;
  document.getElementById('richer-than').innerHTML =
    `You're richer than <strong>${MRCalculator.formatNumber(richerThan)}</strong> people on Earth`;

  // Animate ranking bar
  const fill = document.getElementById('ranking-fill');
  const marker = document.getElementById('ranking-marker');
  setTimeout(() => {
    fill.style.width = percentile + '%';
    marker.style.left = percentile + '%';
  }, 500);
}

function renderMoneyClock() {
  const perSec = MRCalculator.perSecond(currentIncome);
  const perMin = MRCalculator.perMinute(currentIncome);
  const perHr = MRCalculator.perHour(currentIncome);
  const perDay = MRCalculator.perDay(currentIncome);

  document.getElementById('per-second').textContent = '$' + perSec.toFixed(4);
  document.getElementById('per-minute').textContent = '$' + perMin.toFixed(3);
  document.getElementById('per-hour').textContent = '$' + perHr.toFixed(2);
  document.getElementById('per-day').textContent = '$' + perDay.toFixed(2);
}

function startLiveCounter() {
  pageOpenTime = Date.now();
  if (liveCounterInterval) clearInterval(liveCounterInterval);

  const perMs = currentIncome / (365.25 * 24 * 3600 * 1000);
  const el = document.getElementById('live-earnings');

  liveCounterInterval = setInterval(() => {
    const elapsed = Date.now() - pageOpenTime;
    const earned = elapsed * perMs;
    el.textContent = '$' + earned.toFixed(4);
    el.style.transform = 'scale(1.02)';
    setTimeout(() => { el.style.transform = 'scale(1)'; }, 100);
  }, 100);
}

function renderBillionaires() {
  const container = document.getElementById('billionaire-list');
  container.innerHTML = '';

  const top5 = billionairesData.slice(0, 8);

  top5.forEach(b => {
    const time = MRCalculator.billionaireTime(currentIncome, b.per_second);
    const div = document.createElement('div');
    div.className = 'billionaire-item';
    div.innerHTML = `
      <div class="billionaire-info">
        <span class="billionaire-emoji">${b.emoji}</span>
        <div>
          <strong>${b.name}</strong>
          <span class="billionaire-company">${b.company}</span>
        </div>
      </div>
      <div class="billionaire-stat">
        <span class="billionaire-time">${time}</span>
        <span class="billionaire-label">to earn your annual income</span>
      </div>
    `;
    container.appendChild(div);
  });
}

function renderPurchasingPower() {
  const container = document.getElementById('country-list');
  container.innerHTML = '';

  // Pick interesting countries (expensive and cheap)
  const interesting = ['CH', 'NO', 'US', 'JP', 'DE', 'GB', 'KR', 'BR', 'MX', 'TH', 'IN', 'VN', 'PH', 'NG', 'EG'];
  const selected = countriesData.filter(c => interesting.includes(c.code));

  selected.forEach(country => {
    const adjustedIncome = MRCalculator.purchasingPower(currentIncome, country.cost_index);
    const localPercentile = MRCalculator.countryPercentile(adjustedIncome, country.median_income);

    let status, statusClass;
    if (localPercentile > 80) { status = 'Rich'; statusClass = 'status-rich'; }
    else if (localPercentile > 50) { status = 'Comfortable'; statusClass = 'status-comfortable'; }
    else if (localPercentile > 30) { status = 'Average'; statusClass = 'status-average'; }
    else { status = 'Struggling'; statusClass = 'status-poor'; }

    const div = document.createElement('div');
    div.className = 'country-card';
    div.innerHTML = `
      <span class="country-flag">${country.flag}</span>
      <strong class="country-name">${country.country}</strong>
      <span class="country-equivalent">${MRCalculator.formatCurrency(adjustedIncome)}</span>
      <span class="country-status ${statusClass}">${status}</span>
      <span class="country-percentile">Top ${(100 - localPercentile).toFixed(0)}%</span>
    `;
    container.appendChild(div);
  });
}

function renderWhatItBuys() {
  const container = document.getElementById('buys-list');
  container.innerHTML = '';

  const items = MRCalculator.whatItBuys(currentIncome);

  items.forEach(item => {
    const div = document.createElement('div');
    div.className = 'buys-item';
    div.innerHTML = `
      <span class="buys-emoji">${item.emoji}</span>
      <span class="buys-quantity">${MRCalculator.formatNumber(item.quantity)}</span>
      <span class="buys-name">${item.name}</span>
    `;
    container.appendChild(div);
  });
}

function renderDailyTip() {
  const dayOfYear = Math.floor((Date.now() - new Date(new Date().getFullYear(), 0, 0)) / 86400000);
  const tipIndex = dayOfYear % tipsData.length;
  const tip = tipsData[tipIndex];

  document.getElementById('daily-tip').textContent = tip.tip;
  document.getElementById('tip-category').textContent = tip.category;
}

function reset() {
  if (liveCounterInterval) clearInterval(liveCounterInterval);

  document.getElementById('hero').classList.remove('collapsed');
  document.getElementById('results').classList.add('hidden');
  document.getElementById('income-input').value = '';
  document.getElementById('calculate-btn').disabled = true;

  window.scrollTo({ top: 0, behavior: 'smooth' });
  setTimeout(() => document.getElementById('income-input').focus(), 500);
}
