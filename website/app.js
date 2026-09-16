const missions = [
  ['Voyager 1', 'Interstellar', 1977, 'Active'],
  ['Cassini', 'Saturn', 1997, 'Complete'],
  ['New Horizons', 'Pluto', 2006, 'Active'],
  ['Juno', 'Jupiter', 2011, 'Active'],
  ['Perseverance', 'Mars', 2020, 'Active'],
];
const examples = {
  missions: {sql: '-- A small dataset. A bigger perspective.\nSELECT name, destination, launched, status\nFROM missions\nORDER BY launched;\n\n-- What will you discover?', columns: ['name', 'destination', 'launched', 'status'], rows: missions},
  summary: {sql: '-- Find the missions still exploring.\nSELECT status, COUNT(*) AS missions\nFROM missions\nGROUP BY status\nORDER BY missions DESC;\n', columns: ['status', 'missions'], rows: [['Active', 4], ['Complete', 1]]},
};
let selected = 'missions';
function showCode() {
  const code = document.querySelector('#query-code');
  code.replaceChildren();
  for (const token of examples[selected].sql.split(/(--[^\n]*|\b(?:SELECT|FROM|ORDER BY|GROUP BY|DESC|COUNT|AS)\b)/g)) {
    const span = document.createElement('span');
    span.textContent = token;
    if (token.startsWith('--')) span.className = 'sql-comment';
    else if (/^(SELECT|FROM|ORDER BY|GROUP BY|DESC|COUNT|AS)$/.test(token)) span.className = 'sql-keyword';
    code.append(span);
  }
}
function showResults() {
  const example = examples[selected];
  const table = document.querySelector('#result-table');
  const head = document.createElement('thead');
  const row = head.insertRow();
  for (const title of example.columns) { const cell = document.createElement('th'); cell.scope = 'col'; cell.textContent = title; row.append(cell); }
  const body = document.createElement('tbody');
  for (const values of example.rows) { const tr = body.insertRow(); for (const value of values) tr.insertCell().textContent = value; }
  table.replaceChildren(head, body);
  document.querySelector('#result-count').textContent = example.rows.length + ' rows';
}
document.querySelectorAll('[data-query]').forEach(tab => tab.addEventListener('click', () => {
  selected = tab.dataset.query;
  document.querySelectorAll('[data-query]').forEach(item => item.setAttribute('aria-selected', String(item === tab)));
  showCode();
  document.querySelector('#query-status').textContent = 'Ready to run example';
}));
document.querySelector('#run-query').addEventListener('click', () => { showResults(); document.querySelector('#query-status').textContent = 'Example complete · sample data'; });
document.querySelector('#copy-install').addEventListener('click', async event => {
  try { await navigator.clipboard.writeText(document.querySelector('#install-code').textContent); event.target.textContent = 'Copied!'; }
  catch { event.target.textContent = 'Select text to copy'; }
  setTimeout(() => { event.target.textContent = 'Copy'; }, 2500);
});
document.querySelector('#year').textContent = new Date().getFullYear();
showCode();
showResults();
