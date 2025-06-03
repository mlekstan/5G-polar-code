# Operation overview

## Transmission process
Project simulates transsmission process (with focus on 5G polar code) in following steps:

1. Message source
2. Polar encoding
3. BPSK modulation
4. Sending through AWGN channel
5. Successive Cancelation decoding

```mermaid
---
title: Transmission process
---

flowchart LR
  Source e1@==> E[Polar Encoder]
  E e2@==> M[BPSK Modulator]
  M e3@==> C[AWGN Channel]
  C e4@==> D[SC Decoder]

  e1@{ animate: true }
  e2@{ animate: true }
  e3@{ animate: true }
  e4@{ animate: true }
```

