Moves.JapesCoconut = new Moves("Japes Coconut Gates", true, [
    [Moves.ClimbingCheck, Moves.JapesFreeKong],
    [Moves.AllWarps, Moves.JapesFreeKong],
], true);
Moves.AztecTunnelDoor = new Moves("Aztec Tunnel Door", true, [
    [Moves.Vines, Moves.ClimbingCheck, Moves.AztecGuitar],
    [Moves.ClimbingCheck, Moves.Rocket, Moves.AztecGuitar],
], true);
Moves.Aztec5DT = new Moves("Aztec 5DT Switches", true, [
    [Moves.LevelSlam, Moves.Peanut, Moves.Rocket, Moves.AllWarps],
    [Moves.LevelSlam, Moves.Peanut, Moves.Rocket, Moves.AztecTunnelDoor],
], true);
Moves.AztecLlama = new Moves("Aztec Llama Switch", true, [
    [Moves.Blast, Moves.AllWarps],
    [Moves.Blast, Moves.AztecTunnelDoor],
], true);
Moves.TinyTempleIce = new Moves("Tiny Temple Ice Melted", true, [[Moves.LevelSlam, Moves.Peanut, Moves.Guitar]], true);
Moves.FactoryTesting = new Moves("Testing Side Open", true, [[Moves.SlamCheck]], true);
Moves.FactoryProduction = new Moves("Production Room On", true, [
    [Moves.ClimbingCheck, Moves.Coconut, Moves.Grab, Moves.AllWarps],
    [Moves.ClimbingCheck, Moves.Coconut, Moves.Grab, Moves.FactoryTesting],
], true);
Moves.RaisedWater = new Moves("Galleon Raised Water", true, [
    [Moves.Diving, Moves.AllWarps],
    [Moves.Diving, Moves.GalleonLighthouse],
], true);
Moves.LoweredWater = new Moves("Galleon Lowered Water", true, [
    [Moves.Diving, Moves.AllWarps],
    [Moves.Diving, Moves.GalleonLighthouse],
], true);
Moves.GalleonShipSpawned = new Moves("Ship Spawned", true, [
    [Moves.ClimbingCheck, Moves.LevelSlam, Moves.Grab, Moves.AllWarps],
    [Moves.ClimbingCheck, Moves.LevelSlam, Moves.Grab, Moves.RaisedWater, Moves.GalleonLighthouse],
], true);
Moves.GalleonTreasure = new Moves("Treasure Room Open", true, [
    [Moves.AllWarps, Moves.RaisedWater, Moves.Enguarde],
    [Moves.RaisedWater, Moves.GalleonPeanut, Moves.Enguarde],
], true);
