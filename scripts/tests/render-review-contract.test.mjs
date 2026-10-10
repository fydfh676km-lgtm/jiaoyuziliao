import assert from 'node:assert/strict';
import test from 'node:test';
import { buildLayerHtml, buildSlideHtml } from '../image-deck/html.mjs';
import { normalizeManifest, validateRenderManifest } from '../image-deck/manifest.mjs';
import { commercialManifest, reviewedImage, reviewChecks } from './helpers/image-deck-fixture.mjs';

test('a documented commercial manifest also passes HTML construction', () => {
  const manifest = normalizeManifest(commercialManifest(), process.cwd());

  assert.doesNotThrow(() => validateRenderManifest(manifest));
  for (const slide of manifest.slides) {
    assert.match(buildSlideHtml(manifest.deck, slide), /data-layer="whole-slide"/u);
  }
});

test('commercial review cannot pass with an impossible match ratio or score', () => {
  const manifest = commercialManifest(1);
  const review = manifest.slides[0].layers[0].visualReview;
  review.ocr.bodyMatchRatio = 10;
  assert.throws(() => validateRenderManifest(manifest), { code: 'WHOLE_SLIDE_OCR_FAILED' });
  review.ocr.bodyMatchRatio = 1;
  review.commercialScores.contentIntegration = 1000;
  assert.throws(() => validateRenderManifest(manifest), { code: 'COMMERCIAL_SCORE_FAILED' });
});

for (const renderMode of Object.keys(reviewChecks)) {
  const html = (layer) => buildLayerHtml({ renderMode }, { page: 1 }, layer);

  test(`${renderMode} accepts its own complete generated-asset review`, () => {
    assert.match(html(reviewedImage(renderMode)), /^<img /u);
  });

  test(`${renderMode} rejects unreviewed assets and every missing required check`, () => {
    const unreviewed = reviewedImage(renderMode);
    delete unreviewed.visualReview;
    assert.throws(() => html(unreviewed), { code: 'GENERATED_ASSET_NOT_REVIEWED' });
    const failed = reviewedImage(renderMode);
    failed.visualReview.status = 'fail';
    assert.throws(() => html(failed), { code: 'GENERATED_ASSET_NOT_REVIEWED' });
    for (const missing of reviewChecks[renderMode]) {
      const layer = reviewedImage(renderMode);
      layer.visualReview.checkedFor = layer.visualReview.checkedFor.filter((check) => check !== missing);
      assert.throws(() => html(layer), { code: 'GENERATED_ASSET_NOT_REVIEWED' }, missing);
    }
  });

  test(`${renderMode} preserves retry metadata restrictions`, () => {
    for (const [repairRounds, generationAttempts] of [[3, 4], [-1, 0], [0, 2], [0.5, 1.5]]) {
      const layer = reviewedImage(renderMode);
      Object.assign(layer.visualReview, { repairRounds, generationAttempts });
      assert.throws(() => html(layer), { code: 'GENERATED_ASSET_RETRY_LIMIT' });
    }
  });

  test(`${renderMode} still rejects generated non-raster assets`, () => {
    const layer = reviewedImage(renderMode);
    layer.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"/>';
    assert.throws(() => html(layer), /GENERATED_ASSET_NOT_RASTER/u);
  });
}
