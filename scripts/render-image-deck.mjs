#!/usr/bin/env node

import { createHash, randomUUID } from 'node:crypto';
import { mkdir, readFile, readdir, realpath, rename, rm, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { normalizeManifest, validateRenderManifest } from './image-deck/manifest.mjs';
import { packagePptx } from './image-deck/pptx.mjs';
import { renderSlide } from './image-deck/render.mjs';
import { resolveRuntime } from './image-deck/runtime.mjs';
import { createContactSheet, verifyDeck } from './image-deck/verify.mjs';

const FLAGS = new Map([
  ['--project-root', 'projectRoot'],
  ['--manifest', 'manifest'],
  ['--output-dir', 'outputDir'],
  ['--modules-root', 'modulesRoot'],
  ['--browser-executable', 'browserExecutable'],
  ['--internal-dir', 'internalDir'],
]);
const REQUIRED = ['projectRoot', 'manifest', 'outputDir'];

class CliError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.code = code;
    this.details = details;
  }
}

function progress(message) {
  process.stderr.write(`${message}\n`);
}

function emit(report) {
  process.stdout.write(`${JSON.stringify(report)}\n`);
}

function asError(error, fallbackCode) {
  return {
    code: error?.code || fallbackCode,
    message: error?.message || String(error),
    ...(error?.details && typeof error.details === 'object' ? error.details : {}),
  };
}

function parseArguments(argv) {
  const args = { resume: false };
  const seen = new Set();
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    if (flag === '--resume') {
      if (seen.has(flag)) throw new CliError('DUPLICATE_ARGUMENT', `${flag} may only be supplied once.`, { flag });
      args.resume = true;
      seen.add(flag);
      continue;
    }
    const key = FLAGS.get(flag);
    if (!key) throw new CliError('UNKNOWN_ARGUMENT', `Unknown argument: ${flag}`, { flag });
    if (seen.has(flag)) throw new CliError('DUPLICATE_ARGUMENT', `${flag} may only be supplied once.`, { flag });
    const value = argv[index + 1];
    if (!value || value.startsWith('--')) throw new CliError('MISSING_ARGUMENT_VALUE', `${flag} requires a value.`, { flag });
    args[key] = value;
    seen.add(flag);
    index += 1;
  }
  const missing = REQUIRED.filter((key) => !args[key]);
  if (missing.length) throw new CliError('MISSING_REQUIRED_ARGUMENT', `Missing required arguments: ${missing.join(', ')}`, { missing });
  return args;
}

function contained(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === '' || (!path.isAbsolute(relative) && relative !== '..' && !relative.startsWith(`..${path.sep}`));
}

async function physicalPath(candidate) {
  let probe = candidate;
  const suffix = [];
  while (true) {
    try {
      return path.join(await realpath(probe), ...suffix);
    } catch (error) {
      if (error?.code !== 'ENOENT') throw error;
      const parent = path.dirname(probe);
      if (parent === probe) throw error;
      suffix.unshift(path.basename(probe));
      probe = parent;
    }
  }
}

async function resolveInside(projectRoot, input, label) {
  const candidate = path.resolve(projectRoot, input);
  if (!contained(projectRoot, candidate)) throw new CliError('PATH_OUTSIDE_PROJECT', `${label} escapes the authorized project root.`, { label, path: candidate });
  if (!contained(projectRoot, await physicalPath(candidate))) {
    throw new CliError('PATH_OUTSIDE_PROJECT', `${label} resolves outside the authorized project root.`, { label, path: candidate });
  }
  return candidate;
}

