import { createHash } from 'node:crypto';
import { accessSync, constants, readFileSync, realpathSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DEFAULT_ASPECT_RATIO = '16:9';
const DEFAULT_RESOLUTION = { width: 3840, height: 2160 };
const REQUIRED_REVIEW_CHECKS = [
  'pseudo-text',
  'watermark',
  'logo',
  'reference-copying',
  'safe-text-region',
];
const WHOLE_SLIDE_REVIEW_CHECKS = [
  'watermark',
  'logo',
  'reference-copying',
  'ocr-text',
  'commercial-quality',
  'style-continuity',
  'page-specific-relevance',
];
const COMMERCIAL_SCORE_FIELDS = [
  'contentIntegration',
  'visualHierarchy',
  'pageSpecificity',
  'styleContinuity',
  'compositionQuality',
  'artifactCleanliness',
];
const REQUIRED_SLIDE_FIELDS = [
  'title',
  'content',
  'layout',
  'elements',
  'elementStyle',
  'emphasis',
];
const REQUIRED_COURSEWARE_THEME_FIELDS = [
  'topicFamily',
  'visualWorld',
  'material',
  'imageryLanguage',
];
const REQUIRED_COURSEWARE_DESIGN_FIELDS = [
  'pageRole',
  'instructionalAction',
  'focalPoint',
  'composition',
  'textSafeZone',
  'readingPath',
  'density',
  'continuityCue',
];
const COURSEWARE_DENSITIES = new Set(['immersive', 'light', 'standard', 'dense']);

export class ManifestError extends Error {
  constructor(code, message, details = {}) {
    super(`${code}: ${message}`);
    this.name = 'ManifestError';
    this.code = code;
    this.details = details;
  }
}

export function pageFileName(page) {
  return `${String(page).padStart(3, '0')}.png`;
}

function stable(value) {
  if (Array.isArray(value)) return value.map(stable);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, stable(value[key])]));
  }
  return value;
}

export function computeSlideInputHash(deck, slide) {
  const shared = {
    renderMode: deck.renderMode,
    aspectRatio: deck.aspectRatio,
    resolution: deck.resolution,
    referenceImage: deck.referenceImage,
    referenceImageSha256: deck.referenceImageSha256,
    globalStyle: deck.globalStyle,
    visualTheme: deck.visualTheme,
  };
  const { inputHash, outputFile, ...slideInput } = slide;
  return createHash('sha256').update(JSON.stringify(stable({ shared, slide: slideInput }))).digest('hex');
}

