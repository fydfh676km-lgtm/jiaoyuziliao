import assert from 'node:assert/strict';
import test from 'node:test';
import { access, mkdtemp, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { renderSlide } from '../image-deck/render.mjs';
import { resolveRuntime } from '../image-deck/runtime.mjs';

const runtime = resolveRuntime();

async function fixture(t, { scale = 1, bodySize = 64, titleSize = 80, overflow = false } = {}) {
  const root = await mkdtemp(path.join(os.tmpdir(), 'edu-ppt-classroom-test-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const content = overflow ? '课堂材料'.repeat(30) : '观察材料，说出依据。';
  const deck = { renderMode: 'deterministic-text', resolution: { width: 1920 * scale, height: 1080 * scale } };
  const layer = (id, source, text, y, size, width, height) => ({
    kind: 'text', id, source, text,
    x: 80 * scale, y: y * scale, width: width * scale, height: height * scale,
    style: { fontSize: size * scale, minFontSize: 16 * scale, lineHeight: 1.2, color: '#111111' },
  });
  const slide = {
    page: 1, title: '观察与发现', content: [content],
    layers: [
      layer('title', 'title', '观察与发现', 50, titleSize, 1400, 140),
      layer('body', 'content[0]', content, 240, bodySize, overflow ? 500 : 1600, overflow ? 180 : 500),
    ],
  };
  return { deck, slide, outputPath: path.join(root, '001.png'), runtime };
}

test('fitting 24pt teaching text fails rather than publishing a tiny-text page', async (t) => {
  const options = await fixture(t, { bodySize: 48 });
  const result = await renderSlide(options);
  assert.equal(result.status, 'fail');
  assert.ok(result.errors.some(({ code, layerIds }) => code === 'TEXT_TOO_SMALL' && layerIds.includes('body')));
  await assert.rejects(access(options.outputPath), { code: 'ENOENT' });
});

test('a 32pt page title fails even when the body satisfies classroom size', async (t) => {
  const options = await fixture(t, { titleSize: 64 });
  const result = await renderSlide(options);
  assert.equal(result.status, 'fail');
  assert.ok(result.errors.some(({ code, layerIds }) => code === 'TEXT_TOO_SMALL' && layerIds.includes('title')));
  await assert.rejects(access(options.outputPath), { code: 'ENOENT' });
});

for (const scale of [1, 2]) {
  test(`40pt title and 32pt body publish unchanged at ${1920 * scale}x${1080 * scale}`, async (t) => {
    const options = await fixture(t, { scale });
    const result = await renderSlide(options);
    assert.equal(result.status, 'pass', JSON.stringify(result.errors));
    assert.deepEqual(result.textChecks.map(({ fontSize }) => fontSize), [80 * scale, 64 * scale]);
    assert.equal(result.attempts, 0);
    await access(options.outputPath);
  });
}

test('overflow is reported without shrinking or compressing approved teaching copy', async (t) => {
  const options = await fixture(t, { bodySize: 72, overflow: true });
  const result = await renderSlide(options);
  assert.equal(result.status, 'fail');
  assert.ok(result.errors.some(({ code }) => code === 'TEXT_OVERFLOW'));
  const body = result.textChecks.find(({ id }) => id === 'body');
  assert.equal(body.fontSize, 72);
  assert.equal(body.actualText, options.slide.content[0]);
  assert.ok(Math.abs(body.lineHeight - 1.2) < 0.001);
  assert.equal(result.attempts, 0);
  await assert.rejects(access(options.outputPath), { code: 'ENOENT' });
});
