# Cryptography Foundations Atlas

An independent bilingual learning site for systems and security engineers. Default English, with Chinese available on every page.

**Published site:** https://shundazhang.github.io/cryptography-basics/

14 chapters cover foundations, symmetric cryptography, public-key encryption and signatures, Hash/MAC/KDF, randomness, security theory, history, TLS 1.3, SPDM, applied cryptography, future directions, experiments and primary sources. Ten semantic HTML diagrams explain the boundaries between primitives and protocols.

Four browser experiments use WebCrypto for SHA-256, AES-GCM authentication and replay behavior, ECDSA signature verification, and an intentionally insecure GCM nonce-reuse demonstration. Experiments do not upload data or store keys. Use HTTPS or localhost. The downloadable Python exercise checks standard-library behavior and an RFC 5869 known-answer vector; toy arithmetic is explicitly unsuitable for deployment.

## Build and preview

Requires Python 3; no third-party build dependencies.

```sh
python3 build.py
python3 labs/core_examples.py
python3 -m http.server 8767 --bind 127.0.0.1
```

Open http://localhost:8767/ . GitHub Pages serves the generated files directly from the main branch root.

Edit `content.py` for the bilingual notes and source catalog, `diagrams.py` for figures, and `build.py` for page layouts. `labs.js` holds the browser experiments. No external fonts, scripts, analytics or cloud simulator accounts are required.

## Scope and sources

Original explanations are paired with primary-source links to NIST, IETF, DMTF, textbook authors and official API documentation. Historical specifications and informational RFCs are labeled. Review date: 30 September 2026. Notes explain SPDM 1.4.1 and published RFC 10024 hybrid TLS key agreement; later errata and version changes should be checked at the primary sources.

These are study notes and deliberately small experiments, not a deployable cryptographic library. Reuse maintained libraries and specified protocols for real systems.
