import assert from 'node:assert/strict';
import test from 'node:test';
import { access, mkdir, mkdtemp, rm, symlink, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { normalizeManifest, validateRenderManifest } from '../image-deck/manifest.mjs';
import { renderSlide } from '../image-deck/render.mjs';
import { resolveRuntime } from '../image-deck/runtime.mjs';
import { commercialManifest } from './helpers/image-deck-fixture.mjs';

const runtime = resolveRuntime();

async function fixture(t, imageWidth, imageHeight) {
  const root = await mkdtemp(path.join(os.tmpdir(), 'edu-ppt-render-test-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const projectRoot = path.join(root, 'project');
  await mkdir(projectRoot);
  const src = path.join(projectRoot, 'source.png');
  const bytes = await runtime.sharp({ create: { width: imageWidth, height: imageHeight, channels: 3, background: '#fff' } }).png().toBuffer();
  await writeFile(src, bytes);
  const raw = commercialManifest(1, { src, width: 160, height: 90 });
  const manifest = normalizeManifest(raw, projectRoot, { projectRoot });
  validateRenderManifest(manifest);
  return { root, projectRoot, src, bytes, raw, manifest, outputPath: path.join(projectRoot, '001.png') };
}

test('Playwright decodes authorized local PNGs from the renderer HTML', async (t) => {
  const { manifest, outputPath } = await fixture(t, 320, 180);
  const result = await renderSlide({ deck: manifest.deck, slide: manifest.slides[0], outputPath, runtime });
  assert.equal(result.status, 'pass', JSON.stringify(result.errors));
  assert.deepEqual(result.assetChecks.map(({ decoded, naturalWidth, naturalHeight }) => ({ decoded, naturalWidth, naturalHeight })), [
    { decoded: true, naturalWidth: 320, naturalHeight: 180 },
  ]);
  await access(outputPath);
});

test('a nonmatching whole-slide aspect ratio fails without publishing a cropped PNG', async (t) => {
  const { manifest, outputPath } = await fixture(t, 300, 200);
  const result = await renderSlide({ deck: manifest.deck, slide: manifest.slides[0], outputPath, runtime });
  assert.equal(result.status, 'fail');
  assert.deepEqual(result.errors.map(({ code }) => code), ['WHOLE_SLIDE_ASPECT_RATIO_MISMATCH']);
  await assert.rejects(access(outputPath), { code: 'ENOENT' });
});

test('local-image embedding retains lexical and symlink project authorization', async (t) => {
  const { root, projectRoot, bytes, raw } = await fixture(t, 160, 90);
  const outside = path.join(root, 'outside.png');
  await writeFile(outside, bytes);
  raw.slides[0].layers[0].src = outside;
  assert.throws(() => normalizeManifest(raw, projectRoot, { projectRoot }), { code: 'ASSET_OUTSIDE_PROJECT' });
  const linked = path.join(projectRoot, 'linked.png');
  await symlink(outside, linked);
  raw.slides[0].layers[0].src = linked;
  assert.throws(() => normalizeManifest(raw, projectRoot, { projectRoot }), { code: 'ASSET_OUTSIDE_PROJECT' });
});