function isPresentString(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

function verifyPageSequence(slides) {
  const seen = new Set();
  for (const slide of slides) {
    const page = slide?.page;
    if (seen.has(page)) {
      throw new ManifestError('DUPLICATE_PAGE', `Page ${page} appears more than once.`, { page });
    }
    seen.add(page);
  }

  for (let index = 0; index < slides.length; index += 1) {
    const expectedPage = index + 1;
    if (slides[index]?.page !== expectedPage) {
      throw new ManifestError(
        'NON_CONSECUTIVE_PAGE',
        `Expected page ${expectedPage} at position ${expectedPage}.`,
        { expectedPage, actualPage: slides[index]?.page },
      );
    }
  }
}

function contained(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === '' || (!path.isAbsolute(relative) && relative !== '..' && !relative.startsWith(`..${path.sep}`));
}

function localFilePath(source, manifestDir) {
  if (typeof source !== 'string' || source.length === 0 || source.startsWith('data:')) return undefined;
  if (source.startsWith('file:')) {
    const url = new URL(source);
    if (url.hostname) throw new ManifestError('ASSET_OUTSIDE_PROJECT', 'Remote file URLs are not authorized.', { source });
    return fileURLToPath(url);
  }
  if (/^[a-z][a-z\d+.-]*:/iu.test(source) || source.startsWith('//')) {
    throw new ManifestError('ASSET_OUTSIDE_PROJECT', 'Only project-local files and data URLs are authorized.', { source });
  }
  return path.isAbsolute(source) ? path.normalize(source) : path.resolve(manifestDir, source);
}

function authorizeAsset(source, manifestDir, projectRoot, label) {
  const filePath = localFilePath(source, manifestDir);
  if (!filePath) return { source };
  if (!projectRoot) return { source: filePath };
  const lexicalRoot = path.resolve(projectRoot);
  const authorizedRoot = realpathSync(projectRoot);
  if (!contained(lexicalRoot, filePath)) {
    throw new ManifestError('ASSET_OUTSIDE_PROJECT', `${label} escapes the authorized project root.`, { label, path: filePath });
  }
  let physicalPath;
  try {
    physicalPath = realpathSync(filePath);
    if (!contained(authorizedRoot, physicalPath)) {
      throw new ManifestError('ASSET_OUTSIDE_PROJECT', `${label} resolves outside the authorized project root.`, { label, path: filePath });
    }
    accessSync(physicalPath, constants.R_OK);
    if (!statSync(physicalPath).isFile()) throw new Error('Not a regular file');
  } catch (error) {
    if (error instanceof ManifestError) throw error;
    throw new ManifestError('ASSET_NOT_READABLE', `${label} must be an existing readable file.`, { label, path: filePath, cause: error.message });
  }
  return {
    source: filePath,
    sha256: createHash('sha256').update(readFileSync(physicalPath)).digest('hex'),
  };
}

function resolveLayerSources(slides, manifestDir, projectRoot) {
  for (const slide of slides) {
    if (!Array.isArray(slide?.layers)) continue;
    for (const layer of slide.layers) {
      if (layer && typeof layer === 'object' && 'src' in layer) {
        const asset = authorizeAsset(layer.src, manifestDir, projectRoot, `layer ${layer.id ?? 'unknown'} source`);
        layer.src = asset.source;
        if (asset.sha256) layer.sourceSha256 = asset.sha256;
        else delete layer.sourceSha256;
      }
    }
  }
}

export function normalizeManifest(raw, manifestDir, options = {}) {
  const manifest = structuredClone(raw ?? {});
  manifest.deck ??= {};
  manifest.slides ??= [];

  manifest.deck.aspectRatio ??= DEFAULT_ASPECT_RATIO;
  manifest.deck.resolution ??= structuredClone(DEFAULT_RESOLUTION);
  const referenceImage = authorizeAsset(
    manifest.deck.referenceImage,
    manifestDir,
    options.projectRoot,
    'deck reference image',
  );
  manifest.deck.referenceImage = referenceImage.source;
  if (referenceImage.sha256) manifest.deck.referenceImageSha256 = referenceImage.sha256;
  else delete manifest.deck.referenceImageSha256;

  if (!Array.isArray(manifest.slides)) {
    manifest.slides = [];
  }
  verifyPageSequence(manifest.slides);
  resolveLayerSources(manifest.slides, manifestDir, options.projectRoot);

  for (const slide of manifest.slides) {
    slide.outputFile = pageFileName(slide.page);
    slide.inputHash = computeSlideInputHash(manifest.deck, slide);
  }

  return manifest;
}

function missingSlideField(slide) {
  for (const field of REQUIRED_SLIDE_FIELDS) {
    const value = slide?.[field];
    if (value === undefined || value === null || value === '') return field;
  }
  if (!Array.isArray(slide.content)) return 'content';
  if (!Array.isArray(slide.elements)) return 'elements';
  return undefined;
}

function validLayerBounds(layer, resolution) {
  const { x, y, width, height } = layer ?? {};
  return [x, y, width, height].every(Number.isFinite)
    && x >= 0
    && y >= 0
    && width > 0
    && height > 0
    && Number.isFinite(resolution?.width)
    && Number.isFinite(resolution?.height)
    && x + width <= resolution.width
    && y + height <= resolution.height;
}

function validateCanonicalText(slide) {
  const expected = new Map([
    ['title', slide.title],
    ...slide.content.map((content, index) => [`content[${index}]`, content]),
  ]);
  const counts = new Map([...expected.keys()].map((source) => [source, 0]));

  for (const layer of slide.layers) {
    if (layer?.kind !== 'text') continue;
    if (!expected.has(layer.source)) {
      throw new ManifestError(
        'INVALID_CANONICAL_TEXT_SOURCE',
        `Text layer ${layer.id ?? 'unknown'} on page ${slide.page} has an invalid canonical source.`,
        { page: slide.page, layerId: layer.id, source: layer.source },
      );
    }
    counts.set(layer.source, counts.get(layer.source) + 1);
    if (layer.text !== expected.get(layer.source)) {
      throw new ManifestError(
        'CANONICAL_TEXT_MISMATCH',
        `Text layer ${layer.id ?? 'unknown'} on page ${slide.page} differs from ${layer.source}.`,
        { page: slide.page, layerId: layer.id, source: layer.source },
      );
    }
  }

  for (const [source, count] of counts) {
    if (count === 0) {
      throw new ManifestError(
        'CANONICAL_TEXT_SOURCE_MISSING',
        `Page ${slide.page} does not render ${source}.`,
        { page: slide.page, source },
      );
    }
    if (count > 1) {
      throw new ManifestError(
        'CANONICAL_TEXT_SOURCE_DUPLICATED',
        `Page ${slide.page} renders ${source} more than once.`,
        { page: slide.page, source, count },
      );
    }
  }
}

function validateGeneratedLayer(layer, page, renderMode = 'deterministic-text') {
  const review = layer.visualReview;
  const requiredChecks = renderMode === 'commercial-whole-slide'
    ? WHOLE_SLIDE_REVIEW_CHECKS
    : REQUIRED_REVIEW_CHECKS;
  const hasRequiredChecks = Array.isArray(review?.checkedFor)
    && requiredChecks.every((check) => review.checkedFor.includes(check));
  if (review?.status !== 'pass' || !hasRequiredChecks) {
    throw new ManifestError(
      'GENERATED_ASSET_NOT_REVIEWED',
      `Generated asset ${layer.id ?? 'unknown'} on page ${page} lacks a passing visual review.`,
      { page, layerId: layer.id },
    );
  }

  if (!Number.isInteger(review.repairRounds)
    || review.repairRounds < 0
    || review.repairRounds > 2
    || !Number.isInteger(review.generationAttempts)
    || review.generationAttempts !== review.repairRounds + 1) {
    throw new ManifestError(
      'GENERATED_ASSET_RETRY_LIMIT',
      `Generated asset ${layer.id ?? 'unknown'} on page ${page} has invalid retry metadata.`,
      { page, layerId: layer.id },
    );
  }
}

function validateCommercialReview(layer, page) {
  const review = layer.visualReview;
  const ocr = review?.ocr;
  if (ocr?.titleExact !== true || ocr?.essentialTextExact !== true
    || !Number.isFinite(ocr?.bodyMatchRatio) || ocr.bodyMatchRatio < 0.98) {
    throw new ManifestError(
      'WHOLE_SLIDE_OCR_FAILED',
      `Commercial whole-slide page ${page} does not meet the text-fidelity threshold.`,
      { page, layerId: layer.id, ocr },
    );
  }

  const scores = review?.commercialScores;
  const values = COMMERCIAL_SCORE_FIELDS.map((field) => scores?.[field]);
  const average = values.reduce((sum, value) => sum + value, 0) / values.length;
  if (values.some((value) => !Number.isFinite(value) || value < 75) || average < 85) {
    throw new ManifestError(
      'COMMERCIAL_SCORE_FAILED',
      `Commercial whole-slide page ${page} does not meet the saleable-quality threshold.`,
      { page, layerId: layer.id, scores, average },
    );
  }

  if (!Number.isInteger(review?.candidateCount) || review.candidateCount < 1) {
    throw new ManifestError('MISSING_CANDIDATE_REVIEW', `Page ${page} lacks candidate-selection metadata.`, { page, layerId: layer.id });
  }
  if (!Number.isFinite(review?.dominantPanelAreaRatio)
    || review.dominantPanelAreaRatio < 0 || review.dominantPanelAreaRatio > 1) {
    throw new ManifestError('INVALID_PANEL_RATIO', `Page ${page} lacks a valid dominant-panel ratio.`, { page, layerId: layer.id });
  }
  if (review.dominantPanelAreaRatio > 0.45 && !isPresentString(review.largePanelJustification)) {
    throw new ManifestError('UNJUSTIFIED_LARGE_PANEL', `Page ${page} uses a large panel without a content-based justification.`, { page, layerId: layer.id });
  }
}

function validateWholeSlide(deck, slide) {
  if (!isPresentString(slide.layoutArchetype)) {
    throw new ManifestError('MISSING_LAYOUT_ARCHETYPE', `Page ${slide.page} lacks a layout archetype.`, { page: slide.page });
  }
  if (slide.layers.length !== 1) {
    throw new ManifestError('INVALID_WHOLE_SLIDE_LAYER_COUNT', `Page ${slide.page} must contain exactly one whole-slide layer.`, { page: slide.page });
  }
  const layer = slide.layers[0];
  if (layer.kind !== 'image' || layer.id !== 'whole-slide' || layer.generated !== true
    || layer.x !== 0 || layer.y !== 0
    || layer.width !== deck.resolution.width || layer.height !== deck.resolution.height) {
    throw new ManifestError('INVALID_WHOLE_SLIDE_LAYER', `Page ${slide.page} must use one reviewed full-resolution generated image layer named whole-slide.`, { page: slide.page, layer });
  }
  validateGeneratedLayer(layer, slide.page, deck.renderMode);
  validateCommercialReview(layer, slide.page);
}

function validateWholeSlideDeck(deck, slides) {
  if (!isPresentString(deck.styleBible)) {
    throw new ManifestError('MISSING_STYLE_BIBLE', 'Commercial whole-slide decks require a written deck style bible.', {});
  }
  if (!Array.isArray(deck.anchorPages) || deck.anchorPages.length !== 3
    || new Set(deck.anchorPages).size !== 3
    || deck.anchorPages.some((page) => !Number.isInteger(page) || page < 1 || page > slides.length)) {
    throw new ManifestError('INVALID_ANCHOR_PAGES', 'Commercial whole-slide decks require exactly three distinct valid anchor pages.', { anchorPages: deck.anchorPages });
  }
  for (const page of deck.anchorPages) {
    const candidateCount = slides[page - 1].layers[0].visualReview.candidateCount;
    if (candidateCount < 3) {
      throw new ManifestError('INSUFFICIENT_ANCHOR_CANDIDATES', `Anchor page ${page} requires at least three generated candidates.`, { page, candidateCount });
    }
  }
  const archetypes = slides.map((slide) => slide.layoutArchetype);
  for (let index = 2; index < archetypes.length; index += 1) {
    if (archetypes[index] === archetypes[index - 1] && archetypes[index] === archetypes[index - 2]) {
      throw new ManifestError('REPEATED_LAYOUT_ARCHETYPE', `Layout archetype ${archetypes[index]} repeats on more than two consecutive pages.`, { page: index + 1, layoutArchetype: archetypes[index] });
    }
  }
  if (slides.length >= 20) {
    const counts = new Map();
    for (const archetype of archetypes) counts.set(archetype, (counts.get(archetype) ?? 0) + 1);
    if (counts.size < 6) {
      throw new ManifestError('INSUFFICIENT_LAYOUT_DIVERSITY', 'A 20+ page commercial deck requires at least six dominant layout archetypes.', { uniqueArchetypes: counts.size });
    }
    const maximum = Math.floor(slides.length * 0.25);
    for (const [archetype, count] of counts) {
      if (count > maximum) throw new ManifestError('LAYOUT_ARCHETYPE_OVERUSED', `Layout archetype ${archetype} exceeds 25% of the deck.`, { layoutArchetype: archetype, count, maximum });
    }
  }
  const largePanels = slides.map((slide) => slide.layers[0].visualReview.dominantPanelAreaRatio > 0.45);
  for (let index = 2; index < largePanels.length; index += 1) {
    if (largePanels[index] && largePanels[index - 1] && largePanels[index - 2]) {
      throw new ManifestError('LARGE_PANEL_RUN', 'Large text panels may not appear on more than two consecutive commercial slides.', { page: index + 1 });
    }
  }
}

function validateCoursewarePlanning(deck, slides) {
  const courseware = deck?.visualTheme?.courseware;
  if (!courseware || typeof courseware !== 'object') {
    throw new ManifestError('MISSING_COURSEWARE_THEME', 'Educational image decks require deck.visualTheme.courseware planning metadata.');
  }
  for (const field of REQUIRED_COURSEWARE_THEME_FIELDS) {
    if (!isPresentString(courseware[field])) {
      throw new ManifestError('MISSING_COURSEWARE_THEME_FIELD', `Courseware theme field ${field} is required.`, { field });
    }
  }
  if (!Array.isArray(courseware.recurringMotifs)
    || courseware.recurringMotifs.length < 2
    || courseware.recurringMotifs.length > 4
    || courseware.recurringMotifs.some((motif) => !isPresentString(motif))) {
    throw new ManifestError('INVALID_RECURRING_MOTIFS', 'Courseware themes require two to four nonempty recurring motifs.');
  }
  if (!Array.isArray(courseware.densitySequence) || courseware.densitySequence.length !== slides.length
    || courseware.densitySequence.some((density) => !COURSEWARE_DENSITIES.has(density))) {
    throw new ManifestError('INVALID_DENSITY_SEQUENCE', 'Courseware densitySequence must contain one valid density for every slide.', {
      expectedLength: slides.length,
      actualLength: courseware.densitySequence?.length,
    });
  }
  for (const [index, slide] of slides.entries()) {
    const design = slide?.coursewareDesign;
    if (!design || typeof design !== 'object') {
      throw new ManifestError('MISSING_COURSEWARE_DESIGN', `Page ${slide?.page ?? index + 1} lacks coursewareDesign.`, { page: slide?.page ?? index + 1 });
    }
    for (const field of REQUIRED_COURSEWARE_DESIGN_FIELDS) {
      if (!isPresentString(design[field])) {
        throw new ManifestError('MISSING_COURSEWARE_DESIGN_FIELD', `Page ${slide.page} coursewareDesign field ${field} is required.`, { page: slide.page, field });
      }
    }
    if (!COURSEWARE_DENSITIES.has(design.density) || design.density !== courseware.densitySequence[index]) {
      throw new ManifestError('COURSEWARE_DENSITY_MISMATCH', `Page ${slide.page} density must match deck.visualTheme.courseware.densitySequence.`, {
        page: slide.page,
        slideDensity: design.density,
        deckDensity: courseware.densitySequence[index],
      });
    }
  }
}

export function validateRenderManifest(manifest) {
  const deck = manifest?.deck;
  const slides = manifest?.slides;

  if (!isPresentString(deck?.title)) {
    throw new ManifestError('MISSING_DECK_TITLE', 'Deck title is required.');
  }
  if (!isPresentString(deck?.referenceImage)) {
    throw new ManifestError('MISSING_REFERENCE_IMAGE', 'Deck reference image is required.');
  }
  if (!Array.isArray(slides) || slides.length === 0) {
    throw new ManifestError('EMPTY_SLIDES', 'At least one slide is required.');
  }

  verifyPageSequence(slides);

  if (!['deterministic-text', 'commercial-whole-slide'].includes(deck.renderMode)) {
    throw new ManifestError('INVALID_RENDER_MODE', `Unsupported render mode: ${deck.renderMode}.`, { renderMode: deck.renderMode });
  }

  validateCoursewarePlanning(deck, slides);

  for (const slide of slides) {
    const missingField = missingSlideField(slide);
    if (missingField) {
      throw new ManifestError(
        'MISSING_SLIDE_CONTRACT',
        `Page ${slide?.page ?? 'unknown'} is missing ${missingField}.`,
        { page: slide?.page, field: missingField },
      );
    }
    if (!Array.isArray(slide.layers) || slide.layers.length === 0) {
      throw new ManifestError('MISSING_RENDER_LAYERS', `Page ${slide.page} has no render layers.`, { page: slide.page });
    }
    if (deck.renderMode === 'commercial-whole-slide') validateWholeSlide(deck, slide);
    else validateCanonicalText(slide);

    for (const layer of slide.layers) {
      if (!validLayerBounds(layer, deck.resolution)) {
        throw new ManifestError(
          'INVALID_LAYER_BOUNDS',
          `Layer ${layer?.id ?? 'unknown'} on page ${slide.page} is outside deck bounds.`,
          { page: slide.page, layerId: layer?.id },
        );
      }
      if (layer.kind === 'image' && layer.generated === true) {
        if (deck.renderMode !== 'commercial-whole-slide') validateGeneratedLayer(layer, slide.page, deck.renderMode);
      }
    }
  }
  if (deck.renderMode === 'commercial-whole-slide') validateWholeSlideDeck(deck, slides);
}
