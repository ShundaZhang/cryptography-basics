"""Build a bilingual cryptography learning atlas with Python standard library."""
from pathlib import Path
from html import escape
from diagrams import diagram
from content import PAGES, NAV, SOURCES, chapter_content
ROOT = Path(__file__).parent
SITE = 'Cryptography Foundations Atlas'
REPO = 'cryptography-basics'
def pick(lang, en, zh): return zh if lang == 'zh' else en

def href(page, lang, anchor=''):
    return f'{page}{".zh" if lang == "zh" else ""}.html' + (f'#{anchor}' if anchor else '')

def cite(lang, *ids):
    return '<p class="references">' + pick(lang, 'Read the source: ', '对应资料：') + ' · '.join(f'<a href="{SOURCES[i][2]}" target="_blank" rel="noopener noreferrer">{SOURCES[i][1 if lang == "zh" else 0]} ↗</a>' for i in ids) + '</p>'

def para(*texts): return ''.join(f'<p>{t}</p>' for t in texts)

def table(headers, rows):
    return '<div class="table-wrap" tabindex="0"><table><thead><tr>' + ''.join(f'<th scope="col">{h}</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>'

def cards(items):
    return '<div class="cards">' + ''.join(f'<article class="card"><span class="eyebrow">{tag}</span><h3>{title}</h3><p>{text}</p></article>' for tag, title, text in items) + '</div>'

def callout(title, text): return f'<aside class="callout"><strong>{title}</strong><p>{text}</p></aside>'

def code(text): return '<pre><code>' + escape(text) + '</code></pre>'

def section(label, title, intro, content, ident):
    return f'<section class="chapter-section" id="{ident}"><span class="eyebrow">{label}</span><h2>{title}</h2><p class="lead">{intro}</p>{content}</section>'

def hero(lang, page, title, text, anchors=()):
    jumps = ''.join(f'<a href="#{ident}">{label}</a>' for ident, label in anchors)
    return f'<section class="page-intro"><div class="wrap"><span class="eyebrow">{NAV[lang][PAGES.index(page)]} / FIELD GUIDE</span><h1>{title}</h1><p>{text}</p><nav class="jump-links" aria-label="{pick(lang, "On this page", "本页目录")}">{jumps}</nav></div></section>'

def shell(lang, page, body):
    current = 'aria-current="page"'
    nav = ''.join(f'<a href="{href(p,lang)}" {current if p == page else ""}>{n}</a>' for p,n in zip(PAGES,NAV[lang]))
    langs = ''.join(f'<a data-atlas-lang="{l}" href="{href(page,l)}" {current if l == lang else ""}>{label}</a>' for l,label in [('en','EN'),('zh','中文')])
    title = SITE if page == 'index' else f'{NAV[lang][PAGES.index(page)]} · {SITE}'
    desc = pick(lang, 'Learn cryptographic primitives, security models, history, TLS, SPDM and applied cryptography through diagrams, primary sources and local experiments.', '通过图表、一手资料与本地实验学习密码原语、安全模型、历史、TLS、SPDM 与应用密码学。')
    scripts = '<script src="labs.js" defer></script>' if page == 'labs' else ''
    prevnext = ''
    if page != 'index':
        idx=PAGES.index(page)
        prevnext = '<nav class="chapter-pager" aria-label="' + pick(lang,'Chapters','章节') + '">'
        prevnext += f'<a href="{href(PAGES[idx-1],lang)}">← {NAV[lang][idx-1]}</a>'
        if idx < len(PAGES)-1: prevnext += f'<a href="{href(PAGES[idx+1],lang)}">{NAV[lang][idx+1]} →</a>'
        prevnext += '</nav>'
    return f'''<!doctype html>
<html lang="{'zh-CN' if lang == 'zh' else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#182638"><meta name="description" content="{desc}"><title>{escape(title)} · ShundaZhang</title><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="diagrams.css"><script src="language.js"></script>{scripts}</head>
<body><div class="topbar"><div class="wrap"><a href="https://shundazhang.github.io/">← {pick(lang,'Personal home','个人主页')}</a><nav class="languages" aria-label="{pick(lang,'Language selection','语言选择')}">{langs}</nav></div></div><a class="skip" href="#main">{pick(lang,'Skip to content','跳至正文')}</a><header><div class="wrap brand-row"><a class="brand" href="{href('index',lang)}"><span class="brand-mark">C/</span><span>{pick(lang,'CRYPTOGRAPHY FOUNDATIONS','密码学基础')}<small>LEARNING ATLAS</small></span></a><a class="repo-link" href="https://github.com/ShundaZhang/{REPO}">GitHub ↗</a></div><nav class="chapter-nav wrap" aria-label="{pick(lang,'Main navigation','主导航')}">{nav}</nav></header><main id="main">{body}{'<div class="reading wrap">'+prevnext+'</div>' if prevnext else ''}</main><footer><div class="wrap"><div><strong>{pick(lang,SITE,'密码学基础知识地图')}</strong><p>{pick(lang,'Primary-source notes for systems and security engineers','面向系统与安全工程师的一手资料导读')}</p></div><p>{pick(lang,'Reviewed 30 Sep 2026 · EN / 中文','复核于 2026 年 9 月 30 日 · EN / 中文')}</p></div></footer></body></html>'''



def overview(lang):
    t=lambda en,zh:pick(lang,en,zh)
    map_steps=[('01',t('Name the security goal','明确安全目标'),t('Confidentiality · integrity · identity · freshness','机密性 · 完整性 · 身份 · 新鲜度')),('02',t('Choose the primitive','选择密码原语'),t('AEAD · signature · MAC · KDF · CSPRNG','AEAD · 签名 · MAC · KDF · CSPRNG')),('03',t('Read the protocol','读懂协议'),t('Negotiation · transcript · key schedule · state','协商 · 转录 · 密钥派生 · 状态')),('04',t('Review the lifecycle','检查全生命周期'),t('Generate · protect · rotate · revoke · recover','生成 · 保护 · 轮换 · 撤销 · 恢复'))]
    graphic='<aside class="trust-map" aria-label="'+t('Four questions for a cryptographic design','密码设计的四个问题')+'"><div class="map-label">THE ENGINEER’S CHECKPOINTS</div>'+''.join(f'<div class="map-step"><span>{n}</span><div><strong>{title}</strong><small>{desc}</small></div></div>' for n,title,desc in map_steps)+'<div class="map-foot">'+t('A good algorithm still needs a well-defined use','好算法仍需要明确的使用方式')+'</div></aside>'
    body='<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">CRYPTOGRAPHY / FIELD GUIDE</span><h1>'+t('Understand the primitives<br><em>Reason about systems</em>','理解密码原语<br><em>看懂系统设计</em>')+'</h1><p>'+t('A learning map for engineers who know computers and want a coherent view of cryptography: from keys and security games to TLS, SPDM and post-quantum migration.','面向熟悉计算机系统的工程师：从密钥与安全游戏，到 TLS、SPDM 和抗量子迁移，建立完整的密码学视野。')+'</p><div class="hero-actions"><a class="button" href="'+href('foundations',lang)+'">'+t('Start with foundations →','从基础概念开始 →')+'</a><a class="text-link" href="'+href('labs',lang)+'">'+t('Try the local labs ↗','动手做本地实验 ↗')+'</a></div><div class="hero-meta">14 CHAPTERS / 10 DIAGRAMS / 4 INTERACTIVE LABS<br>'+t('ENGLISH & 中文 · PRIMARY SOURCES · NO ACCOUNT REQUIRED','中英双语 · 一手资料 · 无需账号')+'</div></div>'+graphic+'</div></section><div class="reading wrap">'
    routes=[('01',t('Get oriented in a few evenings','用几个晚上的时间入门'),t('Read Foundations, Symmetric, Public key, Hash / MAC / KDF and Randomness. Run the four labs. You should be able to explain what encryption, authentication and freshness each guarantee.','阅读基础、对称密码、公钥、Hash / MAC / KDF 和随机数，完成四个实验。目标是能分别解释加密、认证和新鲜度的保证。')),('02',t('Read real systems next','接着读实际系统'),t('Choose TLS or SPDM according to your work. Trace key establishment, identity verification, transcript binding and failure paths. Then read Applied crypto and review a small design.','按工作需要选择 TLS 或 SPDM，追踪密钥建立、身份验证、转录绑定与失败路径。再读应用密码学，评审一个小型设计。')),('03',t('Build depth over four to six weeks','用四到六周建立深度'),t('Add Theory and History, work through selected textbook sections, and study Future. This is a suggested pace, not a prerequisite chain: every topic has its own entry point.','加入理论与历史，研读选定教材章节，再看未来方向。进度仅供参考；每个方向都可独立进入。'))]
    body+=section('01 / ROUTE',t('A route with useful stopping points','有明确收获的学习路径'),t('Assumed background: basic programming, binary data and a working understanding of computer systems. Learn the mathematical tools as they arise.','预备知识：基础编程、二进制数据与计算机系统常识；数学工具可随内容补充。'),'<div class="sequence">'+''.join(f'<article><span>{n}</span><div><h3>{title}</h3><p>{desc}</p></div></article>' for n,title,desc in routes)+'</div>'+callout(t('What you should be able to review','最终能评审什么'),t('Which property is required? Who holds each key? Where does entropy come from? Which bytes are authenticated? How is replay rejected? What happens after compromise or restart?','需要什么安全属性？谁持有哪些密钥？熵从哪里来？哪些字节被认证？怎样拒绝重放？泄漏或重启后会发生什么？')),'route')
    descs=[t('Goals, parameters and byte conventions','目标、参数和字节约定'),t('AES, stream ciphers, AEAD and nonce rules','AES、流密码、AEAD 与 Nonce 规则'),t('RSA, DH, ECC, signatures and public-key trust','RSA、DH、ECC、签名与公钥信任'),t('Digest properties, HMAC, HKDF and password storage','摘要性质、HMAC、HKDF 与口令存储'),t('Entropy, DRBGs and OS interfaces','熵、DRBG 与操作系统接口'),t('Algebra, security games and reductions','代数、安全游戏与归约'),t('The ideas and failures that shaped the field','塑造密码学的思想与失败'),t('TLS 1.3 handshake, keys and authentication','TLS 1.3 握手、密钥与认证'),t('Device identity, measurements and sessions','设备身份、度量与会话'),t('Envelope encryption, libraries and key lifecycle','信封加密、密码库与密钥生命周期'),t('PQC migration, ZK, MPC and FHE','抗量子迁移、ZK、MPC 与 FHE'),t('Observe crypto through four browser experiments','通过四个浏览器实验观察密码行为'),t('Books, videos, standards and implementations','教材、视频、规范与实现')]
    grid='<div class="topic-grid">'+''.join(f'<a class="topic-card" href="{href(page,lang)}"><span class="eyebrow">{i:02} / FIELD NOTES</span><h3>{NAV[lang][i]}</h3><p>{desc}</p></a>' for i,(page,desc) in enumerate(zip(PAGES[1:],descs),1))+'</div>'
    body+=section('02 / CHAPTERS',t('Choose a question to investigate','选择一个问题开始探索'),t('Each chapter combines an explanation, practical limits and links to the original source.','每章结合原理解释、实际限制与原始资料链接。'),grid,'chapters')
    body+=section('03 / READING',t('Read explanation before specification','先读解释，再查规范'),t('Use a textbook for reasoning, the standard for exact behavior, and an implementation for the engineering boundary.','用教材学习推理，用规范查准确行为，用实现检查工程边界。'),cards([('TEXTBOOK',t('Boneh–Shoup','Boneh–Shoup'),t('Start with encryption, message integrity and authenticated encryption. Follow the probability appendix when a proof needs it.','先读加密、消息完整性和认证加密，需要时再补概率附录。')),('VIDEO',t('Dan Boneh’s lectures','Dan Boneh 课程'),t('The Stanford course page links lectures and slides. Slides are openly available; the external course platform may require an account.','Stanford 课程页提供视频与讲义；讲义可公开阅读，外部课程平台可能需账号。'))])+cite(lang,'book','video'),'reading')
    return body+'</div>'

def labs(lang):
    t=lambda en,zh:pick(lang,en,zh)
    body=hero(lang,'labs',t('Observe the property<br><em>Test the failure</em>','观察安全属性<br><em>验证失败条件</em>'),t('Four local browser experiments using the Web Cryptography API. Inputs and transient keys stay in this page; no experiment data is uploaded or saved. HTTPS or localhost is required.','四个使用 Web Cryptography API 的本地浏览器实验。输入和临时密钥留在当前页面，不上传或保存实验数据；需要 HTTPS 或 localhost。'),[('hash',t('Hash','Hash')),('aead','AEAD'),('signature',t('Signatures','签名')),('nonce',t('Nonce reuse','Nonce 复用'))])+'<div class="reading wrap">'
    def field(ident,label,value):return f'<label class="lab-field" for="{ident}">{label}<input id="{ident}" value="{escape(value,quote=True)}" maxlength="160" autocomplete="off"></label>'
    def btn(action,label):return f'<button type="button" data-action="{action}">{label}</button>'
    def box(ident,fields,buttons):return f'<div class="lab-box" data-lab="{ident}">{fields}<div class="lab-actions">{buttons}</div><p class="lab-state" data-pass="info" id="{ident}-state" role="status" aria-live="polite">'+t('Ready — choose an experiment','就绪 — 选择实验')+f'</p><div class="lab-output" id="{ident}-output" aria-label="'+t('Experiment output','实验输出')+'"></div></div>'
    body+='<noscript><aside class="callout">'+t('Enable JavaScript for interactive experiments. All chapter notes, diagrams and the downloadable Python exercise remain readable without it.','开启 JavaScript 才能使用交互实验。章节、图表及可下载 Python 练习仍可阅读。')+'</aside></noscript>'
    body+=section('01 / DIGEST',t('Change one input, compare two digests','改变输入，比较两个摘要'),t('Hash is deterministic. A changed digest is not proof of who authored the data.','Hash 是确定性的；摘要发生变化不证明谁创建了数据。'),box('hash',field('hash-text',t('UTF-8 input','UTF-8 输入'),'hello'),btn('hash-compare',t('Hash input and input + !','计算输入及输入 + ! 的 Hash')))+para(t('The experiment compares SHA-256 digests and counts changed output bits. Around half is a typical observation, not a promise for every pair or a security proof. The input “hello” also provides a known-answer check.','实验比较 SHA-256 摘要并统计改变的输出位数。约一半是常见现象，而非每一对输入的保证或安全证明。“hello” 同时提供已知答案检查。'))+cite(lang,'sha2','webcrypto'),'hash')
    body+=section('02 / AEAD',t('Decrypt only after authenticating','认证成功后才释放明文'),t('AES-GCM authenticates the ciphertext and AAD. It does not keep replay history for the application.','AES-GCM 认证密文和 AAD，但不替应用记录重放历史。'),box('aead',field('aead-text',t('Plaintext','明文'),'transfer=10')+field('aead-aad',t('Visible authenticated context / AAD','可见认证上下文 / AAD'),'account=demo;version=1'),btn('aead-seal',t('Create a fresh record','创建新记录'))+btn('aead-valid',t('Open valid record','打开有效记录'))+btn('aead-tamper',t('Flip ciphertext bit','翻转密文位'))+btn('aead-context',t('Change AAD','改变 AAD'))+btn('aead-replay',t('Open same record twice','打开同一记录两次')))+para(t('Each new record uses a newly generated key and random 96-bit nonce in this small exercise. Later actions use that sealed record; editing the input fields takes effect when you create another record. A real system needs per-key nonce limits, persistent uniqueness and protocol replay handling.','每条新记录在本小实验中使用新生成的密钥和随机 96 位 Nonce。后续操作针对已密封记录；编辑输入后须创建新记录。实际系统需要密钥使用上限、持续唯一的 Nonce 和协议重放处理。'))+cite(lang,'gcm','webcrypto'),'aead')
    body+=section('03 / SIGNATURE',t('A signature binds bytes to a key','签名把字节绑定到密钥'),t('A mathematical signature check does not establish whether the key belongs to a trusted identity.','数学验签不确定密钥是否属于可信身份。'),box('signature',field('signature-text',t('Message to sign','待签消息'),'release=v1;digest=example'),btn('signature-create',t('Create key and signature','创建密钥及签名'))+btn('signature-valid',t('Verify original','验证原文'))+btn('signature-message',t('Verify changed message','验证修改后消息'))+btn('signature-key',t('Verify with another key','用另一公钥验证')))+para(t('The browser generates a transient ECDSA P-256 key pair and signs using SHA-256. Only the public key and signature bytes are displayed; the private key is non-extractable and discarded when the page closes. This demo does not create a certificate or assert a person’s identity.','浏览器生成临时 ECDSA P-256 密钥对并配合 SHA-256 签名。仅展示公钥与签名字节；私钥不可导出，关闭页面后丢弃。本实验不创建证书，也不声明人的身份。'))+cite(lang,'webcrypto','book'),'signature')
    body+=section('04 / MISUSE',t('Repeated nonce, repeated keystream','Nonce 重复，密钥流重复'),t('An intentional local misuse experiment with two short synthetic messages.','用两条短示例消息故意展示一次本地误用。'),box('nonce',field('nonce-first',t('Message 1','消息 1'),'pay=100;to=alice')+field('nonce-second',t('Message 2','消息 2'),'pay=900;to=bobby'),btn('nonce-reuse',t('Reuse key + nonce','复用 key + nonce'))+btn('nonce-fresh',t('Use distinct nonces','使用不同 Nonce')))+para(t('For the overlapping message length, repeated AES-GCM key/nonce exposes C₁ XOR C₂ = P₁ XOR P₂ because the CTR keystream repeats. The last 16 bytes (authentication tag) are excluded from this comparison. This reveals a relationship between plaintexts; it is not a complete GCM forgery demonstration. Never use this setup for real data.','在两条消息重叠长度内，AES-GCM 重复 key/nonce 导致 CTR 密钥流重复，暴露 C₁ XOR C₂ = P₁ XOR P₂。比较时排除最后 16 字节认证 Tag。这展示明文间关系，并非完整 GCM 伪造实验。勿用于真实数据。'))+cite(lang,'gcm'),'nonce')
    body+=section('05 / NEXT STEPS',t('Make the checks reproducible','让检查可以复现'),t('Repeat basic byte, HMAC and key-derivation checks outside the browser.','在浏览器外重复字节、HMAC 和密钥派生检查。'),'<p class="download"><a href="labs/core_examples.py" download>'+t('Download the Python standard-library exercise ↓','下载 Python 标准库练习 ↓')+'</a></p>'+code('python3 core_examples.py')+para(t('Includes an RFC 5869 HKDF known-answer test, HMAC tamper rejection, random-byte generation and a small Diffie–Hellman arithmetic example. The tiny DH group is for arithmetic only and is insecure for deployment. No hand-written cipher is presented as production code.','包含 RFC 5869 HKDF 已知答案测试、HMAC 篡改拒绝、随机字节生成及小型 DH 算术示例。小 DH 群仅用于算术学习，部署不安全。'))+cite(lang,'secrets','hkdf','hmac'),'next')
    return body+'</div>'

def sources(lang):
    t=lambda en,zh:pick(lang,en,zh)
    body=hero(lang,'sources',t('Read for understanding<br><em>Verify against the source</em>','阅读帮助理解<br><em>回到原始资料核对</em>'),t('A question-oriented shelf of textbooks, lecture material, published specifications and implementations. Publication categories are explicit; an informational RFC is not automatically a Standards Track standard.','按问题整理教材、课程、已发布规范与实现。明确标注资料类别；Informational RFC 不自动等同于 Standards Track 标准。'))+'<div class="reading wrap">'
    groups=[('learn',t('Explanation and historical context','解释与历史背景'),t('Boneh–Shoup is the main reasoning text. Use HAC for reference and history; its older deployment advice and parameters need modern verification.','以 Boneh–Shoup 为主要推理教材；HAC 用作参考和历史资料，其中旧部署建议与参数须按现代资料核对。'),['book','video','hac','dh-paper','rsa-paper']),('primitives',t('Exact primitive behavior','密码原语的准确行为'),t('Read input formats, parameter restrictions, security considerations and test vectors before using the API.','使用接口前阅读输入格式、参数限制、安全注意事项与测试向量。'),['aes','gcm','chacha','rsa','x25519','eddsa','sha2','sha3','hmac','hkdf','argon']),('entropy',t('Randomness and key lifecycle','随机数与密钥生命周期'),t('The 90 series separates entropy sources, DRBG mechanisms and complete constructions. Read API guarantees separately.','90 系列区分熵源、DRBG 机制与完整构造，另行阅读接口保证。'),['90a','90b','90c','secrets','keymgmt']),('protocols',t('Protocol state and authenticated transcripts','协议状态与认证转录'),t('TLS 1.3 and SPDM are the main walkthroughs. SSH is linked for architecture; its original algorithm lists are historical, not current recommendations.','TLS 1.3 与 SPDM 是主要导读；SSH 用于理解架构，其初始算法列表属于历史背景，不作为当前推荐。'),['tls','hybrid','hpke','ssh','noise','spdm','spdm-pdf','spdm-hub','libspdm']),('implementation',t('Supported implementation interfaces','受支持的实现接口'),t('Check the documentation matching your library and browser version; platform availability is not a security proof.','查阅与你的库及浏览器版本一致的文档；平台可用不等于已证明安全。'),['library','webcrypto']),('future',t('Post-quantum standards and status','抗量子标准与状态'),t('ML-KEM is key establishment; ML-DSA and SLH-DSA are signatures. Check the NIST project for later changes and errata.','ML-KEM 用于密钥建立；ML-DSA 与 SLH-DSA 用于签名。后续变化与勘误查 NIST 项目。'),['mlkem','mldsa','slhdsa','pqc'])]
    for n,(ident,title,intro,ids) in enumerate(groups,1):
        grid='<div class="source-grid">'+''.join(f'<a class="source-card" href="{SOURCES[i][2]}" target="_blank" rel="noopener noreferrer"><span class="eyebrow">{SOURCES[i][3]}</span><h3>{SOURCES[i][1 if lang=="zh" else 0]} ↗</h3></a>' for i in ids)+'</div>'
        body+=section(f'{n:02} / PRIMARY SOURCES',title,intro,grid,ident)
    return body+'</div>'


if __name__ == '__main__':
    for page in PAGES:
        for lang in ('en', 'zh'):
            if page == 'index': body = overview(lang)
            elif page == 'labs': body = labs(lang)
            elif page == 'sources': body = sources(lang)
            else:
                info, parts = chapter_content(page, lang)
                body = hero(lang,page,info[0],info[1],[(p[4],p[1]) for p in parts]) + '<div class="reading wrap">'
                for label,title,intro,body_text,ident,figure,refs in parts:
                    body += section(label,title,intro,(diagram(figure,lang) if figure else '') + body_text + cite(lang,*refs),ident)
                body += '</div>'
            (ROOT / href(page,lang)).write_text(shell(lang,page,body),encoding='utf-8')
    print(f'Built {len(PAGES)*2} bilingual pages')
