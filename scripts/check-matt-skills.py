#!/usr/bin/env python3
"""Check overlay frontmatter, invocation policies, links and source dependencies.

Run with `uv run --with pyyaml python scripts/check-matt-skills.py`.
"""
import importlib.util
import json
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('matt_overlay', ROOT / 'scripts/matt-overlay.py')
overlay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(overlay)
manifest, pristine, adapted = overlay.render()
overlay.check_generated(adapted)
links = 0
for name, files in adapted.items():
    text = files['SKILL.md'].decode()
    frontmatter = yaml.safe_load(text.split('---\n', 2)[1])
    assert frontmatter['name'] == name, f'Name mismatch: {name}'
    assert isinstance(frontmatter['description'], str) and frontmatter['description'], name
    if name in pristine:
        original = yaml.safe_load(pristine[name]['SKILL.md'].decode().split('---\n', 2)[1])
        assert frontmatter == original, f'Frontmatter changed: {name}'
        if frontmatter.get('disable-model-invocation'):
            policy = yaml.safe_load(files['agents/openai.yaml'])
            assert policy['policy']['allow_implicit_invocation'] is False, name
    for filename, data in files.items():
        if not filename.endswith('.md'):
            continue
        # Example code fences contain illustrative paths, not actionable links.
        prose = re.sub(r'(?m)^```.*?^```[^\n]*', '', data.decode(), flags=re.S)
        for link in re.findall(r'\[[^\]\n]*\]\(([^)]+)\)', prose):
            if re.match(r'^(https?:|#|mailto:|mention:|/)', link) or '<' in link:
                continue
            link = link.split('#')[0]
            if link:
                target = ROOT / name / Path(filename).parent / link
                assert target.exists(), f'Broken local link: {name}/{filename}: {link}'
            links += 1
for name in ['flight-deck-workflow', 'ambulando-artefacts', 'wingman-sessions', 'artifacts']:
    assert (ROOT / name / 'SKILL.md').is_file(), f'Missing source dependency: {name}'
print(json.dumps({'frontmatter': len(adapted), 'upstream_policies_preserved': len(pristine),
                  'local_links_checked': links, 'source_dependencies': 'present'}))
