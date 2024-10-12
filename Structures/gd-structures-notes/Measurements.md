iu: This is the internal unit used in the GD engine.
30 iu = 1 block

# Distances
source:
https://gdforum.freeforums.net/thread/41659/p1kachu-presents-geometry-editor-guide
- very small move (vs): 1/60 block = 0.5 iu ~= 0.01667 block
- small move (s): 1/15 block = 2 iu ~= 0.06667 block
- normal move (n): 1 block
- half move (h): 1/2 block = 0.5 block
- big move (b): 5 block

# Combinations
- h - 7s = 0.5s ~= 0.03333 block
- h - 6s = 0.1 block
- 3v = 0.05 block
- 6v = 0.1 block
- s + 2v = 0.1 block

# Object Measurements
Small Quarter Circle Outline
- thickness: 0.1
- outer radius: 0.5 
- inner radius: 0.4

Large Quarter Circle Outline
- thickness: 0.1
- outer radius: 1
- inner radius: 0.9

Very Thin Quarter Circle Outline (tileset 0)
(very blurry and imprecise)
thickness: 1 iu = 1/30 ~= 0.03333

Small Filled Dot (tileset 0)
- width/height: ~0.27

Medium Filled Circle (tileset 0)
- width/height: 1

Larger Filled Circle (tileset 0)
- width/height: ~1.667 (based on calculations)

Almost Filled square (tileset 0, non-scaling)
- width/height: 27.5 iu ~= 0.91667

Circle Icon (tileset 8)
- width/height: 16 iu ~= 0.5333

x: `2*5+2+0.5-2s+2v=12.4`
y: `5+2+0.5+1s+2v=7.6`

circle_2_pos = circle_1_pos + (12.4, 7.6)

# Ship Ground Height
This measures the distance from the gameplay edge (the cyan line shown in the
editor) to the screen edge.
height: 10 iu ~= 0.333 blocks

# Default Gameplay Offset
The distance from the the player center to the camera center, purely along the x-axis.
Default offset: 2.5 blocks = 75 iu

# Player Movement Speed
## Calculation Testing
Moving at 1x speed (blue arrow)
All positions are assumed to be the x positions. They are also in the internal
unit (iu), as displayed by the Geode dev tools.

A object is set to follow the player (using a move trigger with follow player x)
for one second.

Random time sample:
- player pos: 119.439 iu
- following object pos: 118.141 iu
Constant follow error: -1.298 iu
(I also tried at a different time and got *exactly* the same result)

After the fact (like weeks later) I realised that I should have taken note of the framerate during the tests. I think I was running at 240 ticks per second via MegaHack. This means the frame time was ~0.0041667 seconds.

## Results
These actually match with those of some other person on Reddit!
https://www.reddit.com/r/geometrydash/comments/3mh4ph/comment/hy0b5sp/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

When I first did these experiments I let the object follow the player for 1 second. I later repeated them, instead letting the object follow for 10 seconds. The original measurements are given as **Movement speed (1s)**.

I'm not sure, but there could still be some source of error due to how long each frame is. I'm getting uncomfortably high error margins (assuming time measurement is of by up to one frame), at ±0.0108 blocks/s in the case of the green arrow!
### 0.5x (orange arrow)
Constant follow error: -1.047 iu

Letting object move for one second:
- Follow object pos: 250.113 iu
- Calc player pos: 251.160 iu

Letting object move for 10 seconds:
- Follow object pos: 2510.518 iu
- Calc player pos: 2511.565 iu

**Movement speed**: 8.37200 blocks/s
**Movement speed (10s)**: 8.371883 blocks/s
### 1x (blue arrow)
Constant follow error: -1.298

Letting object move for one second:
- Follow object pos: 310.281 iu
- Calc player pos: 311.579 iu

Letting object move for 10 seconds:
- Follow object pos: 3114.561 iu
- Calc player pos: 10.38619667 iu

**Movement speed**: 10.3859 blocks/s
**Movement speed (10s)**: 10.38619 blocks/s
### 2x (green arrow)
Constant follow error: -1.614 iu

Letting object move for one second:
- Follow object pos: 385.807 iu
- Calc player pos: 387.421 iu

Letting object move for 10 seconds:
- Follow object pos: 3872.604 iu
- Calc player pos: 3874.218 iu

**Movement speed**: 12.9140 blocks/s
**Movement speed (10s)**: 12.91406 blocks/s

### 3x (purple arrow)
Constant follow error: -1.950 iu

Letting object move for one second:
- Follow object pos: 466.051 iu
- Calc player pos: 468.001 iu

Letting object move for 10 seconds:
- Follow object pos: 4678.036 iu
- Calc player pos: 4679.986 iu

**Movement speed (1s)**: 15.6000 blocks/s
**Movement speed (10s)**: 15.59995 blocks/s
### 4x (red arrow)
Constant follow error: -2.400 iu

Letting object move for one second:
- Follow object pos: 573.600 iu
- Calc player pos: 576.000 iu

Letting object move for 10 seconds:
- Follow object pos: 5757.464 iu
- Calc player pos: 5759.864 iu

**Movement speed (1s)**: 19.2000 blocks/s
**Movement speed (10s)**: 19.1995 blocks/s
