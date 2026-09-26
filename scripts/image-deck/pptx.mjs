import { createHash, randomUUID } from 'node:crypto';
import { execFile } from 'node:child_process';
import { mkdir, readFile, rename, rm } from 'node:fs/promises';
import path from 'node:path';
import { promisify } from 'node:util';
import { pageFileName } from './manifest.mjs';
import { resolveRuntime } from './runtime.mjs';

const execFileAsync = promisify(execFile);

export class PptxPackagingError extends Error {
  constructor(code, message, details = {}) {
    super(`${code}: ${message}`);
    this.name = 'PptxPackagingError';
    this.code = code;
    this.details = details;
  }
}

function orderedPageFiles(pagePaths) {
  if (!Array.isArray(pagePaths) || pagePaths.length === 0) {
    throw new PptxPackagingError('EMPTY_OUTPUT_PAGES', 'At least one page PNG is required.');
  }
  return pagePaths.map((pagePath, index) => {
    const file = path.basename(pagePath);
    const expected = pageFileName(index + 1);
    if (file !== expected) {
      throw new PptxPackagingError(
        'NON_CONSECUTIVE_OUTPUT_PAGE',
        `Expected ${expected} at position ${index + 1}, received ${file}.`,
        { expected, actual: file, position: index + 1 },
      );
    }
    return file;
  });
}

async function zipEntries(filePath) {
  const { stdout } = await execFileAsync('unzip', ['-Z1', filePath]);
  return stdout.trim().split('\n').filter(Boolean);
}

async function unzipText(filePath, entry) {
  const { stdout } = await execFileAsync('unzip', ['-p', filePath, entry]);
  return stdout;
}

async function unzipBuffer(filePath, entry) {
  const { stdout } = await execFileAsync('unzip', ['-p', filePath, entry], { encoding: 'buffer', maxBuffer: 128 * 1024 * 1024 });
  return stdout;
}

function sha256(data) {
  return createHash('sha256').update(data).digest('hex');
}

function geometryFromManifest(manifest) {
  const resolution = manifest?.deck?.resolution ?? { width: 3840, height: 2160 };
  const aspectRatio = manifest?.deck?.aspectRatio ?? '16:9';
  const match = /^(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)$/u.exec(aspectRatio);
  if (!match || !Number.isFinite(resolution.width) || !Number.isFinite(resolution.height)
    || resolution.width <= 0 || resolution.height <= 0) {
    throw new PptxPackagingError('INVALID_DECK_GEOMETRY', 'Manifest aspect ratio and resolution must be positive numeric geometry.');
  }
  const declaredRatio = Number(match[1]) / Number(match[2]);
  const resolutionRatio = resolution.width / resolution.height;
  if (Math.abs(declaredRatio - resolutionRatio) > 1e-9) {
    throw new PptxPackagingError('INVALID_DECK_GEOMETRY', 'Manifest aspect ratio does not match its resolution.', { aspectRatio, resolution });
  }
  const heightInches = 7.5;
  const widthInches = heightInches * resolutionRatio;
  return {
    aspectRatio,
    resolution: { ...resolution },
    widthInches,
    heightInches,
    widthEmu: Math.round(widthInches * 914400),
    heightEmu: Math.round(heightInches * 914400),
  };
}

function xmlAttribute(attributes, name) {
  return new RegExp(`(?:^|\\s)${name}="([^"]*)"`).exec(attributes)?.[1];
}

function relationshipsById(relationshipsXml) {
  const relationships = new Map();
  for (const match of relationshipsXml.matchAll(/<Relationship\b([^>]*)\/?>(?:<\/Relationship>)?/g)) {
    const attributes = match[1];
    const id = xmlAttribute(attributes, 'Id');
    if (id) {
      relationships.set(id, {
        type: xmlAttribute(attributes, 'Type'),
        target: xmlAttribute(attributes, 'Target'),
        targetMode: xmlAttribute(attributes, 'TargetMode'),
      });
    }
  }
  return relationships;
}

