#!/usr/local/bin/python3.12

from __future__ import annotations
from color import *
from gd_colors import *
from dataclasses import dataclass
from enum import Enum
from typing import *


# Very much a work in progress.
# Ambition is to list all colors used in the level, with descriptive names (now
# that the svg file was corrupted, so the colors are missing).
# TODO: Add description of what "(working color)" means.
colors: list[ColorDesc] = [
    ("#000000", "Black Solid", 8),
    (BlendingColor(rgba("#ffffff", 0.0)), "Transparent White Blending", 14),
    ("#efeef0", "Light BG Surface", 25),
    ("#514f57", "Dark Edge", 26),
    ("#ffc153", "Platform Accent", 27),
    (rgba("#0c0b0d", 0.22), "Detail Shadow", 29),
    (CopyColor((0, 0, add(1.06)), 25), "Light Platform Surface", 30),
    ("#ffbd84", "Sky BG Bottom", 34),
    ("#8b729c", "Sky BG Top", 35),
    ("#393840", "Dark BG Edge", 36),
    (BlendingColor(rgba("#000000", 0.0)), "Transparent Black Blending", 46),
    ("#fffbf2", "Lamp Surface", 49),
    (BlendingColor("#ae9961"), "Lamp Glow Overlay", 50),
    ("#8d846e", "Lamp turned off Surface", 50),
    (CopyColor((0, 0, add(1.4)), 36), "Wall Detail", 54),
    (CopyColor((0, 0, add(0.8)), 54), "Wall Detail Border", 55),
    (CopyColor((0, add(1.84), add(0.6)), 36), "Wall Shadow Solid", 58),
    ("#ffa991", "Red Light Surface", 62),
    (BlendingColor("#b4220a"), "Red Light Glow", 63),
    ("#f7f199", "Orb Yellow Particle Solid", 68),
    ("#ff9ef0", "Orb Pink Particle Solid", 69),
    ("#fdc2a6", "Orb Red Particle Solid", 70),
    ("#9aeaff", "Orb Blue Particle Solid", 71),
    ("#b0ffb0", "Orb Green Particle Solid", 72),
    ("#d77ee1", "Orb Purple Particle Solid", 73),
    ("#000000", "Orb Black Particle Solid", 74),
    ("#8687ff", "Orb Teleport Blue Particle Solid", 75),
    ("#ffc46a", "Orb Teleport Orange Particle Solid", 76),
    ("#ffffff", "Orb Particle Solid reserved?", 77),
    ("#ffffff", "Transition White", 78),
    ("#ff7f2a", "Transition Accent", 79),
    ("#000000", "Transition Black", 80),
    ("#b3765b", "Window Sunset Glow Surface", 81),
    (BlendingColor("#3d2921"), "Sunset Glow Blending", 82),
    (rgba("#3d281f", 0.18), "Gunk Overlay", 83),
    (BlendingColor(rgba("#fefefe", 0.5)), "Shine Overlay", 84),
    ("#8f764d", "Crate Surface", 85),
    (CopyColor((0, 0, add(0.72)), 25), "Light BG Building Surface", 86),
    (CopyColor((0, 0, add(1.12)), 86), "Light BG Building Tilted Surface (facing light)", 87),
    (BlendingColor("#434647"), "Day Sunlight Overlay", 88),
    (CopyColor((0, 0, mul(0.28)), 86), "Light BG Building Surface Lit (eq. to 86 with 88 on top)", 89),
    ("#555661", "Dark BG Building Surface", 90),
    (CopyColor((0, 0, add(0.90)), 90), "Dark BG Building Detail", 91),
    (CopyColor((mul(-29), mul(+0.04), mul(-0.06)), 89), "Light BG Building Surface Lit Shadowed (when the lit surface has additional shadow over it)", 92),
    (CopyColor((0, 0, 0, 0.22), 91), "92 Trans", 93),
    (CopyColor((0, 0, add(0.9), 0.55), 91), "92 Shadow", 94),
    (CopyColor((0, 0, 0, 0.0), 35), "Distance Fog Overlay 1", 95),
    (CopyColor((0, 0, 0, 0.03), 35), "Distance Fog Overlay 2", 96),
    (CopyColor((0, 0, 0, 0.03), 35), "Distance Fog Overlay 3", 97),
    (CopyColor((0, 0, 0, 0.03), 35), "Distance Fog Overlay 4", 98),
    (CopyColor((0, 0, 0, 0.03), 35), "Distance Fog Overlay 5", 99),
    (CopyColor((0, 0, 0, 0.12), 35), "Distance Fog Overlay 6", 100),
    (CopyColor((0, 0, 0, 0.16), 35), "Distance Fog Overlay 7", 101),
    (CopyColor((0, 0, 0, 0.54), 35), "Distance Fog Overlay 8", 102),
    ("#", "Distance Fog Overlay res.", 103),
    ("#", "Distance Fog Overlay res.", 104),
    (rgba("#ffffff", 0.0), "Transparent White", 105),
    ("#ffffff", "VFX Overlay Surface White", 106),
    ("#ff9f24", "VFX Overlay Surface Accent.", 107),
    ("#56ff5a", "2x Speed Portal Surface", 108),
    ("#ffffff", "2x Speed Portal Primary", 109),
    ("#000000", "2x Speed Portal Sec", 110),
    ("#000000", "Transition Animation Color 1 (working color)", 111), # Necessary because gradients can not be flashed by group. (I don't think I ever used this ._.)
    ("#847e6f", "Dust/debree", 112),
    (BlendingColor(CopyColor(50)), "Light VFX Particle Overlay Animation (working color)", 113),
    (BlendingColor("#000000"), "Blending Black", 114),
    (rgba("#182515", 0.19), "Window Glass", 115),
    (BlendingColor(CopyColor(55)), "Reflection - Wall Detail Border", 116),
    (BlendingColor(CopyColor(25)), "Reflection - Light BG Surface", 117),
    (rgba("#61795c", 0.31), "Window Glass Shine", 118),
    (BlendingColor(CopyColor(27)), "Accent VFX Particle Overlay Animation (working color)", 119),
    (CopyColor((0, add(0.96), add(1.04)), 35), "Sky Reflection Solid", 120),
        (CopyColor(115, a=0.2), "Window Glass Reflection Strength 1", 121),
    (CopyColor(115, a=0.3), "Window Glass Reflection Strength 2", 122),
    (CopyColor(115, a=0.4), "Window Glass Reflection Strength 3", 123),
    (CopyColor(115, a=0.5), "Window Glass Reflection Strength 4", 124),
    (CopyColor((0, 0, add(0.84)), 25), "Light BG Surface Border", 125),
    (BlendingColor("#404040"), "Window Glass Shine Overlay", 126),
    ("#8a93a0", "Light Cool Turned Off Surface", 127),
    ("#ddebff", "Light Cool Surface", 128), # Currently unused
    (BlendingColor("#bfc6d1"), "Light Cool Glow Overlay", 129),
    (BlendingColor("#52c4ff"), "Portal Blue Glow Overlay", 130),
    (BlendingColor("#cb8341"), "Portal Orange Glow Overlay", 131),
    ("#5e72ff", "Portal Blue Particle Solid", 132),
    ("#ea7332", "Portal Orange Particle Solid", 133),
    ("#98b4c3", "Portal Blue Shine Solid", 134),
    ("#e58e45", "Portal Orange Shine Solid", 135),
    ("#020308", "Void BG", 136),
    (BlendingColor("#fafbff"), "Void Light Solid Overlay", 137),
    (BlendingColor(CopyColor(68)), "Orb Yellow Particle Glow Overlay (Unused)", 138),
    (BlendingColor(CopyColor(69)), "Orb Pink Particle Glow Overlay (Unused)", 139),
    (BlendingColor(CopyColor(70)), "Orb Red Particle Glow Overlay (Unused?)", 140),
    (BlendingColor(CopyColor(71)), "Orb Blue Particle Glow Overlay", 141),
    (BlendingColor(CopyColor(72)), "Reserved", 142),
    (BlendingColor(CopyColor(73)), "Reserved", 143),
    (BlendingColor(CopyColor(74)), "Reserved", 144),
    (BlendingColor(CopyColor(75)), "Reserved", 145),
    (BlendingColor(CopyColor(76)), "Reserved", 146),
    (BlendingColor(CopyColor(77)), "Reserved", 147),
    ("#ff5440", "Abstract Surface Red Solid", 148),
    ("#", "Abstract Surface Reserved Solid", 149),
    ("#", "Abstract Surface Reserved Solid", 150),
    ("#", "Abstract Surface Reserved Solid", 151),
    ("#", "Abstract Surface Reserved Solid", 152),
    ("#ffffff", "Abstract Surface White Solid", 153),
    (rgba("#000000", 0.0), "Transparent Black", 154),
    (rgba("#ffffff", 0.35), "Abstract White Overlay", 155),
    (CopyColor(148, a=0.35), "Abstract Red Overlay (Unused)", 156),
    (BlendingColor("#000000"), "Black Blending", 157),
    ("#95a56c", "Tree Bark", 158),
    ("#", "Tree Wood", 159), # unused currently
    ("#65bc49", "Tree Leaves", 160),
    ("#", "Grass/Forest Ground", 161),
    ("#ff8b8b", "Death Marker Red", 162),
    (BlendingColor("#3e3c2f"), "Sunlight Overlay", 163),
    ("#", "Skylit Shadow", 164),
    (CopyColor((0, mul(0.3), 0), 68), "Orb Yellow Flash Desaturated", 165),
    (CopyColor((0, mul(0.3), 0), 69), "Orb Pink Flash Desaturated", 166),
    (CopyColor((0, mul(0.3), 0), 70), "Orb Red Flash Desaturated", 167),
    (CopyColor((0, mul(0.3), 0), 71), "Orb Blue Flash Desaturated", 168),
    (CopyColor((0, mul(0.3), 0), 72), "Orb Green Flash Desaturated", 169),
    (CopyColor((0, mul(0.3), 0), 73), "Orb Purple Flash Desaturated", 170),
    ("#f1f4ff", "Orb Black Flash Desaturated", 171),
    (CopyColor((0, mul(0.3), 0), 75), "Orb Teleport Blue Flash Desaturated", 172),
    (CopyColor((0, mul(0.3), 0), 76), "Orb Teleport Orange Flash Desaturated", 173),
    (CopyColor((0, 0, 0), 77), "Orb Reserved Flash Desaturated", 174),
    ("#9598aa", "Stone", 175),
    (CopyColor((0, add(0.18), 0), 176), "Death Red Glow Overlay", 176),
    (CopyColor(62, a=0.5), "Red Light Transparent", 177),
    ("#87b1c5", "Water", 178),
    ("#ff5e5e", "Flower Base", 179),
    ("#efe6dd", "Birch Bark", 180),
]

palette_changes: list[PaletteChangeDesc] = [
    ("Part 2", [
        # ("#cdb6ff", 34),
        # (CopyColor((copy_offset(-21), copy_factor(1.5), copy_factor(0.78)), 34), 35),
        ("#b6b3bc", 25), # Light BG Surface
        ("#474851", 26), # Dark Edge
        ("#fdbf53", 27), # Platform Accent
        ("#38353e", 36), # Dark BG Edge
        (CopyColor((0, 0, 0), 35), 34), # Sky BG Bottom
        ("#a1afcc", 35), # Sky BG Top
    ]),
    ("Part 3", [
        ("e7eaed", 30), # Light Platform Surface
        ("97bff2", 35), # Sky BG Top
    ])
]