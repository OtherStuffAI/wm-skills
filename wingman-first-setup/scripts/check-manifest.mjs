#!/usr/bin/env node

import { readFileSync } from 'node:fs';

const path = process.argv[2];
const requireReady = process.argv.includes('--ready');
if (!path || path.startsWith('--')) {
  console.error('Usage: node check-manifest.mjs <manifest.json> [--ready]');
  process.exit(2);
}

let manifest;
try {
  manifest = JSON.parse(readFileSync(path, 'utf8'));
} catch (error) {
  console.error(`Cannot read setup manifest: ${error.message}`);
  process.exit(2);
}

const errors = [];
if (!manifest || typeof manifest !== 'object' || Array.isArray(manifest)) {
  console.error('Setup manifest must be a JSON object.');
  process.exit(1);
}
const oneOf = (value, allowed, field) => {
  if (value != null && !allowed.includes(value)) errors.push(`${field} must be ${allowed.join(' or ')}`);
};
const required = (value, field) => {
  if (typeof value !== 'string' || !value.trim()) errors.push(`${field} is required`);
};
const noSecrets = (value, trail = '') => {
  if (!value || typeof value !== 'object') return;
  for (const [key, child] of Object.entries(value)) {
    const field = trail ? `${trail}.${key}` : key;
    if (/(nsec|secret|private.?key|password|token|recovery)/i.test(key)) errors.push(`${field} must not be stored in the manifest`);
    noSecrets(child, field);
  }
};

noSecrets(manifest);
if (manifest.schema_version !== 1) errors.push('schema_version must be 1');
oneOf(manifest.status, ['interview', 'ready', 'in_progress', 'blocked', 'complete'], 'status');
oneOf(manifest.tower?.mode, ['other_stuff_hosted', 'self_hosted'], 'tower.mode');
oneOf(manifest.owner?.identity_plan, ['existing', 'wingman_app'], 'owner.identity_plan');
oneOf(manifest.host?.agent_mode, ['use_installed', 'isolated'], 'host.agent_mode');
oneOf(manifest.host?.runtime, ['bun', 'docker'], 'host.runtime');
oneOf(manifest.transport?.mode, ['local_http', 'public_https', 'fips_only', 'https_and_fips'], 'transport.mode');
if (manifest.host?.agent_mode === 'isolated' && manifest.host?.runtime && manifest.host.runtime !== 'docker') {
  errors.push('isolated agents require Docker');
}
if (manifest.owner?.npub != null && !/^npub1[023456789acdefghjklmnpqrstuvwxyz]{58}$/.test(manifest.owner.npub)) {
  errors.push('owner.npub must be a public Nostr npub');
}
if (manifest.tower?.url != null) {
  try {
    const url = new URL(manifest.tower.url);
    if (!['http:', 'https:'].includes(url.protocol)) errors.push('tower.url must be HTTP or HTTPS');
    if (manifest.tower?.mode === 'other_stuff_hosted' && url.origin !== 'https://tower-stable-api.b.otherstuff.ai') {
      errors.push('hosted Tower URL must use the Other Stuff Hosted Tower origin');
    }
  } catch {
    errors.push('tower.url must be a URL');
  }
}
if (requireReady) {
  if (!['ready', 'in_progress'].includes(manifest.status)) errors.push('status must be ready or in_progress');
  required(manifest.tower?.mode, 'tower.mode');
  required(manifest.tower?.url, 'tower.url');
  required(manifest.tower?.workspace_name, 'tower.workspace_name');
  required(manifest.owner?.npub, 'owner.npub');
  required(manifest.host?.os, 'host.os');
  required(manifest.host?.agent_mode, 'host.agent_mode');
  required(manifest.host?.runtime, 'host.runtime');
  required(manifest.transport?.mode, 'transport.mode');
  required(manifest.bot?.name, 'bot.name');
  required(manifest.bot?.harness, 'bot.harness');
}

if (errors.length) {
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}
console.log(`Setup manifest valid${requireReady ? ' and ready for staged setup' : ''}.`);
