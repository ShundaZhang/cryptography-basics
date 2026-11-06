"""Bilingual AES notes and attributions for unmodified Wikimedia Commons SVGs."""

from html import escape
from urllib.parse import quote

CC0 = 'https://creativecommons.org/publicdomain/zero/1.0/'
PUBLIC_DOMAIN = 'https://creativecommons.org/publicdomain/mark/1.0/'
IMAGES = {
    'AES-SubBytes.svg': (810, 420, 'Matt Crypto', PUBLIC_DOMAIN),
    'AES-ShiftRows.svg': (810, 300, 'Matt Crypto', PUBLIC_DOMAIN),
    'AES-MixColumns.svg': (810, 430, 'Matt Crypto', PUBLIC_DOMAIN),
    'AES-AddRoundKey.svg': (810, 630, 'Matt Crypto', PUBLIC_DOMAIN),
    'ECB_encryption.svg': (601, 242, 'WhiteTimberwolf', PUBLIC_DOMAIN),
    'CBC_encryption.svg': (601, 242, 'WhiteTimberwolf', PUBLIC_DOMAIN),
    'CBC_decryption.svg': (601, 242, 'WhiteTimberwolf', PUBLIC_DOMAIN),
    'CTR_encryption_2.svg': (601, 242, 'Gwenda / WhiteTimberwolf', PUBLIC_DOMAIN),
    'CFB_encryption.svg': (601, 242, 'Gwenda / WhiteTimberwolf', PUBLIC_DOMAIN),
    'OFB_encryption.svg': (601, 242, 'WhiteTimberwolf', PUBLIC_DOMAIN),
    'GCM-Galois_Counter_Mode_with_IV.svg': (696, 765, 'NIST (McGrew / Viega)', CC0),
    'XTS_encryption.svg': (841, 323, 'John-Mark Gurney (Ke6jjj upload)', PUBLIC_DOMAIN),
}


def original_figure(t, filename, caption):
    width, height, credit, license_url = IMAGES[filename]
    asset = 'assets/aes/' + quote(filename)
    source = 'https://commons.wikimedia.org/wiki/File:' + quote(filename)
    license_name = 'CC0 1.0' if license_url == CC0 else t('Public domain', '公有领域')
    return (
        '<figure class="wiki-figure">'
        f'<a class="wiki-image" href="{asset}" target="_blank" rel="noopener"'
        f' aria-label="{t("Open full-size image", "打开完整尺寸原图")} · {escape(caption, quote=True)}">'
        f'<img src="{asset}" width="{width}" height="{height}"'
        f' loading="lazy" decoding="async" alt="{escape(caption, quote=True)}"></a>'
        f'<figcaption><strong>{escape(caption)}</strong><span>{escape(credit)} · '
        f'<a href="{source}">{t("Wikimedia Commons original", "Wikimedia Commons 原图")}</a> · '
        f'<a href="{license_url}">{license_name}</a></span></figcaption></figure>'
    )


