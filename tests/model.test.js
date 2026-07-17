const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const projectRoot = path.resolve(__dirname, '..');
const sourcePath = path.join(projectRoot, 'src', 'black-hole-accretion-motion-lab.html');
const standalonePath = path.join(projectRoot, 'index.html');
const source = fs.readFileSync(sourcePath, 'utf8');
const standalone = fs.readFileSync(standalonePath, 'utf8');

const scriptStart = source.indexOf('<script>');
const scriptEnd = source.lastIndexOf('</script>');
assert(scriptStart >= 0 && scriptEnd > scriptStart, 'inline script must exist');
assert.doesNotThrow(
  () => new Function(source.slice(scriptStart + '<script>'.length, scriptEnd)),
  'inline JavaScript must parse'
);

const ids = [...source.matchAll(/id="([^"]+)"/g)].map((match) => match[1]);
assert.equal(new Set(ids).size, ids.length, 'element IDs must be unique');
assert(!/<(?:html|head|body)\b/i.test(source), 'editable source must remain an HTML fragment');
assert(!source.includes('fetch('), 'visualization must not fetch external data');
assert(standalone.includes('black-hole-accretion-motion-lab'), 'standalone page must embed the model');

[
  'float orbitalPhase = azimuth - uTime * orbitalRate * 2.6;',
  'float accretionTemperature = mix(0.30, 1.18,',
  'float mappedEmission = radiance / (0.72 + radiance);',
  'color = mix(uBackground, diskColor, clamp(mappedEmission, 0.0, 0.98));',
  'color = mix(color, ringColor, ringStrength);',
  'Math.min(0.5, Math.max(0, (now - lastFrameTime) / 1000))',
  '减少动态 · 点击启动'
].forEach((token) => {
  assert(source.includes(token), `missing source invariant: ${token}`);
  assert(standalone.includes(token), `standalone page is stale: ${token}`);
});

assert(!source.includes('uBackground + diskColor * emission'), 'additive disk saturation must stay removed');
assert(!source.includes('uSeries1 * ring * (0.42 + 1.35 * uAccretion)'), 'additive ring saturation must stay removed');

function calculateIsco(spin) {
  const z1 = 1 + Math.cbrt(1 - spin * spin) *
    (Math.cbrt(1 + spin) + Math.cbrt(1 - spin));
  const z2 = Math.sqrt(3 * spin * spin + z1 * z1);
  return 3 + z2 - Math.sqrt((3 - z1) * (3 + z1 + 2 * z2));
}

const iscoSamples = [0, 0.5, 0.72, 0.9, 0.98].map(calculateIsco);
assert(Math.abs(iscoSamples[0] - 6) < 1e-12, 'Schwarzschild ISCO must equal 6 r_g');
for (let index = 1; index < iscoSamples.length; index += 1) {
  assert(iscoSamples[index] < iscoSamples[index - 1], 'prograde ISCO must shrink with spin');
}

function mappedEmission(accretion, temperature = 0.22, filaments = 1, beaming = 1) {
  const luminosity = Math.pow(accretion, 0.82);
  const radiance = luminosity * (0.18 + 4.4 * temperature) * filaments * beaming;
  return radiance / (0.72 + radiance);
}

const accretionSamples = [0, 0.1, 0.5, 1].map((value) => mappedEmission(value));
for (let index = 1; index < accretionSamples.length; index += 1) {
  assert(accretionSamples[index] > accretionSamples[index - 1], 'mapped disk brightness must rise with accretion');
}
assert(accretionSamples[3] - accretionSamples[1] > 0.3, '10% to 100% accretion must remain visibly separated');
assert(accretionSamples[3] < 0.8, 'nominal disk emission must retain highlight headroom');

function accretionTemperature(accretion) {
  return 0.30 + (1.18 - 0.30) * Math.pow(Math.max(accretion, 0.0001), 0.25);
}

assert(accretionTemperature(1) > accretionTemperature(0.1), 'color temperature must rise with accretion');

const defaultArealRg = 3.3;
const defaultSpin = 0.72;
const orbitalRate = 2.4 / (Math.pow(defaultArealRg, 1.5) + defaultSpin);
const spiralPhaseTravel = orbitalRate * 2.6 * 7 * 1.5;
assert(spiralPhaseTravel > 2, 'spiral texture must move clearly over 1.5 seconds');

console.log('model tests passed');
console.log(`ids=${ids.length} isco=${iscoSamples.map((value) => value.toFixed(4)).join(',')}`);
console.log(`mapped accretion=${accretionSamples.map((value) => value.toFixed(3)).join(',')}`);
console.log(`spiral phase travel in 1.5s=${spiralPhaseTravel.toFixed(2)} rad`);
