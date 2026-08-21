import json
import os
import sys
from pathlib import Path

# getStringFile (js.py shim) loads schema files relative to cwd, so the randomizer root
# (our cwd) must be importable before we import anything from `randomizer`.
sys.path.insert(0, os.getcwd())

from randomizer.SettingStrings import decrypt_settings_string_enum
from randomizer.Settings import Settings
from randomizer.Lists.Switches import SwitchData
from randomizer.Enums.Switches import Switches
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Settings import ActivateAllBananaports, ClimbingStatus
from randomizer.Enums.Types import Types

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

    # Unused, but included so we can import accurately
    "helm_punch_gates": None,
    "helm_star_gates": None,
}


def handle_switchsanity(settings):
    if not settings.switchsanity_enabled:
        return None

    assignments = {
        Switches.JapesFeather: settings.switchsanity_switch_japes_to_hive,
        Switches.JapesRambi: settings.switchsanity_switch_japes_to_rambi,
        Switches.JapesPainting: settings.switchsanity_switch_japes_to_painting_room,
        Switches.JapesDiddyCave: settings.switchsanity_switch_japes_to_cavern,
        Switches.JapesFreeKong: settings.switchsanity_switch_japes_free_kong,
        Switches.AztecBlueprintDoor: settings.switchsanity_switch_aztec_to_kasplat_room,
        Switches.AztecLlamaCoconut: settings.switchsanity_switch_aztec_llama_front,
        Switches.AztecLlamaGrape: settings.switchsanity_switch_aztec_llama_side,
        Switches.AztecLlamaFeather: settings.switchsanity_switch_aztec_llama_back,
        Switches.GalleonLighthouse: settings.switchsanity_switch_galleon_to_lighthouse_side,
        Switches.GalleonShipwreck: settings.switchsanity_switch_galleon_to_shipwreck_side,
        Switches.GalleonCannonGame: settings.switchsanity_switch_galleon_to_cannon_game,
        Switches.FungiYellow: settings.switchsanity_switch_fungi_yellow_tunnel,
        Switches.FungiGreenFeather: settings.switchsanity_switch_fungi_green_tunnel_near,
        Switches.FungiGreenPineapple: settings.switchsanity_switch_fungi_green_tunnel_far,

        Switches.AztecGuitar: settings.switchsanity_switch_aztec_to_connector_tunnel,

        Switches.AztecQuicksandSwitch: settings.switchsanity_switch_aztec_sand_tunnel,

        # Isles has no CBs.
        Switches.IslesMonkeyport: None,
        Switches.IslesHelmLobbyGone: None,
        Switches.IslesAztecLobbyFeather: None,
        Switches.IslesFungiLobbyFeather: None,
        Switches.IslesSpawnRocketbarrel: None,

        # Unlike Japes, the other kong unlocks don't impact the world, so they don't matter for CBs.
        Switches.AztecOKONGPuzzle: None,
        Switches.AztecLlamaPuzzle: None,
        Switches.FactoryFreeKong: None,
    }
    # Some legacy names (to be removed at some point)
    name_overrides = {
        Switches.JapesFeather: "JapesShellhive",
        Switches.GalleonShipwreck: "GalleonPeanut",
        Switches.FungiYellow: "ForestYellowTunnel",
        Switches.FungiGreenFeather: "ForestGreenTunnelFeather",
        Switches.FungiGreenPineapple: "ForestGreenTunnelPineapple",
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
    for switch in SwitchData:
        assigned = assignments[switch]
        if assigned is None:
            continue
        switch_name = name_overrides.get(switch, switch.name)
        if SwitchData[switch].switch_type == SwitchType.GunSwitch:
            if assigned.name == "random":
                # Random-per-seed switchsanity just uses a placeholder, since it can never collapse with another requirement.
                overrides[switch_name] = f"{switch_name}Random"
            elif assigned.name == "any":
                overrides[switch_name] = "AnyGun"
            elif guns[Kongs(assigned.value)] != guns[SwitchData[switch].kong]:
                overrides[switch_name] = guns[Kongs(assigned.value)]
        elif SwitchData[switch].switch_type == SwitchType.InstrumentPad:
            if assigned.name == "random":
                # Random-per-seed switchsanity just uses a placeholder, since it can never collapse with another requirement.
                overrides[switch_name] = f"{switch_name}Random"
            elif assigned.name == "any":
                overrides[switch_name] = "AnyInstrument"
            elif instruments[Kongs(assigned.value)] != instruments[SwitchData[switch].kong]:
                overrides[switch_name] = instruments[Kongs(assigned.value)]
        elif SwitchData[switch].switch_type == SwitchType.SlamSwitch:
            pass # The calculator doesn't support this yet
    return overrides


def settings_to_config(settings):
    # These two are just a straight name translation.
    config = {
        "galleon_water": {"lowered": "Low", "raised": "High"}[settings.galleon_water.name],
        "fungi_time": {"day": "Day", "night": "Night", "dusk": "Dusk", "progressive": "Progressive"}[settings.fungi_time.name],
    }

    config["barriers"] = []
    for barrier in settings.remove_barriers_selected:
        if BARRIERS[barrier.name]:
            config["barriers"].append(BARRIERS[barrier.name])
    if settings.activate_all_bananaports == ActivateAllBananaports.all:
        config["barriers"].append("switchAllWarps")
    if settings.climbing_status == ClimbingStatus.normal:
        config["barriers"].append("switchClimbing")
    if settings.start_with_slam:
        config["barriers"].append("switchSlam")

    config["full_medal"] = int(settings.medal_cb_req)
    if Types.HalfMedal in settings.shuffled_location_types:
        # "Half" medals do not have to be strictly 50% of the full medal (mirrors Spoiler.py).
        config["half_medal"] = max(1, int(config["full_medal"] * (int(settings.half_medal_percentage) / 100)))

    if switchsanity := handle_switchsanity(settings):
        config["switchsanity"] = switchsanity
    return config


settings = Settings(decrypt_settings_string_enum(sys.argv[1]))
key = sys.argv[2]
name = sys.argv[3]
config = {"name": name, **settings_to_config(settings)}

# Add the settings to the JSON data
preset_file = Path("../presets.json") # We are running inside the DK64-Randomizer tree
with preset_file.open("r", encoding="utf-8") as f:
    presets = json.load(f)
presets[key] = config
with preset_file.open("w", encoding="utf-8") as f:
    json.dump(presets, f, indent=4)

# Add the key to the HTML listing
index_file = Path("../index.html")
marker = "// Imported presets are added above this line"
html = index_file.read_text(encoding="utf-8")
marker_pos = html.index(marker)  # raises if the anchor is missing
indent = html[html.rfind("\n", 0, marker_pos) + 1 : marker_pos]
anchor = indent + marker
entry = f'{indent}"{key}",\n'
if entry not in html:
    index_file.write_text(html.replace(anchor, entry + anchor, 1), encoding="utf-8")
