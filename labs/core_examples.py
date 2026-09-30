"""Local teaching checks using only Python's standard library.
Run: python3 core_examples.py
Tiny DH parameters are insecure and used ONLY for arithmetic demonstration.
"""
import hashlib
import hmac
import secrets


def hkdf_sha256(ikm, salt, info, length):
    """RFC 5869 extract/expand for a known-answer test; not a deployment API."""
    if not 0 <= length <= 255 * 32:
        raise ValueError('HKDF output length out of bounds')
    prk = hmac.digest(salt or bytes(32), ikm, 'sha256')
    output = b''
    block = b''
    for counter in range(1, (length + 31) // 32 + 1):
        block = hmac.digest(prk, block + info + bytes([counter]), 'sha256')
        output += block
    return prk, output[:length]


def main():
    digest = hashlib.sha256(b'hello').hexdigest()
    assert digest == '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    print('PASS: SHA-256 known answer')
    # RFC 5869 Appendix A.1, SHA-256 test case 1.
    prk, okm = hkdf_sha256(bytes.fromhex('0b' * 22), bytes(range(13)), bytes(range(240, 250)), 42)
    assert prk.hex() == '077709362c2e32df0ddc3f0dc47bba6390b6c73bb50f9c3122ec844ad7c2b3e5'
    assert okm.hex() == '3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c5db02d56ecc4c5bf34007208d5b887185865'
    _, separated = hkdf_sha256(bytes.fromhex('0b' * 22), bytes(range(13)), b'another-purpose', 42)
    assert separated != okm
    print('PASS: RFC 5869 known answer and purpose separation')
    key = secrets.token_bytes(32)
    message = b'account=demo;amount=10'
    tag = hmac.digest(key, message, 'sha256')
    assert hmac.compare_digest(tag, hmac.digest(key, message, 'sha256'))
    assert not hmac.compare_digest(tag, hmac.digest(key, message + b'!', 'sha256'))
    assert not hmac.compare_digest(tag, hmac.digest(secrets.token_bytes(32), message, 'sha256'))
    print('PASS: HMAC valid, tampered-message and different-key checks')
    # Public toy group. NEVER use these parameters for secrecy.
    p, g, a, b = 23, 5, 6, 15
    public_a, public_b = pow(g, a, p), pow(g, b, p)
    shared_a, shared_b = pow(public_b, a, p), pow(public_a, b, p)
    assert (public_a, public_b, shared_a, shared_b) == (8, 19, 2, 2)
    print('PASS: tiny DH arithmetic (INSECURE teaching group)')
    print('Random key generated from secrets; secret bytes intentionally not printed')


if __name__ == '__main__':
    main()