def round_steps(t):
    return (
        ('SubBytes', 'AES-SubBytes.svg',
         t('Apply the same nonlinear S-box to each byte independently.',
           '每个字节独立通过同一张非线性 S 盒。'),
         t('The S-box takes the multiplicative inverse in GF(2⁸), with zero mapped to zero at that step, then applies an affine transformation. For example, 0x53 maps to 0xed. InvSubBytes uses the inverse table.',
           'S 盒先在 GF(2⁸) 中取乘法逆元（此步规定 0 映射到 0），再做仿射变换。例如 0x53 变为 0xed。解密时 InvSubBytes 使用逆 S 盒。')),
        ('ShiftRows', 'AES-ShiftRows.svg',
         t('Rotate rows left by 0, 1, 2 and 3 bytes.',
           '四行分别向左循环移动 0、1、2、3 字节。'),
         t('A byte stays in its row but can move to a different column. This lets the next column-mixing step spread its influence across columns over successive rounds. InvShiftRows rotates right by the same offsets.',
           '字节仍在原来的行，但可能换到另一列。多轮交替执行移行和混列后，一个字节的变化会扩散到其他列。InvShiftRows 向右移动相同的距离。')),
        ('MixColumns', 'AES-MixColumns.svg',
         t('Each output column combines the four bytes of one input column.',
           '每列的四个输入字节共同生成该列的四个输出字节。'),
         t('Multiply each column by the same invertible matrix in GF(2⁸), modulo x⁸+x⁴+x³+x+1. The first output byte is (02·a₀) ⊕ (03·a₁) ⊕ a₂ ⊕ a₃, with hexadecimal coefficients. The other rows are cyclic rotations of those coefficients. InvMixColumns uses the inverse matrix.',
           '每列在 GF(2⁸) 中乘同一个可逆矩阵，域的模多项式为 x⁸+x⁴+x³+x+1。首个输出字节是 (02·a₀) ⊕ (03·a₁) ⊕ a₂ ⊕ a₃，系数为十六进制；其余各行使用这些系数的循环移位。InvMixColumns 使用逆矩阵。')),
        ('AddRoundKey', 'AES-AddRoundKey.svg',
         t('XOR each state byte with the corresponding round-key byte.',
           '状态的每个字节与轮密钥中对应字节异或。'),
         t('XOR is its own inverse. The initial key addition precedes all rounds; the last round still adds a key and skips MixColumns.',
           '异或再执行一次就能还原。第一轮开始前先做一次轮密钥加；末轮仍做轮密钥加，并跳过 MixColumns。')),
    )


