Some things I figured out about how the editor works (that the GD guide doesn't explain).

> [!NOTE] Note About Units
> There are two systems of units used throughout different triggers and the internal code of Geometry Dash. I've decided to name them as follows:
> **Decimal Units**: 10 du = 1 block
> **Internal Units**: 30 iu = 1 block
> 
> For example, the move trigger lets you choose which units you want to use. With "small step" set to false decimal units are used, while setting it to true uses internal units.

# Move Increments
There are move amounts smaller than a half block. I'll call these "Small" (**s**) and "Very Small" (**v**).
These move objects the following amounts:
s = 2 iu = 1/15 block ~= 0.066667 block
v = 0.5 iu = 1/60 block ~= 0.016667 block

Better Edit introduces another even smaller increment, labelled "Unit" (**u**), or "Pixel" in some versions.
u = 0.1 iu = 1/300 block ~= 0.003333 block

Object positions are **rounded down to the nearest 0.1 iu increment** when saving (*I think*) Note that it doesn't update until you exit and re-enter the level.

# Area Triggers
~~Area trigger length and offsets are in internal units (30 = 1 block). *Is this even true?*~~
Area trigger length and offsets are in decimal units (10 = 1 block).

## Effect Direction
Let's say that some area trigger applies an effect, the **main state**, denoted by "100%" in the image below, which is eased of to the **rest state**. When considering the direction arrows, the **rest state** is applied at the base of the arrow in the direction icons, and is gradually transitioned to the **main state** in the arrows direction.
![[Area-Trigger-Direction-Icons.png]]
For the **Area Fade** trigger with configurable "from" and "to" states, the "from" value is the **rest state**, and the "to" value is the **main state**.
For other triggers (**Area Move**, **Rotate**, **Scale**, and **Tint**), the configured effect constitutes the **main state**.

## Mod Front/Back
These are only relevant with directions 3, 4, 7, and 8 (see the image above).
They are weights which control how the width is distributed in the "forwards" and "backwards" directions, allowing you to choose different widths for them.

The direction which has the highest weight will be the same width as configured in "Length", with the other direction getting the appropriate width "proportional to the two weights" (not really sure how to phrase this, can maybe figure out the formula later).

## Deadzone
The "Deadzone" option is given as a fraction from 0 to 1. Say that the effect is applied along a line, starting at the **rest state**, and ending at the **main state**. This line is then divided into two parts. The "Deadzone", aligned to the **rest state**, is then as wide as the configured "Length" multiplied with the fraction.
![[Editor Guide Notes 2024-06-16 11.50.00.excalidraw]]

## Area Move
The official editor guide lies about the "Move Angle" option. 0 degrees actually points **downwards**, and positive values rotate **counter clockwise**.

# Particle Trigger
The particle trigger PosVar X/Y inputs extend the spawn box equally in both directions, measured in internal units (30 = 1 block). This means that the bounding box will have double what width or height was input.
In radius mode, the "StartRad" and "EndRad" inputs are also in internal units.

# Lens Circle Shader
The "Size" value controls the radius of the circle as a fraction of the total screen width. Or it is **almost**. For some reason, setting it to 0.5 makes the circle *slightly* larger than the entire screen width...

I assume that this scales with varying screen widths, but I haven't checked... It's at least true for a 16:9 display.

**TODO**: I should investigate the exact value of the error in the circle radius in comparison to the screen width.

# On Death Trigger Behaviour
The position of the player is remembered after the player has crashed. So for instance, you can reliably make a group move to P1 position after being triggered by an "On Death" trigger.
# Player Movement Speed
Based on [[Measurements#Player Movement Speed|Measurements]].

- **0.5x:** 8.37200 blocks/s
- **1x:** 10.3859 blocks/s
- **2x:** 12.9140 blocks/s
- **3x:** 15.6000 blocks/s
- **4x:** 19.2000 blocks/s