import { createHash } from 'node:crypto';
import { mkdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { pageFileName } from './manifest.mjs';
import { resolveRuntime } from './runtime.mjs';

function asError(code, message, details = {}) {
  return { code, message, ...details };
}

function reportForPage(renderResults, page) {
  return renderResults.find((result) => result?.page === page);
}

function resolvePagePath({ pageResult, pageFile, pagesDir }) {
  return pageResult?.outputPath ?? path.join(pagesDir, pageFile);
}

async function hashFile(filePath) {
  const data = await readFile(filePath);
  return createHash('sha256').update(data).digest('hex');
}

export async function verifyDeck(options) {
  const { manifest, renderResults = [] } = options;
  const runtime = options.runtime ?? resolveRuntime(options);
  const deck = manifest?.deck ?? {};
  const slides = manifest?.slides ?? [];
  const pagesDir = options.pagesDir ?? options.outputDir ?? process.cwd();
  const expectedResolution = { ...deck.resolution };
  const pages = [];
  const errors = [];

  for (const [index, slide] of slides.entries()) {
    const page = slide.page;
    const file = pageFileName(page);
    const renderResult = reportForPage(renderResults, page);
    const pagePath = resolvePagePath({ pageResult: renderResult, pageFile: file, pagesDir });
    const checks = {
      expectedFile: slide.outputFile === file && path.basename(pagePath) === file,
      renderPassed: renderResult?.status === 'pass',
      inputHashMatches: renderResult?.inputHash === slide.inputHash,
      exists: false,
      isPng: false,
      expectedResolution: false,
    };
    const pageErrors = [];
    let outputHash = '';

    if (page !== index + 1) {
      pageErrors.push(asError('NON_CONSECUTIVE_OUTPUT_PAGE', `Expected page ${index + 1}, received ${page}.`, { page }));
    }
    if (!checks.expectedFile) {
      pageErrors.push(asError('UNEXPECTED_OUTPUT_FILENAME', `Expected ${file}, received ${path.basename(pagePath)}.`, { page, file }));
    }
    if (!checks.renderPassed) {
      pageErrors.push(asError('RENDER_RESULT_NOT_PASSING', `Page ${page} lacks a passing render result.`, { page }));
    }
    if (!checks.inputHashMatches) {
      pageErrors.push(asError('INPUT_HASH_MISMATCH', `Page ${page} input hash does not match the current manifest.`, { page }));
    }

    try {
      const metadata = await runtime.sharp(pagePath).metadata();
      checks.exists = true;
      checks.isPng = metadata.format === 'png';
      checks.expectedResolution = metadata.width === expectedResolution.width
        && metadata.height === expectedResolution.height;
      if (!checks.isPng) {
        pageErrors.push(asError('OUTPUT_NOT_PNG', `Page ${page} is not a PNG.`, { page, file }));
      }
      if (!checks.expectedResolution) {
        pageErrors.push(asError('OUTPUT_RESOLUTION_MISMATCH', `Page ${page} does not match ${expectedResolution.width}×${expectedResolution.height}.`, { page, file }));
      }
      outputHash = await hashFile(pagePath);
    } catch (error) {
      pageErrors.push(asError('MISSING_OUTPUT_PAGE', `Page ${page} output could not be read.`, { page, file, cause: error.message }));
    }

    const status = pageErrors.length === 0 ? 'pass' : 'fail';
    pages.push({ page, file, inputHash: slide.inputHash, outputHash, status, checks });
    errors.push(...pageErrors);
  }

  return {
    status: errors.length === 0 ? 'pass' : 'fail',
    deckTitle: deck.title,
    pageCount: slides.length,
    expectedResolution,
    pages,
    pptx: { path: '', pageCount: 0, status: 'pending' },
    errors,
  };
}

function labelSvg(label) {
  const escaped = String(label).replace(/[&<>"']/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' })[character]);
  return Buffer.from(`<svg width="480" height="36" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#111827"/><text x="18" y="24" fill="#ffffff" font-family="Arial, sans-serif" font-size="20">${escaped}</text></svg>`);
}

export async function createContactSheet(options) {
  const { pagePaths, outputPath } = options;
  const runtime = options.runtime ?? resolveRuntime(options);
  const thumbnailWidth = 480;
  const thumbnailHeight = 270;
  const labelHeight = 36;
  const columns = 4;
  const rows = Math.ceil(pagePaths.length / columns);
  const composites = [];

  for (const [index, pagePath] of pagePaths.entries()) {
    const x = (index % columns) * thumbnailWidth;
    const y = Math.floor(index / columns) * (thumbnailHeight + labelHeight);
    const thumbnail = await runtime.sharp(pagePath)
      .resize(thumbnailWidth, thumbnailHeight, { fit: 'contain', background: '#FFFFFF' })
      .png()
      .toBuffer();
    composites.push({ input: thumbnail, left: x, top: y });
    composites.push({ input: labelSvg(path.basename(pagePath)), left: x, top: y + thumbnailHeight });
  }

  await mkdir(path.dirname(outputPath), { recursive: true });
  await runtime.sharp({
    create: {
      width: columns * thumbnailWidth,
      height: Math.max(1, rows) * (thumbnailHeight + labelHeight),
      channels: 3,
      background: '#FFFFFF',
    },
  }).composite(composites).jpeg({ quality: 90 }).toFile(outputPath);
  return outputPath;
}