def mode_details(t):
    return (
        ('ecb', 'ECB', t('Electronic Codebook', '电子密码本模式'),
         t('Feed every plaintext block into AES independently under the same key.',
           '每个明文块独立送入同一把密钥下的 AES。'),
         (('ECB_encryption.svg', t('Each plaintext block connects only to its own AES box.',
                                    '每个明文块只连到自己的 AES 加密框。')),),
         'Encrypt: C[i] = E_K(P[i])\nDecrypt: P[i] = D_K(C[i])',
         (
             t('The input to the mode consists of full 16-byte blocks. Both directions can process blocks in parallel. Under one key, equal plaintext blocks give equal ciphertext blocks at any position, so repeated fields or image patterns remain recognizable.',
               '模式输入由完整的 16 字节块组成。加解密都可并行。同一密钥下，任意位置的相同明文块都会得到相同密文块，重复字段或图像轮廓会留下可识别的模式。'),
             t('The mode has no IV or authentication. An attacker can also reorder or substitute entire blocks. ECB is a useful way to recognize a single-block test vector, and unsuitable for general message encryption.',
               '该模式没有 IV 和认证，攻击者还可以重排或替换整个块。ECB 有助于理解单块测试向量，普通消息加密应避免使用。'),
         ), 'modes'),
        ('cbc', 'CBC', t('Cipher Block Chaining', '密码分组链接模式'),
         t('Mix in the previous ciphertext before encrypting the next block. The first block uses an IV.',
           '下一个明文块先与前一个密文块异或，再送入 AES。首块使用 IV。'),
         (
             ('CBC_encryption.svg', t('The diagonal arrows carry the previous ciphertext into the next plaintext XOR.',
                                      '斜线表示前一个密文块进入下一个明文块的异或运算。')),
             ('CBC_decryption.svg', t('Decrypt the current block, then XOR the previous ciphertext or the IV.',
                                      '先解密当前块，再与前一个密文块或 IV 异或。')),
         ),
         'C[0] = IV\nEncrypt: C[i] = E_K(P[i] ⊕ C[i−1])\nDecrypt: P[i] = D_K(C[i]) ⊕ C[i−1]',
         (
             t('Use a fresh unpredictable 16-byte IV. It may be public and needs integrity protection. CBC consumes full blocks. A protocol can use PKCS#7, where N padding bytes each equal N, including an entire padding block for already aligned plaintext. The padding convention belongs to the protocol.',
               '使用新鲜、不可预测的 16 字节 IV。IV 可以公开，但需要完整性保护。CBC 处理整块；协议可选 PKCS#7，补 N 字节时每个字节值都是 N，原文恰好对齐时仍补一个完整块。填充规则由协议指定。'),
             t('Encryption waits for C[i−1]. Decryption can run in parallel once the ciphertext blocks are available. Changing C[i−1] flips chosen bits of P[i], and distinguishing padding errors can create a padding oracle. Legacy protocols need an authentication design that validates the record before exposing plaintext or padding outcomes.',
               '加密须等待 C[i−1]；拿到各密文块后，解密可并行。修改 C[i−1] 可以翻转 P[i] 的指定比特，泄露填充错误还可能形成填充预言机。旧协议需要先认证记录，再向调用方暴露明文或填充结果。'),
         ), 'modes'),
        ('ctr', 'CTR', t('Counter mode', '计数器模式'),
         t('Encrypt a sequence of distinct counter blocks to obtain a keystream.',
           '加密一系列互不重复的计数器块，得到密钥流。'),
         (('CTR_encryption_2.svg', t('The image shows one possible format with a nonce prefix and a changing counter suffix.',
                                     '图示是一种计数器块格式，前缀为 Nonce，后缀计数值逐块递增。')),),
         'S[i] = E_K(T[i])\nEncrypt: C[i] = P[i] ⊕ MSB_len(P[i])(S[i])\nDecrypt: P[i] = C[i] ⊕ MSB_len(C[i])(S[i])',
         (
             t('Both sides call AES encryption. The last partial block uses only the matching prefix of the keystream. The counter layout and byte order are defined by the protocol. Independent AES calls allow parallel processing and random access when the block index is known.',
               '双方都调用 AES 加密。末尾不满一块时，只取等长的密钥流前缀。计数器布局和字节序由协议规定。各 AES 调用互相独立，已知块编号即可并行处理或随机访问。'),
             t('Every full counter block T[i] must be distinct under the same key, across all messages. Prevent overlap and wraparound. Reuse gives C ⊕ C′ = P ⊕ P′ on overlapping bytes. CTR alone also lets a ciphertext bit flip change the same plaintext bit.',
               '同一密钥下，所有消息的完整计数器块 T[i] 都必须唯一，要防止范围重叠和回绕。重复时，重叠字节满足 C ⊕ C′ = P ⊕ P′。单独使用 CTR 时，翻转密文的一位也会翻转明文对应的一位。'),
         ), 'modes'),
        ('cfb', 'CFB', t('Cipher Feedback', '密文反馈模式'),
         t('Encrypt the feedback register and feed the ciphertext back into that register.',
           '加密反馈寄存器，再把密文移入该寄存器。'),
         (('CFB_encryption.svg', t('Full-block CFB feeds each ciphertext block into the next AES call.',
                                   '图示为全块 CFB，每个密文块进入下一次 AES 调用。')),),
         'R[1] = IV                        # 128-bit register\nS[i] = MSB_s(E_K(R[i]))\nEncrypt: C[i] = P[i] ⊕ S[i]\nDecrypt: P[i] = C[i] ⊕ S[i]\nR[i+1] = LSB_(128−s)(R[i]) || C[i]',
         (
             t('The segment size s is part of the mode, for example 8 or 128 bits. CFB-128 reduces the register update to R[i+1] = C[i]. Process whole s-bit segments without block padding when the message is already segment-aligned. Use an unpredictable 16-byte IV.',
               '段长 s 是模式参数，例如 8 位或 128 位。CFB-128 的寄存器更新简化为 R[i+1] = C[i]。输入按 s 位段处理，段对齐时无需分组填充。IV 是不可预测的 16 字节值。'),
             t('Both directions use AES encryption and feed back ciphertext, even during decryption. Errors affect the current plaintext segment and can propagate while the altered ciphertext remains in the register. CFB provides confidentiality only.',
               '加解密都调用 AES 加密，解密时反馈的也仍是密文。传输错误会影响当前明文段，并可能在错误密文尚未移出寄存器时继续传播。CFB 仅提供机密性。'),
         ), 'modes'),
        ('ofb', 'OFB', t('Output Feedback', '输出反馈模式'),
         t('Feed back the AES output itself. Plaintext and ciphertext stay outside the feedback loop.',
           '把 AES 输出本身送回下一轮，明文和密文均不进入反馈链。'),
         (('OFB_encryption.svg', t('The arrows between AES calls carry keystream blocks instead of ciphertext.',
                                   'AES 框之间传递的是密钥流分组。')),),
         'O[0] = IV\nO[i] = E_K(O[i−1])\nEncrypt: C[i] = P[i] ⊕ MSB_len(P[i])(O[i])\nDecrypt: P[i] = C[i] ⊕ MSB_len(C[i])(O[i])',
         (
             t('Use a unique 16-byte IV per key, following the standard’s IV-generation requirements. Both directions use AES encryption. Like CTR, the final block can be truncated to the message length. Unlike the independent counters in CTR, OFB must generate keystream blocks sequentially.',
               '同一密钥下使用唯一的 16 字节 IV，并遵循规范的 IV 生成要求。加解密都调用 AES 加密。末块与 CTR 一样可截取等长密钥流，但 OFB 的密钥流块必须依次生成。'),
             t('Reusing an IV repeats the keystream. Flipping a ciphertext bit flips the corresponding plaintext bit without changing the next keystream block. OFB has no authentication.',
               '复用 IV 会重复密钥流。翻转密文的一位会翻转明文对应位，后续密钥流块照常生成。OFB 不提供认证。'),
         ), 'modes'),
        ('gcm', 'GCM', t('Galois/Counter Mode', '伽罗瓦／计数器模式'),
         t('CTR protects plaintext; GHASH binds the ciphertext and associated data to a tag.',
           'CTR 加密明文，GHASH 把密文和关联数据绑定到认证标签。'),
         (('GCM-Galois_Counter_Mode_with_IV.svg',
           t('Follow the counter encryption and the authentication accumulator separately. The latter consumes AAD, ciphertext and their encoded lengths.',
             '分别沿图查看计数器加密和认证累积。认证部分处理 AAD、密文以及两者编码后的长度。')),),
         'H = E_K(0^128)\nJ0 = IV || 0^31 || 1                       # 96-bit IV path\nC = GCTR_K(inc32(J0), P)                   # starts at the next counter\nX = pad128(AAD) || pad128(C) || len64(AAD) || len64(C)\nS = GHASH_H(X)\nTag = MSB_t(E_K(J0) ⊕ S)\n\nOpen: recompute and verify Tag from IV, AAD and C\n      on failure return FAIL; on success release GCTR_K(inc32(J0), C)',
         (
             t('pad128 appends only the zero bits needed to reach a block boundary. len64 encodes the original bit length as a 64-bit integer. GHASH starts at zero and updates Y ← (Y ⊕ X[i]) · H in GF(2¹²⁸) with the GCM polynomial x¹²⁸+x⁷+x²+x+1. The last pair of lengths binds the boundary between AAD and ciphertext. The AES mask on the tag uses J0, while data encryption begins at inc32(J0).',
               'pad128 只补达到分组边界所需的零比特；len64 将原始比特长度编码为 64 位整数。GHASH 从零开始，用 GCM 多项式 x¹²⁸+x⁷+x²+x+1 在 GF(2¹²⁸) 中迭代 Y ← (Y ⊕ X[i]) · H。末尾两个长度绑定 AAD 与密文的分界。Tag 的 AES 掩码用 J0，数据加密从 inc32(J0) 开始。'),
             t('inc32 increments the low 32 bits; GCTR XORs a truncated final keystream block if needed. The formula shows the usual 96-bit IV path. Other permitted IV lengths use the standard’s GHASH construction for J0, also visible in the figure. Use the protocol’s tag size and key limits, and release plaintext only after successful tag verification. IV reuse under the same key can expose plaintext relationships and enable tag forgery.',
               'inc32 递增低 32 位；GCTR 按需截取末块密钥流。公式展示常用的 96 位 IV 路径；规范允许的其他长度需用 GHASH 推导 J0，图中也画出了该分支。Tag 长度和密钥用量按协议规定，认证成功后才释放明文。同一密钥下复用 IV 会泄露明文间的关系，并可能使攻击者伪造 Tag。'),
         ), 'gcm'),
        ('xts', 'XTS', t('XEX-based Tweaked-Codebook mode with Ciphertext Stealing', '带密文窃取的 XEX 可调分组模式'),
         t('A tweak derived from the data-unit number and block index binds encryption to a storage location.',
           '由数据单元编号和块索引派生 tweak，使密文与存储位置相关。'),
         (('XTS_encryption.svg',
           t('Key₂ encrypts the data-unit number i. Multiplication by α advances the tweak; Key₁ handles the data blocks.',
             'Key₂ 加密数据单元编号 i。每乘一次 α 就前进一个块位置；Key₁ 处理数据块。')),),
         'T[0] = E_K2(Encode128(data_unit_number))\nT[j] = α^j · T[0] in the XTS field\nXEX_Encrypt(P, T) = E_K1(P ⊕ T) ⊕ T\nXEX_Decrypt(C, T) = D_K1(C ⊕ T) ⊕ T\n\nPartial tail of r bits, with last full block index j:\n  CC = XEX_Encrypt(P[j], T[j])\n  C_tail = MSB_r(CC)\n  C[j] = XEX_Encrypt(P_tail || LSB_(128−r)(CC), T[j+1])\nDecrypt the tail pair:\n  PP = XEX_Decrypt(C[j], T[j+1])\n  P_tail = MSB_r(PP)\n  P[j] = XEX_Decrypt(C_tail || LSB_(128−r)(PP), T[j])',
         (
             t('K1 and K2 are separate keys of equal size. XTS-AES-128 and XTS-AES-256 use 256 and 512 bits of combined key material respectively. T[j] multiplies by powers of α in GF(2¹²⁸); follow the XTS byte and bit representation. For aligned data units the XEX transform operates on each block independently.',
               'K1 与 K2 是两把等长、相互独立的密钥。XTS-AES-128 和 XTS-AES-256 的合计密钥材料分别为 256 位和 512 位。T[j] 在 GF(2¹²⁸) 中乘 α 的幂，字节及比特表示须遵守 XTS 约定。对齐的数据单元用 XEX 独立处理各块。'),
             t('The original image shows the full-block path. Ciphertext stealing borrows r bits from the provisional ciphertext CC for the short tail, then encrypts a full block with the next tweak. The stored data-unit length stays unchanged; follow the storage format’s ordering of the final full block and partial block. A unit needs at least one full block, and SP 800-38E caps it at 2²⁰ AES blocks.',
               '原图展示整块路径。密文窃取从临时密文 CC 中借出 r 位给短尾，再用下一个 tweak 加密拼成的整块。数据单元长度保持不变；最后的整块与短块按存储格式规定的顺序存放。一个数据单元至少包含一个整块，SP 800-38E 将其上限设为 2²⁰ 个 AES 块。'),
             t('The data-unit number is a location input and may repeat when overwriting a sector. A snapshot observer can detect unchanged data at the same location under the same key. XTS has no tag or replay protection; a storage stack requiring integrity or rollback detection needs additional mechanisms.',
               '数据单元编号是位置参数，覆盖写入同一扇区时可重复。同一位置用同一密钥时，对比快照可以识别未变的数据。XTS 没有认证标签，也不防重放；存储系统需要额外机制来保证完整性或发现回滚。'),
         ), 'xts'),
    )
