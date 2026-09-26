import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { buildSlideHtml } from './html.mjs';
import { launchBrowser, resolveRuntime } from './runtime.mjs';

const MAX_REPAIR_ROUNDS = 2;

async function measureText(page, sourceTextById) {
  const measurements = await page.locator('[data-text-layer]').evaluateAll((elements) => elements.map((element) => {
    const computed = getComputedStyle(element);
    const fontSize = Number.parseFloat(computed.fontSize);
    return {
      id: element.dataset.textLayer,
      actualText: element.textContent,
      clientWidth: element.clientWidth,
      clientHeight: element.clientHeight,
      scrollWidth: element.scrollWidth,
      scrollHeight: element.scrollHeight,
      fontSize,
      lineHeight: Number.parseFloat(computed.lineHeight) / fontSize,
      minFontSize: Number.parseFloat(element.dataset.minFontSize),
    };
  }));
  return measurements.map((check) => ({
    ...check,
    exactText: check.actualText === sourceTextById.get(check.id),
    overflow: check.scrollWidth > check.clientWidth || check.scrollHeight > check.clientHeight,
  }));
}

async function measureAssets(page) {
  return page.locator('img[data-layer]').evaluateAll(async (elements) => Promise.all(elements.map(async (element) => {
    try {
      await element.decode();
      return {
        id: element.dataset.layer,
        decoded: element.complete && element.naturalWidth > 0 && element.naturalHeight > 0,
        naturalWidth: element.naturalWidth,
        naturalHeight: element.naturalHeight,
      };
    } catch (error) {
      return { id: element.dataset.layer, decoded: false, naturalWidth: 0, naturalHeight: 0, cause: error.message };
    }
  })));
}

async function measureLayout(page) {
  return page.locator('[data-layer]').evaluateAll((elements) => {
    const layers = elements.map((element, index) => {
      let allowed = [];
      try { allowed = JSON.parse(element.dataset.allowOverlapWith ?? '[]'); } catch { allowed = []; }
      const rect = element.getBoundingClientRect();
      return {
        id: element.dataset.layer,
        kind: element.dataset.layerKind,
        index,
        allowed,
        rect: { left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom },
      };
    });
    const collisions = [];
    const obscuredText = [];
    for (let firstIndex = 0; firstIndex < layers.length; firstIndex += 1) {
      for (let secondIndex = firstIndex + 1; secondIndex < layers.length; secondIndex += 1) {
        const first = layers[firstIndex];
        const second = layers[secondIndex];
        const intersects = Math.min(first.rect.right, second.rect.right) > Math.max(first.rect.left, second.rect.left)
          && Math.min(first.rect.bottom, second.rect.bottom) > Math.max(first.rect.top, second.rect.top);
        if (!intersects) continue;
        const overlapAuthorized = first.allowed.includes(second.id) || second.allowed.includes(first.id);
        if (!overlapAuthorized) collisions.push([first.id, second.id]);
        if (first.kind === 'text' && second.kind !== 'text') obscuredText.push(first.id);
      }
    }
    return { collisions, obscuredText: [...new Set(obscuredText)] };
  });
}

async function repairOverflow(page, round) {
  return page.locator('[data-text-layer]').evaluateAll((elements, currentRound) => {
    let changed = false;
    for (const element of elements) {
      if (element.scrollWidth <= element.clientWidth && element.scrollHeight <= element.clientHeight) continue;
      const computed = getComputedStyle(element);
      const fontSize = Number.parseFloat(computed.fontSize);
      const lineHeight = Number.parseFloat(computed.lineHeight) / fontSize;
      const minFontSize = Number.parseFloat(element.dataset.minFontSize);
      const remainingRounds = 3 - currentRound;
      const nextFontSize = currentRound === 2
        ? minFontSize
        : Math.max(minFontSize, fontSize - ((fontSize - minFontSize) / remainingRounds));
      const nextLineHeight = Math.max(1, lineHeight - 0.1);
      if (nextFontSize < fontSize) {
        element.style.fontSize = `${nextFontSize}px`;
        changed = true;
      }
      if (nextLineHeight < lineHeight) {
        element.style.lineHeight = String(nextLineHeight);
        changed = true;
      }
    }
    return changed;
  }, round);
}