async function resolvePaths(args) {
  let projectRoot;
  try {
    projectRoot = await realpath(path.resolve(args.projectRoot));
    if (!(await stat(projectRoot)).isDirectory()) throw new Error('Not a directory');
  } catch (error) {
    throw new CliError('INVALID_PROJECT_ROOT', 'The project root must be an existing directory.', { cause: error.message });
  }
  const manifestPath = await resolveInside(projectRoot, args.manifest, 'manifest');
  const outputDir = await resolveInside(projectRoot, args.outputDir, 'output directory');
  const internalDir = await resolveInside(projectRoot, args.internalDir ?? 'image-deck/.internal', 'internal directory');
  const [physicalOutputDir, physicalInternalDir] = await Promise.all([
    physicalPath(outputDir),
    physicalPath(internalDir),
  ]);
  if (contained(outputDir, internalDir) || contained(physicalOutputDir, physicalInternalDir)) {
    throw new CliError('INTERNAL_DIRECTORY_IN_OUTPUT', 'The internal directory must be outside the delivery output directory.', {
      outputDir,
      internalDir,
    });
  }
  return {
    projectRoot,
    manifestPath,
    outputDir,
    pagesDir: path.join(outputDir, 'pages'),
    internalDir,
    reportPath: path.join(internalDir, 'generation-report.json'),
    contactSheetPath: path.join(internalDir, 'contact-sheet.jpg'),
  };
}

async function readManifest(filePath) {
  progress(`Reading manifest: ${filePath}`);
  let source;
  try {
    source = await readFile(filePath, 'utf8');
  } catch (error) {
    throw new CliError('MANIFEST_READ_FAILED', 'The render manifest could not be read.', { cause: error.message });
  }
  try {
    return JSON.parse(source);
  } catch (error) {
    throw new CliError('INVALID_MANIFEST_JSON', 'The render manifest is not valid JSON.', { cause: error.message });
  }
}

async function hashFile(filePath) {
  return createHash('sha256').update(await readFile(filePath)).digest('hex');
}

