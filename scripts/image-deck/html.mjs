import { readFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { validateGeneratedLayer } from './manifest.mjs';

const RASTER_EXTENSION = /\.(?:png|jpe?g|webp|avif|gif)$/iu;
const COLOR = /^(?:transparent|currentColor|#[\da-f]{3,8}|(?:rgb|hsl)a?\([\d.%\s,/-]+\))$/iu;
const FONT_FAMILY = /^[\p{L}\p{N} ,_-]+$/u;
const FONT_WEIGHT = /^(?:normal|bold|[1-9]00)$/iu;
const TEXT_ALIGN = new Set(['left', 'center', 'right', 'justify', 'start', 'end']);
const OBJECT_FIT = new Set(['fill', 'contain', 'cover', 'none', 'scale-down']);
const SVG_ELEMENTS = new Set([
  'svg', 'g', 'defs', 'symbol', 'use', 'path', 'rect', 'circle', 'ellipse', 'line',
  'polyline', 'polygon', 'text', 'tspan', 'image', 'lineargradient', 'radialgradient',
  'stop', 'clippath', 'mask', 'pattern', 'title', 'desc',
]);
const SVG_ATTRIBUTES = new Set([
  'xmlns', 'xmlns:xlink', 'version', 'id', 'class', 'viewbox', 'width', 'height',
  'x', 'y', 'x1', 'y1', 'x2', 'y2', 'cx', 'cy', 'r', 'rx', 'ry', 'd', 'points',
  'fill', 'fill-opacity', 'fill-rule', 'stroke', 'stroke-width', 'stroke-linecap',
  'stroke-linejoin', 'stroke-miterlimit', 'stroke-dasharray', 'stroke-dashoffset',
  'stroke-opacity', 'transform', 'opacity', 'display', 'visibility',
  'preserveaspectratio', 'gradientunits', 'gradienttransform', 'offset', 'stop-color',
  'stop-opacity', 'clip-path', 'clip-rule', 'mask', 'maskunits', 'maskcontentunits',
  'patternunits', 'patterncontentunits', 'text-anchor', 'font-family', 'font-size',
  'font-weight', 'letter-spacing', 'dominant-baseline', 'alignment-baseline',
  'vector-effect', 'href', 'xlink:href', 'role', 'aria-label', 'aria-hidden', 'focusable',
]);

export function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function number(value, name) {
  if (!Number.isFinite(value)) throw new Error(`INVALID_LAYER_${name.toUpperCase()}: ${name} must be finite.`);
  return value;
}

function cssColor(value, fallback) {
  const text = String(value ?? fallback);
  if (!COLOR.test(text)) throw new Error('UNSAFE_STYLE_VALUE: Unsupported CSS color value.');
  return text;
}

function cssFontFamily(value, fallback) {
  const text = String(value ?? fallback);
  if (!FONT_FAMILY.test(text)) throw new Error('UNSAFE_STYLE_VALUE: Unsupported font family value.');
  return text;
}

function cssFontWeight(value, fallback) {
  const text = String(value ?? fallback);
  if (!FONT_WEIGHT.test(text)) throw new Error('UNSAFE_STYLE_VALUE: Unsupported font weight value.');
  return text;
}

function cssTextAlign(value, fallback) {
  const text = String(value ?? fallback).toLowerCase();
  if (!TEXT_ALIGN.has(text)) throw new Error('UNSAFE_STYLE_VALUE: Unsupported text alignment value.');
  return text;
}

function cssObjectFit(value, fallback) {
  const text = String(value ?? fallback).toLowerCase();
  if (!OBJECT_FIT.has(text)) throw new Error('UNSAFE_STYLE_VALUE: Unsupported object-fit value.');
  return text;
}

function bounds(layer) {
  return `position:absolute;left:${number(layer.x, 'x')}px;top:${number(layer.y, 'y')}px;width:${number(layer.width, 'width')}px;height:${number(layer.height, 'height')}px`;
}

function layerAttributes(layer) {
  const allowed = Array.isArray(layer.allowOverlapWith) ? layer.allowOverlapWith : [];
  return `data-layer="${escapeHtml(layer.id)}" data-layer-kind="${escapeHtml(layer.kind)}" data-allow-overlap-with="${escapeHtml(JSON.stringify(allowed))}"`;
}

function assertReviewedRaster(deck, slide, layer) {
  if (layer.generated !== true) return;
  validateGeneratedLayer(layer, slide.page, deck.renderMode);
  const source = String(layer.src ?? '');
  const pathname = source.startsWith('file:') ? new URL(source).pathname : source;
  const isRaster = /^data:image\/(?:png|jpe?g|webp|avif|gif)(?:;|,)/iu.test(source) || RASTER_EXTENSION.test(pathname);
  if (!isRaster) throw new Error('GENERATED_ASSET_NOT_RASTER: Generated visuals must use raster image assets.');
}

function localAssetUrl(source) {
  if (typeof source !== 'string' || source.length === 0) throw new Error('INVALID_LOCAL_ASSET: Asset source is required.');
  if (source.startsWith('data:')) return source;
  if (source.startsWith('file:')) {
    const url = new URL(source);
    if (url.hostname) throw new Error('EXTERNAL_ASSET_URL: Only local file URLs are allowed.');
    return url.href;
  }
  if (/^[a-z][a-z\d+.-]*:/iu.test(source) || source.startsWith('//')) {
    throw new Error('EXTERNAL_ASSET_URL: Only local file URLs are allowed.');
  }
  return pathToFileURL(source).href;
}

function embeddedImageUrl(source) {
  const url = localAssetUrl(source);
  if (url.startsWith('data:')) return url;
  const filePath = fileURLToPath(url);
  const extension = /\.([a-z\d]+)$/iu.exec(filePath)?.[1]?.toLowerCase();
  const mime = {
    png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg',
    webp: 'image/webp', avif: 'image/avif', gif: 'image/gif', svg: 'image/svg+xml',
  }[extension] ?? 'application/octet-stream';
  // normalizeManifest authorizes project-local paths before HTML construction.
  // Embedding avoids Chromium's about:blank -> file: origin restriction.
  return `data:${mime};base64,${readFileSync(filePath).toString('base64')}`;
}

function readSvg(layer) {
  if (typeof layer.svg === 'string') return layer.svg;
  const source = localAssetUrl(layer.src);
  if (source.startsWith('data:')) {
    const comma = source.indexOf(',');
    if (comma === -1) throw new Error('INVALID_SVG: Malformed data URL.');
    const metadata = source.slice(0, comma);
    const content = source.slice(comma + 1);
    return metadata.endsWith(';base64') ? Buffer.from(content, 'base64').toString('utf8') : decodeURIComponent(content);
  }
  return readFileSync(fileURLToPath(source), 'utf8');
}

function svgAttributes(tag) {
  const attributes = [];
  let index = 0;
  while (/\s/u.test(tag[index] ?? '')) index += 1;
  while (index < tag.length && !/[\s/>]/u.test(tag[index])) index += 1;

  while (index < tag.length) {
    while (index < tag.length && /[\s/]/u.test(tag[index])) index += 1;
    if (index >= tag.length) break;
    const nameStart = index;
    while (index < tag.length && !/[\s=/>]/u.test(tag[index])) index += 1;
    const name = tag.slice(nameStart, index).toLowerCase();
    while (/\s/u.test(tag[index] ?? '')) index += 1;
    let value;
    if (tag[index] === '=') {
      index += 1;
      while (/\s/u.test(tag[index] ?? '')) index += 1;
      const quote = tag[index];
      if (quote === '"' || quote === "'") {
        index += 1;
        const valueStart = index;
        while (index < tag.length && tag[index] !== quote) index += 1;
        value = tag.slice(valueStart, index);
        if (tag[index] === quote) index += 1;
      } else {
        const valueStart = index;
        while (index < tag.length && !/[\s/>]/u.test(tag[index])) index += 1;
        value = tag.slice(valueStart, index);
      }
    }
    if (name) attributes.push({ name, value });
  }
  return attributes;
}

function parseSvgTags(source) {
  const tags = [];
  let searchFrom = 0;
  while (true) {
    const start = source.indexOf('<', searchFrom);
    if (start === -1) return tags;
    if (source.startsWith('<!--', start)) {
      return [{ type: 'invalid' }];
    }
    if (source.startsWith('<![CDATA[', start)) {
      return [{ type: 'invalid' }];
    }
    const first = source[start + 1];
    if (!first || first === '!' || first === '?') return [{ type: 'invalid' }];

    let end = start + 1;
    let quote;
    while (end < source.length) {
      const character = source[end];
      if (quote) {
        if (character === quote) quote = undefined;
      } else if (character === '"' || character === "'") {
        quote = character;
      } else if (character === '>') {
        break;
      }
      end += 1;
    }
    if (end === source.length) return [{ type: 'invalid' }];

    const raw = source.slice(start + 1, end);
    const trimmed = raw.trim();
    const closing = trimmed.startsWith('/');
    const body = (closing ? trimmed.slice(1) : trimmed).trimStart();
    const name = /^([a-z][\w:.-]*)(?=[\s/>]|$)/iu.exec(body)?.[1]?.toLowerCase();
    if (!name) return [{ type: 'invalid' }];
    tags.push({
      type: 'tag',
      start,
      end: end + 1,
      raw,
      name,
      closing,
      selfClosing: !closing && /\/\s*$/u.test(trimmed),
    });
    searchFrom = end + 1;
  }
}

function hasSafeSvgStructure(source) {
  const tags = parseSvgTags(source);
  const root = tags[0];
  if (!root || root.type !== 'tag' || root.closing || root.name !== 'svg' || source.slice(0, root.start).trim()) {
    return false;
  }

  const stack = [];
  let rootEnd;
  for (const tag of tags) {
    if (tag.type === 'invalid') return false;
    if (rootEnd || !SVG_ELEMENTS.has(tag.name)) return false;
    if (tag.closing) {
      if (tag.raw.trim().slice(1).trim() !== tag.name || stack.at(-1) !== tag.name) return false;
      stack.pop();
      if (stack.length === 0) rootEnd = tag.end;
      continue;
    }
    for (const { name, value } of svgAttributes(tag.raw)) {
      if (!SVG_ATTRIBUTES.has(name) || /^on[a-z][\w:.-]*$/iu.test(name)) return false;
      if (name === 'href' || name === 'xlink:href') {
        const reference = value?.trim().toLowerCase();
        if (!reference || (!reference.startsWith('#') && !reference.startsWith('data:'))) return false;
      }
    }
    if (tag.selfClosing) {
      if (stack.length === 0) rootEnd = tag.end;
    } else {
      stack.push(tag.name);
    }
  }
  return stack.length === 0 && rootEnd !== undefined && source.slice(rootEnd).trim() === '';
}

function trustedSvg(source) {
  const contentWithoutNamespaces = source.replace(/\s+xmlns(?::[a-z\d_-]+)?\s*=\s*["']https?:\/\/www\.w3\.org\/[^"']+["']/giu, '');
  const unsafe = /<\s*script\b|<\s*foreignObject\b|https?:\/\/|url\s*\(\s*["']?\s*(?!#|data:)/iu;
  if (!/<svg\b/iu.test(source)) throw new Error('INVALID_SVG: SVG root is required.');
  if (unsafe.test(contentWithoutNamespaces) || !hasSafeSvgStructure(source)) {
    throw new Error('UNSAFE_SVG: SVG contains scripts, handlers, or external content.');
  }
  return source;
}

function textHtml(deck, layer) {
  const style = layer.style ?? {};
  const fontSize = number(style.fontSize, 'fontSize');
  const minFontSize = number(style.minFontSize ?? fontSize, 'minFontSize');
  const lineHeight = number(style.lineHeight ?? 1.2, 'lineHeight');
  return `<div ${layerAttributes(layer)} data-text-layer="${escapeHtml(layer.id)}" data-min-font-size="${minFontSize}" data-source-font-size="${fontSize}" data-source-line-height="${lineHeight}" style="${bounds(layer)};overflow:hidden;white-space:pre-wrap;overflow-wrap:normal;word-break:normal;font-family:${cssFontFamily(style.fontFamily ?? deck.visualTheme?.fontFamily, 'sans-serif')};font-size:${fontSize}px;font-weight:${cssFontWeight(style.fontWeight, 400)};color:${cssColor(style.color ?? deck.visualTheme?.body, '#000')};line-height:${lineHeight};text-align:${cssTextAlign(style.align, 'left')}">${escapeHtml(layer.text ?? '')}</div>`;
}

function imageHtml(deck, slide, layer) {
  assertReviewedRaster(deck, slide, layer);
  const style = layer.style ?? {};
  return `<img ${layerAttributes(layer)} src="${escapeHtml(embeddedImageUrl(layer.src))}" alt="" style="${bounds(layer)};display:block;object-fit:${cssObjectFit(style.objectFit ?? layer.objectFit, deck.renderMode === 'commercial-whole-slide' ? 'contain' : 'cover')};border-radius:${number(style.radius ?? 0, 'radius')}px">`;
}

function shapeHtml(layer) {
  const style = layer.style ?? {};
  const shape = layer.shape === 'roundRect' ? 'rect' : layer.shape;
  if (!['rect', 'circle', 'line'].includes(shape)) throw new Error(`UNSUPPORTED_SHAPE: ${layer.shape}`);
  if (shape === 'line') {
    return `<div ${layerAttributes(layer)} style="${bounds(layer)};height:0;border-top:${number(style.strokeWidth ?? 1, 'strokeWidth')}px solid ${cssColor(style.stroke ?? style.fill, '#000')};transform:rotate(${number(style.rotation ?? 0, 'rotation')}deg);transform-origin:left center"></div>`;
  }
  const radius = shape === 'circle' ? '50%' : `${number(style.radius ?? 0, 'radius')}px`;
  return `<div ${layerAttributes(layer)} style="${bounds(layer)};background:${cssColor(style.fill, 'transparent')};border:${number(style.strokeWidth ?? 0, 'strokeWidth')}px solid ${cssColor(style.stroke, 'transparent')};border-radius:${radius}"></div>`;
}

export function buildLayerHtml(deck, slide, layer) {
  if (layer.generated === true && layer.kind !== 'image') {
    throw new Error('GENERATED_ASSET_NOT_RASTER: Generated visuals must use raster image assets.');
  }
  if (layer.kind === 'text') return textHtml(deck, layer);
  if (layer.kind === 'image') return imageHtml(deck, slide, layer);
  if (layer.kind === 'shape') return shapeHtml(layer);
  if (layer.kind === 'svg') return `<div ${layerAttributes(layer)} style="${bounds(layer)};overflow:hidden">${trustedSvg(readSvg(layer))}</div>`;
  throw new Error(`UNSUPPORTED_LAYER_KIND: ${layer.kind}`);
}

export function buildSlideHtml(deck, slide) {
  const width = number(deck?.resolution?.width, 'width');
  const height = number(deck?.resolution?.height, 'height');
  const layers = (slide.layers ?? []).map((layer) => buildLayerHtml(deck, slide, layer)).join('');
  return `<!doctype html><html><head><meta charset="utf-8"><style>*{box-sizing:border-box}html,body{margin:0;width:${width}px;height:${height}px;overflow:hidden}#page{position:relative;width:${width}px;height:${height}px;overflow:hidden;background:${cssColor(deck.visualTheme?.background, '#fff')}}</style></head><body><main id="page" data-page="${escapeHtml(slide.page)}">${layers}</main></body></html>`;
}
