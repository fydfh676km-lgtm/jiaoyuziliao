export const dataImage = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j8ioAAAAASUVORK5CYII=';
export const reviewChecks = {
  'deterministic-text': ['pseudo-text', 'watermark', 'logo', 'reference-copying', 'safe-text-region'],
  'commercial-whole-slide': ['watermark', 'logo', 'reference-copying', 'ocr-text', 'commercial-quality', 'style-continuity', 'page-specific-relevance'],
};

export function reviewedImage(renderMode, { src = dataImage, width = 3840, height = 2160 } = {}) {
  return {
    kind: 'image', id: 'whole-slide', generated: true, src,
    x: 0, y: 0, width, height,
    visualReview: {
      status: 'pass', checkedFor: [...reviewChecks[renderMode]],
      generationAttempts: 1, repairRounds: 0,
      ocr: { titleExact: true, essentialTextExact: true, bodyMatchRatio: 1 },
      commercialScores: {
        contentIntegration: 90, visualHierarchy: 90, pageSpecificity: 90,
        styleContinuity: 90, compositionQuality: 90, artifactCleanliness: 90,
      },
      candidateCount: 1, dominantPanelAreaRatio: 0.1,
    },
  };
}

export function commercialManifest(pageCount = 3, { src = dataImage, width = 3840, height = 2160 } = {}) {
  return {
    deck: {
      title: '商业整页检查', renderMode: 'commercial-whole-slide', referenceImage: src,
      resolution: { width, height }, aspectRatio: '16:9',
      styleBible: '统一纸张与水墨视觉',
      anchorPages: Array.from({ length: Math.min(3, pageCount) }, (_, index) => index + 1),
      visualTheme: { courseware: {
        topicFamily: 'literary-humanities', visualWorld: '水墨山水', material: '纸张',
        imageryLanguage: '原创情境图解', recurringMotifs: ['山形', '水纹'],
        densitySequence: Array(pageCount).fill('standard'),
      } },
    },
    slides: Array.from({ length: pageCount }, (_, index) => ({
      page: index + 1, title: `标题${index + 1}`, content: ['正文'], layout: '单轴构图',
      elements: [], elementStyle: '纸张水墨', emphasis: '关键文字', layoutArchetype: `构图${index + 1}`,
      coursewareDesign: {
        pageRole: '讲解', instructionalAction: '理解概念', focalPoint: '关键文字',
        composition: '单轴构图', textSafeZone: '稳定阅读区', readingPath: '从标题到正文',
        density: 'standard', continuityCue: '山形与水纹',
      },
      layers: [reviewedImage('commercial-whole-slide', { src, width, height })],
    })),
  };
}
