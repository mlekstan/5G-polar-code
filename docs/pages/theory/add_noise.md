## Noise parameters

!!! info "Symbols info"
    
    - $E_b/N_0$ — the ratio of bit energy to noise power density, expressed in dB
    - $N$ — number of noise samples generated
    - $K$ — number of bits modulated simultaneously (e.g. in M-ary modulation)

Converting from dB to linear scale:

$$
\frac{N_0}{E_b} = 10^{-\frac{E_b/N_0\,[\mathrm{dB}]}{10}}.
$$

---

## Standard deviation of noise

By definition of Gaussian white noise, the noise energy per bit is \(\tfrac{N_0}{2}\). For \(K\) bits and \(N\) samples, the standard deviation \(\sigma\) is:

$$
\sigma
= \sqrt{\frac{1}{2}\,\frac{N}{K}\,\frac{N_0}{E_b}}
= \sqrt{\frac{1}{2}\,\frac{N}{K}\,10^{-\frac{E_b/N_0\,\mathrm{[dB]}}{10}}}.
$$

---

## Generating AWGN in Python

```python
def gwn(self, EbN0dB: float, K: int, N: int) -> NDArray[np.float64]:
    # Converting E_b/N_0 from dB to linear scale
    N0Eb = 10 ** (-EbN0dB/10)
    # Calculating standard deviation
    std_dev = sqrt(0.5 * N/K * N0Eb)
    # Generating N samples of white gaussian noise
    return np.random.randn(N) * std_dev
```