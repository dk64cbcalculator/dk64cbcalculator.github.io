import json
import os
import sys
from pathlib import Path

# getStringFile (js.py shim) loads schema files relative to cwd, so the randomizer root
# (our cwd) must be importable before we import anything from `randomizer`.
sys.path.insert(0, os.getcwd())

from randomizer.SettingStrings import decrypt_settings_string_enum
from randomizer.Lists.Switches import SwitchData
from randomizer.Enums.Switches import Switches
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Enums.Kongs import Kongs

BARRIERS = {
    "japes_coconut_gates": "switchJapesCoconut",
    "japes_shellhive_gate": "switchJapesShellhive",
    "aztec_tunnel_door": "switchAztecTunnel",
    "aztec_5dtemple_switches": "switchAztec5DT",
    "aztec_llama_switches": "switchAztecLlama",
    "aztec_tiny_temple_ice": "switchAztecIce",
    "factory_production_room": "switchFactoryProd",
    "factory_testing_gate": "switchFactoryTesting",
    "galleon_lighthouse_gate": "switchGalleonLighthouse",
    "galleon_shipyard_area_gate": "switchGalleonShipyard",
    "galleon_seasick_ship": "switchGalleonSeasick",
    "galleon_treasure_room": "switchGalleonTreasure",
    "castle_crypt_doors": "switchCryptDoors",
    "forest_green_tunnel": "switchForestGreen",
    "forest_yellow_tunnel": "switchForestYellow",
    "caves_igloo_pads": "switchCavesIgloo",
    "caves_ice_walls": "switchCavesWalls",
}


def handle_switchsanity(settings):
    assignments = {
        Switches.JapesRambi: settings.get("switchsanity_switch_japes_to_rambi"),
        Switches.JapesPainting: settings.get("switchsanity_switch_japes_to_painting_room"),
        Switches.JapesDiddyCave: settings.get("switchsanity_switch_japes_to_cavern"),
        Switches.AztecBlueprintDoor: settings.get("switchsanity_switch_aztec_to_kasplat_room"),
        Switches.AztecLlamaCoconut: settings.get("switchsanity_switch_aztec_llama_front"),
        Switches.AztecLlamaGrape: settings.get("switchsanity_switch_aztec_llama_side"),
        Switches.AztecLlamaFeather: settings.get("switchsanity_switch_aztec_llama_back"),
        Switches.GalleonCannonGame: settings.get("switchsanity_switch_galleon_to_cannon_game"),

        Switches.IslesSpawnRocketbarrel: settings.get("switchsanity_switch_isles_spawn_rocketbarrel"),
        Switches.AztecGuitar: settings.get("switchsanity_switch_aztec_to_connector_tunnel"),

        Switches.AztecQuicksandSwitch: settings.get("switchsanity_switch_aztec_sand_tunnel"),
    }
    guns = {
        Kongs.donkey: "Coconut",
        Kongs.diddy: "Peanut",
        Kongs.lanky: "Grape",
        Kongs.tiny: "Feather",
        Kongs.chunky: "Pineapple",
    }
    instruments = {
        Kongs.donkey: "Bongos",
        Kongs.diddy: "Guitar",
        Kongs.lanky: "Trombone",
        Kongs.tiny: "Sax",
        Kongs.chunky: "Triangle",
    }

    overrides = {}
    for switch, assigned in assignments.items():
        # We are not handling "random per seed" yet.
        if assigned is None or assigned.name == "random":
            continue
        if SwitchData[switch].switch_type == SwitchType.GunSwitch:
            if assigned.name == "any":
                overrides[switch.name] = "AnyGun"
            elif guns[Kongs(assigned.value)] != guns[SwitchData[switch].kong]:
                overrides[switch.name] = guns[Kongs(assigned.value)]
        elif SwitchData[switch].switch_type == SwitchType.InstrumentPad:
            if assigned.name == "any":
                overrides[switch.name] = "AnyInstrument"
            elif instruments[Kongs(assigned.value)] != instruments[SwitchData[switch].kong]:
                overrides[switch.name] = instruments[Kongs(assigned.value)]
        elif SwitchData[switch].switch_type == SwitchType.SlamSwitch:
            pass # The calculator doesn't support this yet
    return overrides


def settings_to_config(settings):
    # These three are just a straight name translation
    barriers = [BARRIERS[barrier.name] for barrier in settings.get("remove_barriers_selected", [])]
    galleon_water = {"lowered": "Low", "raised": "High"}[settings["galleon_water"].name]
    fungi_time = {"day": "Day", "night": "Night", "dusk": "Dusk", "progressive": "Progressive"}[settings["fungi_time"].name]

    warps = settings.get("activate_all_bananaports")
    if warps is not None and warps.name == "all":
        barriers.append("switchAllWarps")

    # Check if we start with climbing *or* if climbing is guaranteed in a starting move pool
    for move in settings.get("starting_move_list_selected", []):
        if move.name == "Climbing":
            barriers.append("switchClimbing")
            break
    else:
        for i in range(5):
            pool = settings.get(f"starting_moves_list_{i + 1}", [])
            if settings.get(f"starting_moves_list_count_{i + 1}", 0) < len(pool):
                continue
            if any(move.name == "Climbing" for move in pool):
                barriers.append("switchClimbing")
                break

    full_medal = int(settings["medal_cb_req"])
    # "Half" medals do not have to be strictly 50% of the full medal (mirrors Spoiler.py).
    half_medal = max(1, int(full_medal * (int(settings.get("half_medal_percentage", 50)) / 100)))

    config = {
        "barriers": barriers,
        "full_medal": full_medal,
        "half_medal": half_medal,
        "galleon_water": galleon_water,
        "fungi_time": fungi_time,
    }
    if switchsanity := handle_switchsanity(settings):
        config["switchsanity"] = switchsanity
    return config


settings = decrypt_settings_string_enum(sys.argv[1])
key = sys.argv[2]
name = sys.argv[3]
config = {"name": name, **settings_to_config(settings)}

preset_file = Path('../presets.json') # We are running inside the DK64-Randomizer tree
with preset_file.open('r', encoding='utf-8') as f:
    presets = json.load(f)
presets[key] = config
with preset_file.open('w', encoding='utf-8') as f:
    json.dump(presets, f, indent=4)

# Register the key in the calculator's ordered preset list, unless it's already listed.
index_file = Path('../index.html')
marker = "// Imported presets are added above this line"
html = index_file.read_text(encoding='utf-8')
marker_pos = html.index(marker)  # raises if the anchor is missing
indent = html[html.rfind("\n", 0, marker_pos) + 1 : marker_pos]
anchor = indent + marker
entry = f'{indent}"{key}",\n'
if entry not in html:
    index_file.write_text(html.replace(anchor, entry + anchor, 1), encoding='utf-8')