function errorsFor(textChecks, assetChecks, layoutChecks) {
  const errors = [];
  const mismatched = textChecks.filter((check) => !check.exactText);
  if (mismatched.length > 0) errors.push({ code: 'TEXT_MISMATCH', message: 'Rendered text differs from its source text.', layerIds: mismatched.map((check) => check.id) });
  const overflowing = textChecks.filter((check) => check.overflow);
  if (overflowing.length > 0) errors.push({ code: 'TEXT_OVERFLOW', message: 'Text remains outside deterministic layer bounds.', layerIds: overflowing.map((check) => check.id) });
  const failedAssets = assetChecks.filter((check) => !check.decoded);
  if (failedAssets.length > 0) errors.push({ code: 'ASSET_DECODE_FAILED', message: 'One or more raster images could not be decoded.', layerIds: failedAssets.map((check) => check.id) });
  if (layoutChecks.collisions.length > 0) errors.push({ code: 'LAYER_COLLISION', message: 'Layers overlap without explicit authorization.', pairs: layoutChecks.collisions });
  if (layoutChecks.obscuredText.length > 0) errors.push({ code: 'TEXT_OBSCURED', message: 'A later layer obscures protected text.', layerIds: layoutChecks.obscuredText });
  return errors;
}

function canonicalText(slide, source) {
  if (source === 'title') return slide.title;
  const match = /^content\[(\d+)\]$/u.exec(source ?? '');
  return match ? slide.content?.[Number(match[1])] : undefined;
}

export async function renderSlide(options) {
  const { deck, slide, outputPath } = options;
  const dimensions = { width: deck.resolution.width, height: deck.resolution.height };
  const html = buildSlideHtml(deck, slide);
  const runtime = options.runtime ?? resolveRuntime(options);
  const browser = await launchBrowser(runtime);
  let context;
  try {
    context = await browser.newContext({ viewport: dimensions, deviceScaleFactor: 1 });
    await context.route('**/*', async (route) => {
      const url = route.request().url();
      if (url.startsWith('file:') || url.startsWith('data:')) return route.continue();
      return route.abort('blockedbyclient');
    });
    const page = await context.newPage();
    await page.setContent(html, { waitUntil: 'load' });
    await page.evaluate(async () => { await document.fonts.ready; });

    const sourceTextById = new Map(slide.layers
      .filter((layer) => layer.kind === 'text')
      .map((layer) => [String(layer.id), canonicalText(slide, layer.source)]));
    let attempts = 0;
    let textChecks = await measureText(page, sourceTextById);
    while (attempts < MAX_REPAIR_ROUNDS && textChecks.some((check) => check.overflow)) {
      const changed = await repairOverflow(page, attempts + 1);
      if (!changed) break;
      attempts += 1;
      textChecks = await measureText(page, sourceTextById);
    }
    const [assetChecks, layoutChecks] = await Promise.all([measureAssets(page), measureLayout(page)]);
    const errors = errorsFor(textChecks, assetChecks, layoutChecks);
    const result = {
      status: errors.length === 0 ? 'pass' : 'fail',
      attempts,
      page: slide.page,
      outputPath,
      inputHash: slide.inputHash,
      dimensions,
      textChecks,
      assetChecks,
      layoutChecks,
      errors,
    };
    if (result.status === 'pass') {
      await mkdir(path.dirname(outputPath), { recursive: true });
      await page.locator('#page').screenshot({ path: outputPath, type: 'png' });
    }
    return result;
  } finally {
    await context?.close();
    await browser.close();
  }
}
