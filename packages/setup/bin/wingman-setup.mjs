#!/usr/bin/env node

import { cpSync, existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, renameSync, rmSync } from 'node:fs';
import { homedir } from 'node:os';
import { basename, dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const skillName = 'wingman-first-setup';
const source = resolve(dirname(fileURLToPath(import.meta.url)), '..', 'skill', skillName);
const version = JSON.parse(readFileSync(resolve(dirname(fileURLToPath(import.meta.url)), '..', 'package.json'), 'utf8')).version;

function usage() {
  return `Wingman first setup installer v${version}

Usage: npx @wingmanbefree/setup [--target all|codex|claude|goose|opencode] [--skills-dir PATH] [--force] [--dry-run]

Options:
  --target       Agent to install for (default: all four)
  --skills-dir   Custom parent directory for one installation; overrides --target
  --force        Replace an existing copy after making a backup
  --dry-run      Show the destination without changing files
  --help         Show this help
  --version      Show the package version
`;
}

function fail(message) {
  console.error(`wingman-setup: ${message}`);
  process.exitCode = 1;
}

function expandHome(path) {
  return path === '~' ? homedir() : path.startsWith('~/') ? join(homedir(), path.slice(2)) : path;
}

function parseArgs(args) {
  const options = { target: 'all', skillsDir: null, force: false, dryRun: false };
  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--help' || arg === '-h') return { action: 'help' };
    if (arg === '--version' || arg === '-v') return { action: 'version' };
    if (arg === '--force') options.force = true;
    else if (arg === '--dry-run') options.dryRun = true;
    else if (arg === '--target' || arg === '--skills-dir') {
      const value = args[++i];
      if (!value || value.startsWith('--')) throw new Error(`${arg} requires a value`);
      if (arg === '--target') options.target = value;
      else options.skillsDir = value;
    } else throw new Error(`unknown option ${arg}`);
  }
  if (!['all', 'codex', 'claude', 'goose', 'opencode'].includes(options.target)) {
    throw new Error('target must be all, codex, claude, goose, or opencode');
  }
  return options;
}

function destinationsFor(options) {
  if (options.skillsDir) return [join(resolve(expandHome(options.skillsDir)), skillName)];
  const parents = {
    codex: join(homedir(), '.codex', 'skills'),
    claude: join(homedir(), '.claude', 'skills'),
    goose: join(homedir(), '.config', 'goose', 'skills'),
    opencode: join(homedir(), '.config', 'opencode', 'skills'),
  };
  const targets = options.target === 'all' ? Object.keys(parents) : [options.target];
  return targets.map((target) => join(parents[target], skillName));
}

function filesUnder(root, prefix = '') {
  return readdirSync(root, { withFileTypes: true }).flatMap((entry) => {
    const relative = join(prefix, entry.name);
    return entry.isDirectory() ? filesUnder(join(root, entry.name), relative) : [relative];
  }).sort();
}

function sameSkill(destination) {
  if (!existsSync(destination)) return false;
  const files = filesUnder(source);
  const installedFiles = filesUnder(destination);
  return files.length === installedFiles.length && files.every((file, index) => {
    if (file !== installedFiles[index]) return false;
    const installed = join(destination, file);
    return existsSync(installed) && readFileSync(installed).equals(readFileSync(join(source, file)));
  });
}

function installOne(destination, options) {
  if (existsSync(destination) && sameSkill(destination)) {
    console.log(`${skillName} is already installed at ${destination}`);
    return;
  }
  mkdirSync(dirname(destination), { recursive: true });
  const staging = mkdtempSync(join(dirname(destination), `.${skillName}-`));
  const stagedSkill = join(staging, skillName);
  let backup = null;
  try {
    cpSync(source, stagedSkill, { recursive: true });
    if (existsSync(destination)) {
      backup = join(dirname(destination), `${basename(destination)}.backup-${Date.now()}-${process.pid}`);
      renameSync(destination, backup);
    }
    try {
      renameSync(stagedSkill, destination);
    } catch (error) {
      if (backup) renameSync(backup, destination);
      throw error;
    }
  } finally {
    rmSync(staging, { recursive: true, force: true });
  }

  console.log(`Installed ${skillName} to ${destination}`);
  if (backup) console.log(`Previous copy backed up to ${backup}`);
}

function install(options) {
  const destinations = destinationsFor(options);
  if (options.dryRun) {
    for (const destination of destinations) console.log(`Would install ${skillName} to ${destination}`);
    return;
  }
  const conflicts = destinations.filter((destination) => existsSync(destination) && !sameSkill(destination));
  if (conflicts.length && !options.force) {
    throw new Error(`${conflicts.join(', ')} already exists. Use --force to back up and replace changed copies.`);
  }
  for (const destination of destinations) installOne(destination, options);
  console.log('Next: ask your agent, "Use wingman-first-setup to set up my Wingman."');
  console.log('The agent will interview you and record the setup choices before provisioning.');
}

try {
  const options = parseArgs(process.argv.slice(2));
  if (options.action === 'help') console.log(usage());
  else if (options.action === 'version') console.log(version);
  else install(options);
} catch (error) {
  fail(error.message);
}
