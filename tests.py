import json
import os
from pathlib import Path

import requests

from import_settings_string import settings_to_config

if 'DK64_API_KEY' in os.environ:
  headers = { 'X-API-Key': os.environ['DK64_API_KEY'] }
else:
  headers = { 'Referer': 'https://dk64randomizer.com/' }

def test_import_all_settings():
  with Path(__file__).with_name('presets.json').open(encoding='utf-8') as f:
    expected_presets = {}
    # Discarding the preset keys here; they're internal to the calculator UX.
    for preset in json.load(f).values():
      expected_presets[preset['name']] = preset

  cache = Path('cached_presets.json')
  if not cache.exists():
    r = requests.get('https://api.dk64rando.com/api/get_presets', headers=headers)
    r.raise_for_status()
    with cache.open('w', encoding='utf-8') as f:
      f.write(r.text)
  with cache.open('r', encoding='utf-8') as f:
    actual_presets = json.load(f)

  assert len(expected_presets) == len(actual_presets)
  for actual_preset in actual_presets:
    expected = expected_presets.pop(actual_preset['name'])
    actual = settings_to_config(actual_preset['settings_string'], actual_preset['name'])
    assert expected == actual
  assert len(expected_presets) == 0

if __name__ == '__main__':
  import pytest
  raise SystemExit(pytest.main([__file__, "-vv", "--tb=short"]))