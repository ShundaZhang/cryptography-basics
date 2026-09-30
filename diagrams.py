"""Local, responsive diagrams with text labels and primary-source captions."""
from diagram_core import tr, node, arrow, flow, frame
from content import SOURCES

def exchange(lang,left,right,rows):
    t=lambda en,zh:tr(lang,en,zh)
    body='<div class="viz-scroll-hint">'+t('Read top to bottom · Each arrow is one message or flight','从上到下阅读 · 每个箭头表示一条消息或一组报文')+'</div><div class="viz-exchange"><div class="viz-two">'+node(left,tone='protected')+node(right,tone='neutral')+'</div>'
    for i,(direction,label) in enumerate(rows,1):
        body+=f'<div class="viz-packet {direction}"><div class="viz-packet-label"><span class="viz-step">{i:02}</span>{label}</div></div>'
    return body+'</div>'

def diagram(name,lang):
    t=lambda en,zh:tr(lang,en,zh)
    if name=='primitive-map':
        title=t('Match each security goal to its building blocks','让安全目标对应密码积木')
        body='<div class="viz-two">'+node(t('Hide contents','隐藏内容'),'AEAD', 'protected')+node(t('Check shared-key origin','检查共享密钥来源'),'MAC / AEAD','protected')+node(t('Public verification','公开验证'),t('Signature + authenticated public key','签名 + 经过认证的公钥'),'neutral')+node(t('Establish a secret','建立秘密'),'DH / KEM → KDF','neutral')+'</div>'
        body+=arrow(t('A protocol adds identities, context and state','协议加入身份、上下文与状态'),'down')+node(t('Application decision','应用决策'),t('Authorization · replay protection · key lifecycle','授权 · 防重放 · 密钥生命周期'),'neutral')
        caption=t('Hash and encoding are supporting tools. A successful primitive operation does not settle identity or authorization.','Hash 和编码是辅助工具。原语操作成功并不决定身份或授权。');src='book'
    elif name=='aead':
        title=t('Keep the visible header authenticated','让可见 Header 也经过认证')
        body='<div class="viz-two">'+node(t('Secret key + unique nonce','秘密密钥 + 唯一 Nonce'),t('Sender and receiver follow the same construction','发送方和接收方使用相同构造'),'protected')+node(t('Plaintext + associated data','明文 + 关联数据'),t('AAD may contain version, tenant or sequence','AAD 可包含版本、租户或序号'))+'</div>'
        body+=arrow('Seal','down')+node(t('Nonce + ciphertext + tag + visible AAD','Nonce + 密文 + Tag + 可见 AAD'),t('Send an unambiguous record','发送无歧义记录'),'neutral')+arrow('Open','down')
        body+='<div class="viz-two">'+node(t('Authentication succeeds → plaintext','认证成功 → 明文'),t('Application checks context and replay state','应用检查上下文和重放状态'),'protected')+node(t('Authentication fails → reject','认证失败 → 拒绝'),t('Do not use unauthenticated plaintext','不使用未经认证的明文'),'outside')+'</div>'
        caption=t('AAD is authenticated but not encrypted. Nonce/tag requirements and key-usage bounds belong to the chosen mode.','AAD 被认证，但未被加密。Nonce / Tag 要求及密钥使用上限由所选模式规定。');src='gcm'
    elif name=='public-roles':
        title=t('Encryption and signing reverse the key roles','加密与签名使用不同的密钥角色')
        body='<div class="viz-lane"><span class="viz-lane-label">'+t('CONFIDENTIALITY','机密性')+'</span>'+flow([node(t('Sender','发送方'),t('Recipient public encryption key','接收者加密公钥')),arrow(t('Encrypt','加密')),node(t('Ciphertext','密文')),arrow(t('Decrypt','解密')),node(t('Recipient','接收者'),t('Recipient private key','接收者私钥'),'protected')])+'</div>'
        body+='<div class="viz-lane"><span class="viz-lane-label">'+t('PUBLIC AUTHENTICITY','公开验证真实性')+'</span>'+flow([node(t('Signer','签名者'),t('Signer private key','签名者私钥'),'protected'),arrow(t('Sign','签名')),node(t('Message + signature','消息 + 签名')),arrow(t('Verify','验证')),node(t('Verifier','验证方'),t('Authenticated signer public key','经过认证的签名者公钥'),'neutral')])+'</div>'
        caption=t('A signature does not hide the message. KEM/DH establish keying material and are a third operation.','签名不隐藏消息。KEM/DH 建立密钥材料，是第三种操作。');src='rsa'
    elif name=='hash-mac-kdf':
        title=t('Similar-looking outputs, different contracts','输出看起来相似，安全要求不同')
        body='<div class="viz-lane">'+flow([node(t('Message','消息')),arrow('Hash'),node(t('Public digest','公开摘要'),t('No secret → no source authentication','没有秘密 → 不认证来源'),'neutral')])+'</div>'
        body+='<div class="viz-lane">'+flow([node(t('Secret key + encoded message','秘密密钥 + 编码消息'),'','protected'),arrow('HMAC'),node(t('Authentication tag','认证 Tag'),t('Any key holder can generate it','任意密钥持有者均可生成'),'protected')])+'</div>'
        body+='<div class="viz-lane">'+flow([node(t('Keying material + salt + labels','密钥材料 + Salt + 标签')),arrow('HKDF'),node(t('Separate usage keys','独立用途密钥'),t('Encryption / authentication / direction','加密 / 认证 / 方向'),'protected')])+'</div>'
        caption=t('HMAC authenticates using a shared secret; HKDF derives keys. Neither a fast hash nor HKDF is a password-hardening substitute.','HMAC 用共享秘密认证，HKDF 派生密钥。快速 Hash 和 HKDF 均不能代替口令强化。');src='hkdf'
    elif name=='random-pipeline':
        title=t('Protect the seed and the evolving state','保护种子与演化状态')
        body=flow([node(t('Noise + health tests','噪声 + 健康测试'),'SP 800-90B','neutral'),arrow(t('Condition / seed','调理 / 播种')),node('DRBG','SP 800-90A','protected'),arrow(t('State update + output','状态更新 + 输出')),node(t('Keys / tokens / samples','密钥 / Token / 样本'),'OS CSPRNG API','protected')])
        body+='<div class="viz-strip">'+t('SP 800-90C specifies constructions combining entropy sources and DRBGs; reseed and state protection depend on the construction','SP 800-90C 规定熵源与 DRBG 的组合构造；重播种和状态保护取决于构造')+'</div>'
        caption=t('A simplified trust path, not an entropy-source certification diagram. A long deterministic output cannot repair a guessable seed.','简化信任路径，并非熵源认证图。长的确定性输出无法修复可猜测种子。');src='90c'
    elif name=='security-game':
        title=t('An indistinguishability game makes the claim precise','不可区分性游戏让安全声明变精确')
        body=flow([node(t('Adversary chooses m₀, m₁','攻击者选择 m₀、m₁'),t('Equal length; allowed oracle queries','等长；允许的 Oracle 查询'),'outside'),arrow(t('Submit pair','提交消息对')),node(t('Challenger chooses b ∈ {0,1}','挑战者选择 b ∈ {0,1}'),t('Return Enc(k,m_b)','返回 Enc(k,m_b)'),'neutral'),arrow(t('Ciphertext','密文')),node(t('Adversary guesses b′','攻击者猜测 b′'),t('Measure advantage over a random guess','衡量超过随机猜测的优势'),'outside')])
        caption=t('IND-CPA sketch. IND-CCA adds a restricted decryption oracle. Length leakage and implementation side channels need their own model.','IND-CPA 草图。IND-CCA 增加受限制解密 Oracle。长度泄漏与实现侧信道需要各自建模。');src='book'
    elif name=='tls-flow':
        title=t('TLS 1.3 binds the shared secret to an authenticated transcript','TLS 1.3 把共享秘密绑定到经过认证的转录')
        body=exchange(lang,t('Client','客户端'),t('Server','服务端'),[
            ('right','ClientHello · '+t('versions / groups / key share','版本 / 群 / 密钥份额')),
            ('left','ServerHello · '+t('selection / key share → handshake keys','选择 / 密钥份额 → 握手密钥')),
            ('left',t('Encrypted: EncryptedExtensions, Certificate, CertificateVerify, Finished','加密报文：EncryptedExtensions、Certificate、CertificateVerify、Finished')),
            ('right','Finished · '+t('after chain, service-name and transcript checks','在证书链、服务名及转录检查之后')),
            ('both',t('Application records: directional AEAD traffic keys','应用记录：按方向分离的 AEAD 流量密钥')),
        ])
        caption=t('Common certificate-based server-authenticated path; optional client authentication, PSK, early data and retry are omitted. ServerHello is not encrypted.','常见证书模式的服务端认证路径；省略可选客户端认证、PSK、早期数据和重试。ServerHello 未加密。');src='tls'
    elif name=='spdm-flow':
        title=t('SPDM separates negotiated capability from approval','SPDM 分离协商能力与状态批准')
        body=exchange(lang,'Requester','Responder',[
            ('right','GET_VERSION / GET_CAPABILITIES / NEGOTIATE_ALGORITHMS'),
            ('left',t('Responses: versions, capabilities and algorithm selection','响应：版本、能力与算法选择')),
            ('right','GET_DIGESTS / GET_CERTIFICATE / CHALLENGE'),
            ('left',t('Identity material + authenticated challenge response','身份材料 + 经过认证的挑战响应')),
            ('right',t('GET_MEASUREMENTS · request authenticated/fresh evidence','GET_MEASUREMENTS · 请求经过认证且新鲜的证据')),
            ('left',t('Measurement response → reference-value appraisal','度量响应 → 参考值评估')),
            ('both',t('Optional secure session: KEY_EXCHANGE / FINISH + secured messages','可选安全会话：KEY_EXCHANGE / FINISH + 安全消息')),
        ])
        caption=t('Illustrative certificate path, not a mandatory universal ordering. Negotiated capabilities, authentication mode and secured-message bindings define allowed flows.','证书模式示意，并非统一强制顺序。协商能力、认证模式及安全消息 Binding 定义允许路径。');src='spdm-pdf'
    elif name=='envelope':
        title=t('Keep the bulk-data key separate from the wrapping key','分离数据密钥与包裹密钥')
        body='<div class="viz-two">'+node('DEK',t('Random per-object data key','每对象随机数据密钥'),'protected')+node('KEK / recipient key',t('KMS/HSM or defined key-wrapping scheme','KMS/HSM 或规定的密钥包裹方案'),'protected')+'</div>'
        body+=arrow(t('Encrypt object + protect DEK','加密对象 + 保护 DEK'),'down')+node(t('Stored envelope','存储的信封'),t('Version / algorithm / nonce / AAD / ciphertext / tag / wrapped DEK','版本 / 算法 / Nonce / AAD / 密文 / Tag / 包裹 DEK'),'neutral')
        body+=arrow(t('Authorize → unwrap DEK → authenticate/decrypt','授权 → 解包 DEK → 认证 / 解密'),'down')+node(t('Authorized consumer','获授权接收者'),t('Receives plaintext within the designed boundary','在设计边界内接收明文'),'protected')
        caption=t('KEK rewrapping differs from re-encrypting data after DEK compromise. Bind tenant and object metadata; key-service authorization remains essential.','重新包裹 KEK 与 DEK 泄漏后重新加密数据不同。应绑定租户及对象元数据；密钥服务授权仍必需。');src='keymgmt'
    elif name=='kem':
        title=t('A KEM yields a secret, then AEAD protects the message','KEM 产生秘密，再由 AEAD 保护消息')
        body=flow([node(t('Recipient key pair','接收者密钥对'),t('Publish encapsulation key; protect decapsulation key','公布封装公钥；保护解封装私钥'),'protected'),arrow(t('Encapsulate','封装')),node(t('Sender gets ciphertext c + secret z','发送者获得密文 c + 秘密 z'),'ML-KEM','neutral'),arrow(t('Send c; recipient decapsulates','发送 c；接收者解封装')),node(t('Recipient recovers z','接收者恢复 z'),t('According to the KEM’s validity behavior','按 KEM 的有效性行为处理'),'protected')])
        body+=arrow('z → KDF → AEAD','down')+node(t('A defined encryption protocol','定义好的加密协议'),t('Add identity, context and replay rules separately','另行加入身份、上下文和重放规则'),'neutral')
        caption=t('KEM ciphertext transports keying material, not application plaintext. A KEM alone does not authenticate the sender.','KEM 密文传递密钥材料，不是应用明文。KEM 本身不认证发送者。');src='mlkem'
    else:raise ValueError(name)
    return frame(lang,name+'-diagram',title,body,caption,SOURCES[src][2],SOURCES[src][0 if lang=='en' else 1])
