import assert from 'node:assert/strict';
import test from 'node:test';
import { validateRenderManifest } from '../image-deck/manifest.mjs';
import { commercialManifest } from './helpers/image-deck-fixture.mjs';

test('one, two, and three-page decks accept one passing candidate per anchor', () => {
  for (const pageCount of [1, 2, 3, 4]) {
    assert.doesNotThrow(() => validateRenderManifest(commercialManifest(pageCount)));
  }
});

test('the anchor set has exactly min(3, pageCount) distinct existing pages', () => {
  for (const anchorPages of [[], [1], [1, 1], [1, 3], [1, 2, 3]]) {
    const manifest = commercialManifest(2);
    manifest.deck.anchorPages = anchorPages;
    assert.throws(() => validateRenderManifest(manifest), { code: 'INVALID_ANCHOR_PAGES' });
  }
});

test('whole-page candidate count is bounded to three', () => {
  for (const count of [0, -1, 4, 1.5]) {
    const manifest = commercialManifest(1);
    manifest.slides[0].layers[0].visualReview.candidateCount = count;
    assert.throws(() => validateRenderManifest(manifest), { code: 'INVALID_CANDIDATE_BUDGET' });
  }
});

function withHistory() {
  const manifest = commercialManifest(1);
  Object.assign(manifest.slides[0].layers[0].visualReview, {
    candidateCount: 3, selectedCandidate: 3,
    repairRounds: 1, generationAttempts: 2,
    candidateHistory: [
      { repairRounds: 2, generationAttempts: 3 },
      { repairRounds: 0, generationAttempts: 1 },
      { repairRounds: 1, generationAttempts: 2 },
    ],
  });
  return manifest;
}

test('three candidates with at most two local repairs each are valid', () => {
  assert.doesNotThrow(() => validateRenderManifest(withHistory()));
});

test('multi-candidate legacy metadata cannot claim an unrecorded bounded repair budget', () => {
  for (const candidateHistory of [undefined, [{ repairRounds: 0, generationAttempts: 1 }]]) {
    const manifest = withHistory();
    manifest.slides[0].layers[0].visualReview.candidateHistory = candidateHistory;
    assert.throws(() => validateRenderManifest(manifest), { code: 'MISSING_CANDIDATE_HISTORY' });
  }
});

test('every candidate, including an unselected one, must respect its repair budget', () => {
  for (const candidate of [{ repairRounds: 3, generationAttempts: 4 }, { repairRounds: 1, generationAttempts: 1 }]) {
    const manifest = withHistory();
    manifest.slides[0].layers[0].visualReview.candidateHistory[0] = candidate;
    assert.throws(() => validateRenderManifest(manifest), { code: 'CANDIDATE_RETRY_LIMIT' });
  }
});

test('selected candidate and top-level retry metadata must match the recorded history', () => {
  const manifest = withHistory();
  const review = manifest.slides[0].layers[0].visualReview;
  review.selectedCandidate = 4;
  assert.throws(() => validateRenderManifest(manifest), { code: 'INVALID_SELECTED_CANDIDATE' });
  review.selectedCandidate = 1;
  assert.throws(() => validateRenderManifest(manifest), { code: 'CANDIDATE_HISTORY_MISMATCH' });
});
