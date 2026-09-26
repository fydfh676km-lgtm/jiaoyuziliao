import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';
import os from 'node:os';
import path from 'node:path';

const DEFAULT_MODULES_ROOT = path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const MACOS_CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

export function resolveRuntime({ modulesRoot, browserExecutable } = {}) {
  const resolvedModulesRoot = modulesRoot
    ?? process.env.IMAGE_DECK_MODULES_ROOT
    ?? DEFAULT_MODULES_ROOT;
  const require = createRequire(path.join(resolvedModulesRoot, '_image_deck_loader.cjs'));
  const playwright = require('playwright');
  const sharp = require('sharp');
  const pptxgenjs = require('pptxgenjs');
  const managedBrowser = playwright.chromium.executablePath();
  const executablePath = [
    browserExecutable,
    process.env.IMAGE_DECK_BROWSER_EXECUTABLE,
    managedBrowser,
    process.platform === 'darwin' ? MACOS_CHROME : undefined,
  ].find((candidate) => typeof candidate === 'string' && candidate.length > 0 && existsSync(candidate));

  if (!executablePath) {
    throw new Error('BROWSER_EXECUTABLE_NOT_FOUND: No usable Chromium executable was found.');
  }

  return { playwright, sharp, pptxgenjs, browserExecutable: executablePath, modulesRoot: resolvedModulesRoot };
}

export async function launchBrowser(runtime) {
  return runtime.playwright.chromium.launch({ executablePath: runtime.browserExecutable, headless: true });
}
