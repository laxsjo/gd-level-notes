darken amount: -rgb(0.15 0.15 0.15) ~= -rgb(38 38 38)

Let $C$ be the set of all colors (with an alpha).
$$\begin{align*}
C&= \set{(r, g, b, a)\suchthat r,g,b,a\in ℕ\and r,g,b,a⩽255}\\
\end{align*}$$
$$\begin{align*}
\fn{rgb}&:C\to\text{RGB part}\\
\fn{rgb}(c)&= (r,g,b)\\
\\
\fn{α}&:C\toℕ\\
\fn{α}(c)&= a\\
\\
c=(r,g,b,a) \and c\in C &\Implies c_{\fn{rgb}}=(r,g,b) \\
c=(r,g,b,a) \and c\in C &\Implies c_{\fn{α}}=a \\\\

\end{align*}$$

$$\begin{align*}
c_{d}&= \fn{rgb}(38,38,38)\\
\\
d&:C\to C\\
d(c)&= c_{\fn{rgb}}·c_α-c_{d \fn{rgb}}·c_{d \fn{α}}\\
\\

\end{align*}$$