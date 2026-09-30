/* Local teaching experiments. WebCrypto handles algorithms; no network calls. */
(() => {
  'use strict';
  const zh = document.documentElement.lang.startsWith('zh');
  const t = (en, cn) => zh ? cn : en;
  const encoder = new TextEncoder();
  const hex = value => Array.from(new Uint8Array(value), b => b.toString(16).padStart(2, '0')).join('');
  const xor = (a, b) => Uint8Array.from(a.slice(0, Math.min(a.length, b.length)), (v, i) => v ^ b[i]);
  const equal = (a, b) => a.length === b.length && a.every((v, i) => v === b[i]);
  const bytes = id => encoder.encode(document.getElementById(id).value);
  const write = (lab, message, output, pass = true) => {
    const state = document.getElementById(`${lab}-state`);
    state.textContent = message;
    state.dataset.pass = String(pass);
    document.getElementById(`${lab}-output`).textContent = output;
  };
  let record = null;
  let signed = null;
  const aesKey = () => crypto.subtle.generateKey({name: 'AES-GCM', length: 256}, false, ['encrypt', 'decrypt']);
  const randomNonce = () => crypto.getRandomValues(new Uint8Array(12));
  const gcm = (iv, additionalData) => ({name: 'AES-GCM', iv, additionalData, tagLength: 128});
  const signatureAlgorithm = {name: 'ECDSA', hash: 'SHA-256'};
  const requireRecord = () => { if (!record) throw new Error(t('Create a fresh record first', '请先创建新记录')); };
  const requireSignature = () => { if (!signed) throw new Error(t('Create a key and signature first', '请先创建密钥及签名')); };
  async function open(iv, aad, ciphertext) {
    try { return new Uint8Array(await crypto.subtle.decrypt(gcm(iv, aad), record.key, ciphertext)); }
    catch (err) { if (err.name === 'OperationError') return null; throw err; }
  }
  const actions = {
    async 'hash-compare'() {
      const input = bytes('hash-text');
      const changed = encoder.encode(document.getElementById('hash-text').value + '!');
      const a = new Uint8Array(await crypto.subtle.digest('SHA-256', input));
      const b = new Uint8Array(await crypto.subtle.digest('SHA-256', changed));
      const differences = xor(a, b).reduce((sum, value) => sum + value.toString(2).replace(/0/g, '').length, 0);
      const known = hex(a) === '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824';
      write('hash', t(`${differences} of 256 output bits differ`, `256 个输出位中 ${differences} 位不同`),
        `SHA-256(input)\n${hex(a)}\n\nSHA-256(input + !)\n${hex(b)}\n\n` + t('Input bytes: ', '输入字节数：') + input.length +
        (document.getElementById('hash-text').value === 'hello' ? '\n' + t('Known-answer check for hello: ', 'hello 已知答案检查：') + String(known) : ''));
    },
    async 'aead-seal'() {
      const plaintext = bytes('aead-text'); const aad = bytes('aead-aad');
      const key = await aesKey(); const iv = randomNonce();
      const ct = new Uint8Array(await crypto.subtle.encrypt(gcm(iv, aad), key, plaintext));
      record = {key, iv, aad, ct, plaintext};
      write('aead', t('Record sealed — now test verification', '记录已密封 — 现在测试认证'),
        `AES-256-GCM\nNonce (96 bits): ${hex(iv)}\nAAD (UTF-8 hex): ${hex(aad)}\nCiphertext: ${hex(ct.slice(0, -16))}\nTag (128 bits): ${hex(ct.slice(-16))}\n` + t('The key is non-extractable and is not displayed', '密钥不可导出且不显示'));
    },
    async 'aead-valid'() {
      requireRecord(); const result = await open(record.iv, record.aad, record.ct);
      const valid = result !== null && equal(result, record.plaintext);
      write('aead', t(valid ? 'Authenticated — plaintext released' : 'Unexpected verification failure', valid ? '认证通过 — 释放明文' : '异常：认证失败'), result === null ? 'REJECTED' : new TextDecoder().decode(result), valid);
    },
    async 'aead-tamper'() {
      requireRecord(); const modified = record.ct.slice(); modified[0] ^= 1;
      const result = await open(record.iv, record.aad, modified);
      write('aead', t(result === null ? 'Tampering rejected — no plaintext released' : 'Unexpected acceptance', result === null ? '拒绝篡改 — 不释放明文' : '异常：被接受'),
        t('Changed first ciphertext byte (or tag if the message is empty)\n', '修改首个密文字节（空消息时为 Tag）\n') + `Authentication result: ${result === null ? 'REJECTED' : 'ACCEPTED'}`, result === null);
    },
    async 'aead-context'() {
      requireRecord(); const changed = new Uint8Array(record.aad.length + 1); changed.set(record.aad); changed[changed.length - 1] = 33;
      const result = await open(record.iv, changed, record.ct);
      write('aead', t(result === null ? 'Changed AAD rejected — context is authenticated' : 'Unexpected acceptance', result === null ? '拒绝修改后的 AAD — 上下文被认证' : '异常：被接受'),
        `Changed AAD: ${hex(changed)}\nAuthentication result: ${result === null ? 'REJECTED' : 'ACCEPTED'}`, result === null);
    },
    async 'aead-replay'() {
      requireRecord(); const first = await open(record.iv, record.aad, record.ct); const second = await open(record.iv, record.aad, record.ct);
      const accepted = first !== null && second !== null;
      write('aead', t('Replay needs protocol state', '拒绝重放需要协议状态'),
        `Open #1: ${first === null ? 'REJECTED' : 'ACCEPTED'}\nOpen #2: ${second === null ? 'REJECTED' : 'ACCEPTED'}\n\n` + t('Both copies are cryptographically authentic. No replay filter is present in this demo. Track sequence numbers or challenges in the protocol.', '两份记录都通过密码认证。本演示没有重放过滤。应由协议追踪序号或挑战。'), accepted ? 'info' : false);
    },
    async 'signature-create'() {
      const keys = await crypto.subtle.generateKey({name: 'ECDSA', namedCurve: 'P-256'}, false, ['sign', 'verify']);
      const message = bytes('signature-text'); const signature = await crypto.subtle.sign(signatureAlgorithm, keys.privateKey, message);
      const publicBytes = await crypto.subtle.exportKey('raw', keys.publicKey);
      signed = {publicKey: keys.publicKey, message, signature};
      write('signature', t('Signature created — verify the bytes and key', '已创建签名 — 检查消息字节与公钥'),
        `ECDSA P-256 / SHA-256\nPublic key (raw): ${hex(publicBytes)}\nSignature (WebCrypto r || s): ${hex(signature)}\n\n` + t('No certificate or identity assertion is included', '不包含证书或身份声明'));
    },
    async 'signature-valid'() {
      requireSignature(); const valid = await crypto.subtle.verify(signatureAlgorithm, signed.publicKey, signed.signature, signed.message);
      write('signature', t(valid ? 'Original message verifies' : 'Unexpected verification failure', valid ? '原消息验签通过' : '异常：验签失败'), `verify(original, original_key) = ${valid}`, valid);
    },
    async 'signature-message'() {
      requireSignature(); const changed = new Uint8Array(signed.message.length + 1); changed.set(signed.message); changed[changed.length - 1] = 33;
      const valid = await crypto.subtle.verify(signatureAlgorithm, signed.publicKey, signed.signature, changed);
      write('signature', t(!valid ? 'Changed message rejected' : 'Unexpected acceptance', !valid ? '拒绝修改后的消息' : '异常：被接受'), `verify(changed_message, original_key) = ${valid}`, !valid);
    },
    async 'signature-key'() {
      requireSignature(); const other = await crypto.subtle.generateKey({name: 'ECDSA', namedCurve: 'P-256'}, false, ['sign', 'verify']);
      const valid = await crypto.subtle.verify(signatureAlgorithm, other.publicKey, signed.signature, signed.message);
      write('signature', t(!valid ? 'Different public key rejected' : 'Unexpected acceptance', !valid ? '拒绝不同公钥' : '异常：被接受'), `verify(original, other_key) = ${valid}`, !valid);
    },
    async nonce(reuse) {
      const first = bytes('nonce-first'); const second = bytes('nonce-second');
      const key = await aesKey(); const iv1 = randomNonce(); let iv2 = reuse ? iv1 : randomNonce();
      while (!reuse && equal(iv1, iv2)) iv2 = randomNonce();
      const ct1 = new Uint8Array(await crypto.subtle.encrypt(gcm(iv1, new Uint8Array()), key, first));
      const ct2 = new Uint8Array(await crypto.subtle.encrypt(gcm(iv2, new Uint8Array()), key, second));
      const px = xor(first, second); const cx = xor(ct1.slice(0, -16), ct2.slice(0, -16)); const match = equal(px, cx);
      const informative = px.length === 0 || !reuse;
      write('nonce', px.length === 0 ? t('Enter two nonempty messages to compare', '输入两条非空消息才能比较') :
        reuse ? t('Repeated keystream exposes the XOR relationship', '重复密钥流暴露 XOR 关系') : t('Distinct nonces change the keystream', '不同 Nonce 改变密钥流'),
        `Nonce 1: ${hex(iv1)}\nNonce 2: ${hex(iv2)}\nCompared bytes: ${px.length}\nP1 XOR P2: ${hex(px)}\nC1 XOR C2: ${hex(cx)}\nEqual: ${match}\n\n` +
        (reuse ? t('Intentional misuse. Tags excluded. Never reuse a GCM nonce with the same key.', '故意误用；已排除 Tag。切勿在同一 GCM 密钥下复用 Nonce。') : t('A single nonmatch illustrates this sample; it does not prove security. Very short samples can match by chance.', '本次不相等只说明这组样本，不证明安全。极短样本可能偶然相等。')),
        informative ? 'info' : match);
    },
    async 'nonce-reuse'() { await actions.nonce(true); },
    async 'nonce-fresh'() { await actions.nonce(false); }
  };
  document.querySelectorAll('[data-lab]').forEach(box => {
    box.addEventListener('click', async event => {
      const button = event.target.closest('button[data-action]');
      if (!button || box.dataset.busy === 'true') return;
      const lab = box.dataset.lab; box.dataset.busy = 'true';
      const buttons = box.querySelectorAll('button'); buttons.forEach(b => b.disabled = true);
      try {
        if (!globalThis.crypto?.subtle) throw new Error(t('WebCrypto is unavailable. Use HTTPS or localhost in a supported browser.', 'WebCrypto 不可用，请使用受支持浏览器中的 HTTPS 或 localhost。'));
        await actions[button.dataset.action]();
      } catch (error) {
        write(lab, t('Experiment could not run', '实验未能运行'), error.message || error.name, false);
      } finally { box.dataset.busy = 'false'; buttons.forEach(b => b.disabled = false); }
    });
  });
})();
