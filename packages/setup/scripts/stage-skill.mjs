import { cpSync, existsSync, mkdirSync, rmSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const packageDir = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const source = resolve(packageDir, '..', '..', 'wingman-first-setup');
const destination = resolve(packageDir, 'skill', 'wingman-first-setup');

if (!existsSync(resolve(source, 'SKILL.md'))) {
  throw new Error(`Canonical skill is missing: ${source}`);
}

rmSync(destination, { recursive: true, force: true });
mkdirSync(dirname(destination), { recursive: true });
cpSync(source, destination, { recursive: true });