function deckPptxPath(outputDir, title) {
  const safeTitle = [...String(title || 'image-deck').normalize('NFKC')]
    .slice(0, 96).join('').replace(/[\\/:*?"<>|\u0000-\u001f\u007f]/gu, '_').trim() || 'image-deck';
  return path.join(outputDir, `${safeTitle}_图片版.pptx`);
}

async function readPriorReport(filePath, resume) {
  if (!resume) return undefined;
  try {
    const report = JSON.parse(await readFile(filePath, 'utf8'));
    progress(`Loaded resume report: ${filePath}`);
    return report;
  } catch (error) {
    progress(error?.code === 'ENOENT' ? 'No prior report found; starting a full render.' : 'Prior report is unusable; starting a full render.');
    return undefined;
  }
}

async function reusableResult(slide, outputPath, priorReport, dimensions) {
  const priorPage = priorReport?.pages?.find((page) => page?.page === slide.page);
  if (priorPage?.status !== 'pass' || priorPage.file !== slide.outputFile || priorPage.inputHash !== slide.inputHash || !priorPage.outputHash) return undefined;
  try {
    if ((await hashFile(outputPath)) !== priorPage.outputHash) return undefined;
  } catch {
    return undefined;
  }
  return { status: 'pass', attempts: 0, page: slide.page, outputPath, inputHash: slide.inputHash, dimensions, textChecks: [], errors: [], reused: true };
}

async function renderPages(manifest, outputDir, runtime, priorReport) {
  const dimensions = { ...manifest.deck.resolution };
  const results = [];
  for (const slide of manifest.slides) {
    const outputPath = path.join(outputDir, slide.outputFile);
    const reuse = await reusableResult(slide, outputPath, priorReport, dimensions);
    if (reuse) {
      progress(`Reusing page ${slide.page}: ${slide.outputFile}`);
      results.push(reuse);
      continue;
    }
    progress(`Rendering page ${slide.page}: ${slide.outputFile}`);
    try {
      results.push({ ...(await renderSlide({ deck: manifest.deck, slide, outputPath, runtime })), reused: false });
    } catch (error) {
      results.push({ status: 'fail', attempts: 0, page: slide.page, outputPath, inputHash: slide.inputHash, dimensions, textChecks: [], errors: [asError(error, 'PAGE_RENDER_FAILED')], reused: false });
    }
  }
  return results;
}

function detailedPages(verifiedPages, renderResults) {
  return verifiedPages.map((page) => {
    const renderResult = renderResults.find((result) => result.page === page.page);
    return { ...page, reused: renderResult?.reused === true, attempts: renderResult?.attempts ?? 0, textChecks: renderResult?.textChecks ?? [], renderErrors: renderResult?.errors ?? [] };
  });
}

async function outputSetErrors(manifest, outputDir, pagesDir) {
  const actual = (await readdir(pagesDir)).filter((file) => file.toLowerCase().endsWith('.png')).sort();
  const rootPngs = (await readdir(outputDir)).filter((file) => file.toLowerCase().endsWith('.png')).sort();
  const expected = manifest.slides.map((slide) => slide.outputFile);
  return rootPngs.length === 0 && actual.length === expected.length && actual.every((file, index) => file === expected[index])
    ? []
    : [{ code: 'OUTPUT_PAGE_SET_MISMATCH', message: 'Output PNG count, location, or numeric order does not match the current manifest.', expected, actual, rootPngs }];
}

function pathFields(paths) {
  return { manifestPath: paths.manifestPath, outputDir: paths.outputDir, pagesDir: paths.pagesDir, internalDir: paths.internalDir };
}

function failedReport(error, options = {}) {
  const normalized = asError(error, options.fallbackCode || 'UNKNOWN_ERROR');
  return {
    status: 'fail', pageCount: options.pageCount ?? 0, pages: options.pages ?? [],
    contactSheet: options.contactSheet ?? { path: options.contactSheetPath ?? '', status: 'skipped' },
    pptx: options.pptx ?? { path: options.pptxPath ?? '', pageCount: 0, status: 'skipped' },
    failedPage: options.failedPage ?? null, fatalCode: normalized.code,
    errors: options.errors ?? [normalized], ...(options.paths ?? {}),
  };
}

async function writeReport(filePath, report) {
  await mkdir(path.dirname(filePath), { recursive: true });
  const temporary = path.join(path.dirname(filePath), `.${path.basename(filePath)}.${randomUUID()}.tmp`);
  try {
    await writeFile(temporary, `${JSON.stringify(report, null, 2)}\n`);
    await rename(temporary, filePath);
  } finally {
    await rm(temporary, { force: true });
  }
}

async function finalizeFailure(report, reportPath, exitCode, message) {
  try {
    await writeReport(reportPath, report);
  } catch (error) {
    report.reportWriteError = asError(error, 'REPORT_WRITE_FAILED');
    progress(`REPORT_WRITE_FAILED: ${report.reportWriteError.message}`);
  }
  progress(message);
  emit(report);
  return exitCode;
}

async function priorPassingPptx(priorReport, pptxPath) {
  if (!['pass', 'preserved'].includes(priorReport?.pptx?.status) || priorReport.pptx.path !== pptxPath) return undefined;
  try {
    if (!(await stat(pptxPath)).isFile()) return undefined;
    return { path: pptxPath, pageCount: priorReport.pptx.pageCount, status: 'preserved' };
  } catch {
    return undefined;
  }
}

async function run() {
  let args;
  let paths;
  let manifest;
  let runtime;
  try {
    args = parseArguments(process.argv.slice(2));
    paths = await resolvePaths(args);
    manifest = normalizeManifest(await readManifest(paths.manifestPath), path.dirname(paths.manifestPath), { projectRoot: paths.projectRoot });
    validateRenderManifest(manifest);
    runtime = resolveRuntime({ modulesRoot: args.modulesRoot, browserExecutable: args.browserExecutable });
    try {
      await mkdir(paths.outputDir, { recursive: true });
      await mkdir(paths.pagesDir, { recursive: true });
    } catch (error) {
      throw new CliError('OUTPUT_DIRECTORY_UNAVAILABLE', 'The output directory could not be prepared.', { cause: error.message });
    }
    try {
      await mkdir(paths.internalDir, { recursive: true });
    } catch (error) {
      throw new CliError('INTERNAL_DIRECTORY_UNAVAILABLE', 'The internal report directory could not be prepared.', { cause: error.message });
    }
  } catch (error) {
    const report = failedReport(error, { paths: paths ? pathFields(paths) : {} });
    progress(`${report.fatalCode}: ${report.errors[0].message}`);
    emit(report);
    return 2;
  }

  const pptxPath = deckPptxPath(paths.outputDir, manifest.deck.title);
  const priorReport = await readPriorReport(paths.reportPath, args.resume);
  let renderResults;
  let verification;
  try {
    renderResults = await renderPages(manifest, paths.pagesDir, runtime, priorReport);
    progress('Verifying all page PNGs.');
    verification = await verifyDeck({ manifest, renderResults, pagesDir: paths.pagesDir, runtime });
    const extras = await outputSetErrors(manifest, paths.outputDir, paths.pagesDir);
    if (extras.length) verification = { ...verification, status: 'fail', errors: [...verification.errors, ...extras] };
  } catch (error) {
    const report = failedReport(error, { fallbackCode: 'PAGE_VERIFICATION_FAILED', pageCount: manifest.slides.length, pptxPath, contactSheetPath: paths.contactSheetPath, paths: pathFields(paths) });
    return finalizeFailure(report, paths.reportPath, 3, `${report.fatalCode}: ${report.errors[0].message}`);
  }

  const pages = detailedPages(verification.pages, renderResults);
  if (verification.status !== 'pass') {
    const failedRender = renderResults.find((result) => result.status !== 'pass');
    const error = failedRender?.errors?.[0] ?? verification.errors[0] ?? { code: 'PAGE_VERIFICATION_FAILED', message: 'Page verification failed.' };
    const report = failedReport(error, {
      pageCount: manifest.slides.length, pages, failedPage: failedRender?.page ?? error.page ?? null,
      errors: [...renderResults.flatMap((result) => result.status === 'pass' ? [] : result.errors), ...verification.errors],
      pptx: (await priorPassingPptx(priorReport, pptxPath)) ?? { path: pptxPath, pageCount: 0, status: 'skipped' },
      contactSheetPath: paths.contactSheetPath, paths: pathFields(paths),
    });
    return finalizeFailure(report, paths.reportPath, 3, `${report.fatalCode}: page ${report.failedPage ?? 'unknown'} failed; PPTX packaging skipped.`);
  }

  const pagePaths = manifest.slides.map((slide) => path.join(paths.pagesDir, slide.outputFile));
  let contactSheet = { path: paths.contactSheetPath, status: 'pending' };
  try {
    progress(`Creating contact sheet: ${paths.contactSheetPath}`);
    await createContactSheet({ pagePaths, outputPath: paths.contactSheetPath, runtime });
    contactSheet = { path: paths.contactSheetPath, status: 'pass' };
    progress(`Packaging and verifying PPTX: ${pptxPath}`);
    const pptx = await packagePptx({ manifest, pagePaths, outputPath: pptxPath, runtime });
    const report = { ...verification, status: 'pass', pages, contactSheet, pptx, failedPage: null, fatalCode: null, errors: [], ...pathFields(paths) };
    await writeReport(paths.reportPath, report);
    progress(`Image deck passed: ${manifest.slides.length} pages.`);
    emit(report);
    return 0;
  } catch (error) {
    const report = failedReport(error, {
      fallbackCode: 'PACKAGING_FAILED', pageCount: manifest.slides.length, pages,
      pptx: { path: pptxPath, pageCount: 0, status: 'fail' },
      contactSheet: contactSheet.status === 'pass' ? contactSheet : { path: paths.contactSheetPath, status: 'fail' },
      paths: pathFields(paths),
    });
    return finalizeFailure(report, paths.reportPath, 4, `${report.fatalCode}: ${report.errors[0].message}`);
  }
}

process.exitCode = await run();
