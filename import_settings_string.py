import json
import os
import subprocess
import sys

from pathlib import Path

def settings_string_to_preset(settings_string, name):
    # v6 is currently in development, so settings strings might come in as v5 (stable) or v6 (dev)
    # Unfortunately, due to the overlapping types, we need to do a complete import,
    # so we shell out to a separate python instance to try again (if the import fails).
    root = Path(__file__).parent
    result = subprocess.run(
        [sys.executable, root / 'convert_settings_string.py', settings_string],
        env=os.environ | {'PYTHONPATH': '.'},
        cwd=root / 'DK64-Randomizer',
        capture_output=True, text=True)
    if result.returncode != 0 and 'before version 6' in result.stderr:
        result = subprocess.run(
            [sys.executable, root / 'convert_settings_string.py', settings_string],
            env=os.environ | {'PYTHONPATH': '.'},
            cwd=root / 'DK64-Randomizer-v5', # Secondary clone
            capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return {"name": name} | json.loads(result.stdout)

if __name__ == "__main__":
    config = settings_string_to_preset(sys.argv[1], sys.argv[2])

    key = sys.argv[3]
    # Add the settings to the JSON data
    preset_file = Path("presets.json")
    with preset_file.open("r", encoding="utf-8") as f:
        presets = json.load(f)
    presets[key] = config
    with preset_file.open("w", encoding="utf-8") as f:
        json.dump(presets, f, indent=4)

    # Add the key to the HTML listing
    index_file = Path("index.html")
    marker = "// Imported presets are added above this line"
    html = index_file.read_text(encoding="utf-8")
    marker_pos = html.index(marker)  # raises if the anchor is missing
    indent = html[html.rfind("\n", 0, marker_pos) + 1 : marker_pos]
    anchor = indent + marker
    entry = f'{indent}"{key}",\n'
    if entry not in html:
        index_file.write_text(html.replace(anchor, entry + anchor, 1), encoding="utf-8")