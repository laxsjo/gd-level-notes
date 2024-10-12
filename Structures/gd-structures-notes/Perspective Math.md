The perspective in this level is built based on groups defined to be positioned at a virtual depth (which I'll label as the z-axis) from the camera. An item is placed on it's virtual x and y position as if a orthogonal projection was applied (i.e. where no side faces are visible). They are then positioned at the start of the level and made to follow the camera as appropriate such that their position is correctly moving as if a 3D perspective was applied.
The camera is decided to be 40 blocks "away" from the player, referred to as the "player layer" or just "the player". This is an arbitrary choice, and it probably decides the FOV of the camera or something (haven't cared enough to work out the math).

At the start of the level, an object is moved to the center of the screen, hence forth referred to as "the center object", which will follow the camera center for the remainder of the level. Then, objects in a specific group x, at a distance $d$ from the player are scaled with the center object as center by the amount $s$ in the formula below.
$$s=\frac{1}{1+ \frac{d}{40}}$$
Then the objects of group x are made to follow the center object using a follow trigger by the amount $\fn{mod}$.
$$\fn{mod}=1- \frac{1}{1+ \frac{d}{40}}$$

As the follow trigger has a accuracy of two decimal places, the lowest increment change in follow mod would be $0.01$. The inverse of the mod formula is
$$\begin{align*}
d&= - \frac{40\fn{mod}}{\fn{mod}-1},
\end{align*}$$
which if we plug in $\fn{mod}=0.01$ into, we get $\Δd=0.\overline{40}\block$. Actually this is incorrect, as $d(\fn{mod})$ isn't a linear function!

Actually, there is a second concept referred to as the "depth factor", which is how many times the distance from the camera to the player layer would have to be multiplied to reach the considered depth. So if an object would be twice the distance  of the player away from the camera, its depth factor would be $2$. Denoted by $\fn{df}$, it is given by the following formula:
$$\fn{df}=1+ \frac{d}{40}$$
