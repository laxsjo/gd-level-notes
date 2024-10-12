
$$\begin{align*}
d&= 40·(f_{d}-1)\\
d&= 40f_{d}-40\\
f_{d}&= \frac{d+40}{40}\\
\\
m&= 1 - \frac{1}{f_{d}}\\
m&= 1- \frac{40}{d+40}\\
d+40&= \frac{40}{1-m}\\
d&= \frac{40}{1-m}-40
\end{align*}$$

We have a transformation which scales by $s_{x}$ and $s_{y}$ around the axis $\theta$. We then match this by first scaling by (axis-aligned) $c_{x}$ and $c_{y}$, then skewing by $m_{x}$ and $m_y$. Then:
$$\begin{align*}
c_{x}&= s_{x}\cos{θ}\\
m_{x}c_{y}&= -s_{x}\sinθ\\
m_{y}c_{x}&= s_{y}\sinθ\\
c_{y}&= s_{y}\cos{θ}\\
\\
m_{x}&= - \frac{s_{x}\sinθ}{s_{y}\cosθ}\\
m_{y}&= \frac{s_{y}\sinθ}{s_{x}\cosθ}\\
\\
c_{x}&= s_{x}\cosθ\\
c_{y}&= s_{y}\cosθ\\
m_{x}&= - \frac{s_{x}}{s_{y}}\tanθ\\
m_{y}&= \frac{s_{y}}{s_{x}}\tanθ\\
\end{align*}$$

Assuming $s_{x}=s$ and $s_{y}=1$:
$$\begin{align*}
c_{x}&= s\cosθ\\
c_{y}&= \cosθ\\
m_{x}&= -s\tanθ\\
m_{y}&= \frac{1}{s}\tanθ
\end{align*}$$
