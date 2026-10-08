// Run the real offline-app regex parsers against the editable JSON, pre-build.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'pulse-aneesh.html'), 'utf8');
function extract(name) {
  const start = html.indexOf(`function ${name}(`);
  assert(start >= 0, `missing app function ${name}`);
  const end = html.indexOf('\n}', start);
  // escapeHtml is a one-line function; the other parsers close at line start.
  return name === 'escapeHtml' ? html.slice(start, html.indexOf('\n', start)) : html.slice(start, end + 2);
}
const context = vm.createContext({});
vm.runInContext(['parseMatch', 'fillupHtml', 'matchOptHtml', 'splitExp', 'escapeHtml'].map(extract).join('\n'), context);
function validateQuestion(q) {
  assert.equal(context.splitExp(q.exp).page, String(q.page), `${q.id}: splitExp`);
  if (q.fmt === 'fillup') {
    assert(q.q.includes('____'), `${q.id}: missing literal blank`);
    assert(context.fillupHtml(q.q).includes('class="blank"'), `${q.id}: fillup renderer`);
  }
  if (q.fmt !== 'match') return;
  assert(q.q.includes(' — 1) ') && q.q.includes(' … A) '), `${q.id}: exact match grammar`);
  const parsed = context.parseMatch(q.q);
  assert(parsed, `${q.id}: parseMatch returned null`);
  const n = parsed.left.length;
  assert(n >= 2 && n <= 9 && n === parsed.right.length, `${q.id}: equal 2–9 item columns`);
  const leftLabels = [...q.q.split(' … ')[0].matchAll(/(?:^|\s)(\d+)\)\s/g)].map(m => +m[1]);
  const rightLabels = [...q.q.split(' … ')[1].matchAll(/(?:^|\s)([A-Z])\)\s/g)].map(m => m[1]);
  assert.deepEqual(leftLabels, Array.from({length: n}, (_, i) => i + 1), `${q.id}: nested/nonsequential left tokens`);
  assert.deepEqual(rightLabels, Array.from({length: n}, (_, i) => String.fromCharCode(65 + i)), `${q.id}: nested/nonsequential right tokens`);
  for (const item of [...parsed.left, ...parsed.right]) {
    assert(!/(?:^|\s)(?:\d+|[A-Z])\)\s/.test(item), `${q.id}: reserved token inside item`);
  }
  q.opts.forEach((opt, i) => {
    const pairs = opt.split(/\s*,\s*/);
    assert.equal(pairs.length, n, `${q.id}: option missing left items`);
    const decoded = pairs.map(p => {
      const m = p.match(/^(\d)\s*[-–]\s*([A-Z])$/);
      assert(m, `${q.id}: matchOptHtml pair syntax`);
      return [+m[1], m[2].charCodeAt(0) - 65];
    });
    assert.deepEqual(decoded.map(p => p[0]).sort((a,b) => a-b), leftLabels, `${q.id}: left coverage`);
    assert(decoded.every(p => p[1] >= 0 && p[1] < n), `${q.id}: right out of range`);
    if (i === q.ans) assert.equal(new Set(decoded.map(p => p[1])).size, n, `${q.id}: answer is not a bijection`);
    assert.equal((context.matchOptHtml(opt).match(/class="mpair"/g) || []).length, n, `${q.id}: option rendering`);
  });
}
let count = 0;
for (const file of fs.readdirSync(path.join(root, 'data')).filter(f => /^ch\d+\.json$/.test(f))) {
  for (const q of JSON.parse(fs.readFileSync(path.join(root, 'data', file), 'utf8')).questions) {
    validateQuestion(q); count++;
  }
}
// Negative controls verify the gate actually rejects the common authoring errors.
const fixture = {id:'test', page:383, fmt:'match', q:'Match — 1) alpha 2) beta 3) gamma … A) one B) two C) three', opts:['1-A, 2-B, 3-C','1-B, 2-A, 3-C','1-C, 2-B, 3-A','1-A, 2-C, 3-B'], ans:0, exp:'Example. (Book p383)'};
validateQuestion(fixture);
assert.throws(() => validateQuestion({...fixture, q:fixture.q.replace(' … ', ' / ')}));
assert.throws(() => validateQuestion({...fixture, opts:['1-A, 2-A, 3-C', ...fixture.opts.slice(1)]}));
assert.throws(() => validateQuestion({...fixture, opts:['1-A, 2-B', ...fixture.opts.slice(1)]}));
assert.throws(() => validateQuestion({...fixture, q:fixture.q.replace('alpha', 'alpha 4) nested')}));
assert.throws(() => validateQuestion({...fixture, fmt:'fillup', q:'No blank here'}));
console.log(`PASS: actual parseMatch/fillupHtml/matchOptHtml/splitExp on ${count} questions + 5 rejection controls`);