async function verifyPackagedPptx(filePath, pagePaths, geometry) {
  const expectedPageCount = pagePaths.length;
  const entries = await zipEntries(filePath);
  const slideEntries = entries.filter((entry) => /^ppt\/slides\/slide\d+\.xml$/.test(entry));
  const mediaEntries = entries.filter((entry) => /^ppt\/media\/[^/]+\.png$/.test(entry));
  if (slideEntries.length !== expectedPageCount || mediaEntries.length !== expectedPageCount) {
    throw new PptxPackagingError('PPTX_PAGE_MEDIA_MISMATCH', 'Packaged PPTX slide or media count does not match page count.', {
      expectedPageCount,
      slideCount: slideEntries.length,
      mediaCount: mediaEntries.length,
    });
  }
  const presentationXml = await unzipText(filePath, 'ppt/presentation.xml');
  const slideSize = /<p:sldSz\b[^>]*\bcx="(\d+)"[^>]*\bcy="(\d+)"/u.exec(presentationXml);
  if (!slideSize || Number(slideSize[1]) !== geometry.widthEmu || Number(slideSize[2]) !== geometry.heightEmu) {
    throw new PptxPackagingError('PPTX_GEOMETRY_MISMATCH', 'Packaged PPTX slide dimensions do not match the manifest.', {
      expected: { width: geometry.widthEmu, height: geometry.heightEmu },
      actual: slideSize ? { width: Number(slideSize[1]), height: Number(slideSize[2]) } : undefined,
    });
  }
  const embeddedMediaEntries = new Set();

  for (let page = 1; page <= expectedPageCount; page += 1) {
    const slideEntry = `ppt/slides/slide${page}.xml`;
    const relationshipsEntry = `ppt/slides/_rels/slide${page}.xml.rels`;
    const [slideXml, relationshipsXml] = await Promise.all([
      unzipText(filePath, slideEntry),
      unzipText(filePath, relationshipsEntry),
    ]);
    const embeddedRelationshipIds = [...slideXml.matchAll(/\br:embed="([^"]+)"/g)].map((match) => match[1]);
    const pictureCount = (slideXml.match(/<p:pic>/g) ?? []).length;
    const imageRelationshipCount = (relationshipsXml.match(/relationships\/image/g) ?? []).length;
    if (pictureCount !== 1 || embeddedRelationshipIds.length !== 1 || imageRelationshipCount !== 1) {
      throw new PptxPackagingError('PPTX_IMAGE_ONLY_CONTRACT_FAILED', `Slide ${page} must contain exactly one image relationship.`, {
        page,
        pictureCount,
        embeddedRelationshipCount: embeddedRelationshipIds.length,
        imageRelationshipCount,
      });
    }
    const pictureXml = /<p:pic>[\s\S]*?<\/p:pic>/u.exec(slideXml)?.[0] ?? '';
    const imageExtent = /<a:off x="0" y="0"\s*\/>\s*<a:ext cx="(\d+)" cy="(\d+)"\s*\/>/u.exec(pictureXml);
    const hasCrop = /<a:srcRect\b(?![^>]*\bl="0"[^>]*\bt="0"[^>]*\br="0"[^>]*\bb="0")[^>]*>/u.test(pictureXml);
    if (!imageExtent || Number(imageExtent[1]) !== geometry.widthEmu || Number(imageExtent[2]) !== geometry.heightEmu || hasCrop) {
      throw new PptxPackagingError('PPTX_GEOMETRY_MISMATCH', `Slide ${page} image does not fill the manifest canvas without cropping.`, {
        page,
        expected: { width: geometry.widthEmu, height: geometry.heightEmu },
      });
    }
    const relationship = relationshipsById(relationshipsXml).get(embeddedRelationshipIds[0]);
    const hasInternalTarget = relationship?.targetMode === undefined || relationship.targetMode === 'Internal';
    const mediaEntry = hasInternalTarget && relationship?.type?.endsWith('/image') && relationship.target
      ? path.posix.normalize(path.posix.join('ppt/slides', relationship.target))
      : undefined;
    if (!mediaEntry || !mediaEntries.includes(mediaEntry) || embeddedMediaEntries.has(mediaEntry)) {
      throw new PptxPackagingError('PPTX_IMAGE_RELATIONSHIP_INVALID', `Slide ${page} does not embed a distinct packaged PNG.`, {
        page,
        relationshipId: embeddedRelationshipIds[0],
        target: relationship?.target,
        targetMode: relationship?.targetMode,
        mediaEntry,
      });
    }
    embeddedMediaEntries.add(mediaEntry);
    const [sourceBytes, embeddedBytes] = await Promise.all([
      readFile(pagePaths[page - 1]),
      unzipBuffer(filePath, mediaEntry),
    ]);
    if (sha256(sourceBytes) !== sha256(embeddedBytes)) {
      throw new PptxPackagingError('PPTX_MEDIA_HASH_MISMATCH', `Slide ${page} does not embed the source PNG bytes for that page.`, {
        page,
        sourceFile: path.basename(pagePaths[page - 1]),
        mediaEntry,
      });
    }
  }
}

export async function packagePptx(options) {
  const { pagePaths, outputPath } = options;
  if (typeof outputPath !== 'string' || outputPath.length === 0) {
    throw new PptxPackagingError('MISSING_PPTX_OUTPUT_PATH', 'A final PPTX output path is required.');
  }
  const pageFiles = orderedPageFiles(pagePaths);
  const geometry = geometryFromManifest(options.manifest);
  const runtime = options.runtime ?? resolveRuntime(options);
  const outputDir = path.dirname(outputPath);
  const temporaryPath = path.join(outputDir, `.${path.basename(outputPath)}.${randomUUID()}.tmp.pptx`);
  const PptxGenJS = runtime.pptxgenjs;
  const pptx = new PptxGenJS();
  pptx.defineLayout?.({ name: 'IMAGE_DECK', width: geometry.widthInches, height: geometry.heightInches });
  pptx.layout = 'IMAGE_DECK';
  pptx.author = 'Codex';
  pptx.subject = 'Image-only education presentation';

  for (const pagePath of pagePaths) {
    const slide = pptx.addSlide();
    slide.background = { color: 'FFFFFF' };
    slide.addImage({ path: pagePath, x: 0, y: 0, w: geometry.widthInches, h: geometry.heightInches });
  }

  await mkdir(outputDir, { recursive: true });
  try {
    await pptx.writeFile({ fileName: temporaryPath });
    await verifyPackagedPptx(temporaryPath, pagePaths, geometry);
    await rename(temporaryPath, outputPath);
  } catch (error) {
    await rm(temporaryPath, { force: true });
    throw error;
  }

  return { path: outputPath, pageCount: pagePaths.length, pageFiles, geometry: { aspectRatio: geometry.aspectRatio, resolution: geometry.resolution }, status: 'pass' };
}
