import json
import os
from pathlib import Path

from import_settings_string import settings_string_to_preset

import requests

def fetch_presets(branch):
  cache = Path(f'cached_presets_{branch}.json')
  if not cache.exists():
    raise
    if 'DK64_API_KEY' in os.environ:
      headers = { 'X-API-Key': os.environ['DK64_API_KEY'] }
    else:
      headers = { 'Referer': 'https://dk64randomizer.com/' }
    r = requests.get(f'https://api.dk64rando.com/api/get_presets?branch={branch}', headers=headers)
    r.raise_for_status()
    cache.write_text(r.text, encoding='utf-8')
  return json.loads(cache.read_text(encoding='utf-8'))

def test_import_all_settings():
  with Path(__file__).with_name('presets.json').open(encoding='utf-8') as f:
    expected_presets = {}
    # Discarding the preset keys here; they're internal to the calculator UX.
    for preset in json.load(f).values():
      expected_presets[preset['name']] = preset

  actual_presets = fetch_presets('dev')

  assert len(expected_presets) == len(actual_presets)
  for actual_preset in actual_presets:
    expected = expected_presets.pop(actual_preset['name'])
    actual = settings_string_to_preset(actual_preset['settings_string'], actual_preset['name'])
    assert expected == actual
  assert len(expected_presets) == 0

if __name__ == '__main__':
  import pytest
  raise SystemExit(pytest.main([__file__, "-vv", "--tb=short"]))