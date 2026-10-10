import assert from 'node:assert/strict';
import test from 'node:test';
import { normalizeManifest, validateRenderManifest } from '../image-deck/manifest.mjs';

const dataImage = 'data:image/png;base64,AA==';

function coursewareTheme(densitySequence) {
  return {
    topicFamily: 'derived',
    visualWorld: '统一的教育视觉世界',
    material: '克制纸张质感',
    imageryLanguage: '内容相关的原创教育图解',
    recurringMotifs: ['路径线', '重点节点'],
    densitySequence,
  };
}

function coursewareDesign(density = 'standard') {
  return {
    pageRole: 'concept-or-method',
    instructionalAction: '理解并解释核心概念',
    focalPoint: '核心概念',
    composition: '单一主轴组织信息',
    textSafeZone: '左侧稳定阅读区',
    readingPath: '标题到正文再到图解',
    density,
    continuityCue: '延续路径线和重点节点',
  };
}

function deterministicSlide() {
  return {
    page: 1,
    title: '标题',
    content: ['正文'],
    layout: '布局',
    elements: [],
    elementStyle: '风格',
    emphasis: '重点',
    coursewareDesign: coursewareDesign(),
    layers: [
      { kind: 'text', id: 'title', source: 'title', text: '标题', x: 0, y: 0, width: 50, height: 10 },
      { kind: 'text', id: 'body', source: 'content[0]', text: '正文', x: 0, y: 10, width: 50, height: 10 },
    ],
  };
}

function assertManifestError(code, operation) {
  assert.throws(operation, (error) => error?.code === code);
}

test('requires an explicit render mode instead of silently selecting deterministic text', () => {
  const manifest = normalizeManifest({
    deck: {
      title: '测试',
      referenceImage: dataImage,
      resolution: { width: 100, height: 100 },
      visualTheme: { courseware: coursewareTheme(['standard']) },
    },
    slides: [deterministicSlide()],
  }, process.cwd());
  assertManifestError('INVALID_RENDER_MODE', () => validateRenderManifest(manifest));
});

test('requires educational visual-world and per-page planning records', () => {
  const slide = deterministicSlide();
  delete slide.coursewareDesign;
  assertManifestError('MISSING_COURSEWARE_THEME', () => validateRenderManifest({
    deck: {
      title: '测试', referenceImage: dataImage, renderMode: 'deterministic-text', resolution: { width: 100, height: 100 },
    },
    slides: [slide],
  }));
});

test('requires a per-page educational design record when the deck theme exists', () => {
  const slide = deterministicSlide();
  delete slide.coursewareDesign;
  assertManifestError('MISSING_COURSEWARE_DESIGN', () => validateRenderManifest({
    deck: {
      title: '测试', referenceImage: dataImage, renderMode: 'deterministic-text', resolution: { width: 100, height: 100 },
      visualTheme: { courseware: coursewareTheme(['standard']) },
    },
    slides: [slide],
  }));
});

test('requires per-page density to match the deck density sequence', () => {
  assertManifestError('COURSEWARE_DENSITY_MISMATCH', () => validateRenderManifest({
    deck: {
      title: '测试', referenceImage: dataImage, renderMode: 'deterministic-text', resolution: { width: 100, height: 100 },
      visualTheme: { courseware: coursewareTheme(['light']) },
    },
    slides: [deterministicSlide()],
  }));
});

test('rejects a layout archetype occupying more than 25 percent of a 21-page deck', () => {
  const requiredChecks = ['watermark', 'logo', 'reference-copying', 'ocr-text', 'commercial-quality', 'style-continuity', 'page-specific-relevance'];
  const scores = {
    contentIntegration: 90,
    visualHierarchy: 90,
    pageSpecificity: 90,
    styleContinuity: 90,
    compositionQuality: 90,
    artifactCleanliness: 90,
  };
  const archetypes = ['A', 'B', 'A', 'C', 'A', 'D', 'A', 'E', 'A', 'F', 'A', 'B', 'C', 'D', 'E', 'F', 'B', 'C', 'D', 'E', 'F'];
  const slides = archetypes.map((layoutArchetype, index) => ({
    page: index + 1,
    title: `标题${index + 1}`,
    content: [],
    layout: '布局',
    elements: [],
    elementStyle: '风格',
    emphasis: '重点',
    layoutArchetype,
    coursewareDesign: coursewareDesign('standard'),
    layers: [{
      kind: 'image',
      id: 'whole-slide',
      generated: true,
      src: dataImage,
      x: 0,
      y: 0,
      width: 100,
      height: 100,
      visualReview: {
        status: 'pass',
        checkedFor: requiredChecks,
        repairRounds: 0,
        generationAttempts: 1,
        ocr: { titleExact: true, essentialTextExact: true, bodyMatchRatio: 1 },
        commercialScores: scores,
        candidateCount: 1,
        dominantPanelAreaRatio: 0.1,
      },
    }],
  }));
  assertManifestError('LAYOUT_ARCHETYPE_OVERUSED', () => validateRenderManifest({
    deck: {
      title: '21页测试',
      referenceImage: dataImage,
      renderMode: 'commercial-whole-slide',
      resolution: { width: 100, height: 100 },
      styleBible: '统一风格',
      anchorPages: [1, 2, 3],
      visualTheme: { courseware: coursewareTheme(slides.map(() => 'standard')) },
    },
    slides,
  }));
});
