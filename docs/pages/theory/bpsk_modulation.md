In BPSK (Binary Phase Shift Keying), each bit $(u_j \in \{0,1\}$ is mapped to a symbol.

$$
r_j = 1 - 2\,u_j
\quad\Longrightarrow\quad
r_j =
\begin{cases}
+1, & \text{if } u_j = 0,\\
-1, & \text{if } u_j = 1.
\end{cases}
$$

The entire BPSK signal is written as:

$$
s(t)
= \sum_{j=1}^{N}
r_j \,\cos\bigl(2\pi f_c\,t\bigr)\,
\Pi\!\Bigl(\frac{t - jT_r}{T_r}\Bigr),
$$

where the rectangular function $\Pi(z)$ is defined as:

$$
\Pi(z) =
\begin{cases}
1, & 0 \le z < 1,\\
0, & \text{otherwise}.
\end{cases}
$$

!!! info "Symbols info"

    - $\vec{u}$ – input bit sequence, where $u_j \in \{0,1\}$
    - $\vec{r}$ – BPSK symbols, where $r_j \in \{+1,-1\}$  
    - $f_c$ – carrier frequency  
    - $T_r$ – bit duration  
    - $N$ – number of bits
