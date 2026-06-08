import sys, time, random
import requests
import os
import re
import ast
import base64
import zlib
import hashlib
import hmac
import binascii
import textwrap
import marshal
import struct
import json
import time as _time_mod

# حاول استيراد المكتبات الخارجية، إذا لم تكن موجودة لن يتوقف السكربت فوراً لكن سيحتاجها لاحقاً
try:
    import python_minifier
except ImportError:
    python_minifier = None

# ================== قفل GitHub + واجهة النسر ==================

CHECK_URL   = "https://raw.githubusercontent.com/waelhadi/Nasrn1/refs/heads/main/Nasrp2"
TIMEOUT     = 5
COUNT_START = 10
COUNT_DELAY = 0.6
WIDTH       = 86

RST = "\033[0m"; B = "\033[1m"; DIM = "\033[2m"
RED = "\033[31m"; YLW = "\033[33m"; CYN = "\033[36m"; MAG = "\033[35m"
GRN = "\033[32m"; BLU = "\033[34m"; WHT = "\033[37m"
BLK = "\033[30m"; BGK = "\033[40m"; BGW = "\033[47m"
CSI = "\033["

def cls():         print(CSI + "2J" + CSI + "H", end="", flush=True)
def home():        print(CSI + "H", end="", flush=True)
def hide_cursor(): print(CSI + "?25l", end="", flush=True)
def show_cursor(): print(CSI + "?25h", end="", flush=True)

def visible_len(s):
    import re
    return len(re.sub(r"\x1b\[[0-9;]*m", "", s))

def center_lines(block, width=WIDTH):
    out = []
    for ln in block.splitlines():
        ln = ln.rstrip("\n")
        pad = max(0, (width - visible_len(ln)) // 2)
        out.append(" " * pad + ln)
    return "\n".join(out)

def type_line(text, delay=0.0015):
    for ch in text:
        print(ch, end="", flush=True); time.sleep(delay)
    print()

def render_logo():
    try:
        import pyfiglet
        logo = pyfiglet.figlet_format("NASR", font="slant")
        return "\n".join(RED + B + ln + RST for ln in logo.rstrip("\n").split("\n"))
    except Exception:
        ascii_logo = [
            r" _   _    ___    ____   ____ ",
            r"| \ | |  / _ \  / ___| / ___|",
            r"|  \| | | | | | \___ \ \___ \ ",
            r"| |\  | | |_| |  ___) | ___) |",
            r"|_| \_|  \___/  |____/ |____/ ",
        ]
        return "\n".join(RED + B + ln + RST for ln in ascii_logo)

def pulse_title(msg, pulses=3):
    blk_r = center_lines(f"{B}{RED}{msg}{RST}")
    blk_y = center_lines(f"{B}{YLW}{msg}{RST}")
    for _ in range(pulses):
        home(); print(blk_r, end="", flush=True); time.sleep(0.18)
        home(); print(blk_y, end="", flush=True); time.sleep(0.18)

def flash(block, flashes=2):
    for _ in range(flashes):
        home(); print(BGK + BLK + block + RST, end="", flush=True); time.sleep(0.08)
        home(); print(BGW + BLK + block + RST, end="", flush=True); time.sleep(0.06)
        home(); print(BGK + BLK + block + RST, end="", flush=True); time.sleep(0.06)

def drip_line(width=58):
    n = random.randint(width-8, width)
    return RED + "🩸" * n + RST

def check_connection():
    try:
        r = requests.get(CHECK_URL, timeout=TIMEOUT)
        return r.status_code == 200
    except requests.RequestException:
        return False

def countdown(start=COUNT_START, delay=COUNT_DELAY):
    palette = [RED, YLW, GRN, CYN, BLU, MAG, WHT]
    try:
        import pyfiglet
        big = True
    except Exception:
        big = False

    for i in range(start, -1, -1):
        color = palette[i % len(palette)]
        cls()
        num_str = str(i)

        if big:
            import pyfiglet
            art = pyfiglet.figlet_format(num_str, font="slant")
            block = color + B + art + RST
        else:
            block = f"""
{color}{B}
       ╔══════════╗
          {num_str.center(6)}
       ╚══════════╝
{RST}
""".rstrip("\n")

        print(center_lines(block))
        print(center_lines(DIM + "Preparing cinematic lock..." + RST))
        print("\a", end="", flush=True)
        time.sleep(delay)

def nasser_lock():
    try:
        hide_cursor()
        countdown()
        cls()
        title = "النــــــــــســــــــــر 🦅 أوقــــــف الأداة"
        pulse_title(title, pulses=3)
        logo = center_lines(render_logo())
        flash(logo, flashes=2)
        body = [
            "",
            center_lines(f"{B}{RED}🔒 لا يمكنك تشغيل هذه الأداة حالياً.{RST}"),
            center_lines(f"{B}{YLW}📧 تواصل مع المطوّر: @NASR101{RST}"),
            center_lines(f"{B}{CYN}⚠️ أي محاولة لعب بالتشفير تعرّضك للخطر.{RST}"),
            "",
            center_lines(drip_line(), width=WIDTH),
        ]
        for ln in body:
            type_line(ln, delay=0.0012)
            time.sleep(0.02)
        print("\a", end="", flush=True)
        time.sleep(1.0)
    finally:
        show_cursor()
    sys.exit(1)

# ================== من هنا يبدأ نظام التشفير NASR ==================

RESET = "\033[0m"
COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}

def colorize(text: str, c: str) -> str:
    return f"{COLORS.get(c, '')}{text}{RESET}"

LOGO_TEXT = r"""
███╗   ██╗ █████╗ ███████╗██████╗ 
███║   ██║██╔══██╗██╔════╝██╔══██╗
████╗  ██║███████║███████╗██████╔╝
██╔██╗ ██║██╔══██║╚════██║██╔══██╗
██║╚██╗██║██║  ██║███████║██║  ██║
╚═╝ ╚═╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

   NASR Telegram-ID @NASR101
"""

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# ================== شريط انتظار NASR ==================

def wait_bar(total_seconds: int = 20):
    clear_screen()
    print(colorize(LOGO_TEXT, "green"))
    print()
    msg = "🦅 من فضلك انتظر حتى ينتهي تجهيز التشفير بتقنية النسر..."
    print(colorize(msg, "cyan"))
    print()

    bar_len = 40
    for sec in range(total_seconds + 1):
        progress = sec / total_seconds if total_seconds > 0 else 1.0
        if progress < 0: progress = 0
        if progress > 1: progress = 1
        filled = int(bar_len * progress)
        bar = "█" * filled + "-" * (bar_len - filled)
        remaining = total_seconds - sec
        mins = remaining // 60
        rems = remaining % 60
        time_str = f"{mins:02d}:{rems:02d}"
        line = f"{CYN}[{bar}]{RST} {WHT}{int(progress*100):3d}% {time_str}{RST}"
        sys.stdout.write("\r" + line)
        sys.stdout.flush()
        time.sleep(1)
    print()

# ================== إعدادات OBF V3 ==================

NO_COMMENTS     = os.environ.get("NO_COMMENTS", "1") == "1"
KEEP_DOCSTRINGS = os.environ.get("KEEP_DOCSTRINGS", "0") == "1"
NASR_MINIFY     = os.environ.get("NASR_MINIFY", "0") == "1"
NASR_NUMBERS    = os.environ.get("NASR_NUMBERS", "1") == "1"

_BANNER_RE = re.compile(
    r'^\s*(?:#![^\n]*\n)?'
    r'(?:#.*coding[:=].*\n)?'
    r'(?:[ \t]*(\"\"\"|\'\'\')(.|\n)*?\1[ \t]*\n)?',
    re.M
)

def strip_top_banner_and_comments(text: str) -> str:
    text = _BANNER_RE.sub('', text, count=1)
    if not NO_COMMENTS:
        return text
    text = re.sub(r'(?m)^\s*#.*\n', '', text)
    return text

_OBF_PREAMBLE = """
import base64 as __b64, zlib as __zl

def __sx__(c: bytes, k: int, s: int) -> str:
    raw = bytearray(__b64.b64decode(c))
    kb = k & 0xFF
    sb = s & 0xFF
    for i in range(len(raw)):
        raw[i] ^= ((kb + sb * i) & 0xFF)
    return __zl.decompress(bytes(raw)).decode('utf-8', 'strict')
"""

def _collect_docstring_const_nodes(root: ast.AST):
    if KEEP_DOCSTRINGS:
        keep = set()
        def mark_first_str_expr(body):
            if body and isinstance(body[0], ast.Expr):
                v = body[0].value
                if isinstance(v, ast.Constant) and isinstance(v.value, str):
                    keep.add(id(v))
        class _Walker(ast.NodeVisitor):
            def visit_Module(self, node: ast.Module):
                mark_first_str_expr(node.body); self.generic_visit(node)
            def visit_FunctionDef(self, node: ast.FunctionDef):
                mark_first_str_expr(node.body); self.generic_visit(node)
            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
                mark_first_str_expr(node.body); self.generic_visit(node)
            def visit_ClassDef(self, node: ast.ClassDef):
                mark_first_str_expr(node.body); self.generic_visit(node)
        _Walker().visit(root)
        return keep
    return set()

class _StringObfuscator(ast.NodeTransformer):
    def __init__(self, doc_keep_ids: set):
        super().__init__()
        self._doc_keep_ids = doc_keep_ids
        self._in_joined = 0

    def visit_JoinedStr(self, node: ast.JoinedStr):
        self._in_joined += 1
        self.generic_visit(node)
        self._in_joined -= 1
        return node

    def visit_Constant(self, node: ast.Constant):
        if not isinstance(node.value, str):
            return node
        if id(node) in self._doc_keep_ids:
            return node
        if self._in_joined > 0:
            return node
        s_val = node.value
        k = random.randint(1, 255)
        s = random.randint(1, 255)
        packed = zlib.compress(s_val.encode("utf-8"), 9)
        out = bytearray(packed)
        kb = k & 0xFF
        sb = s & 0xFF
        for i in range(len(out)):
            out[i] ^= ((kb + sb * i) & 0xFF)
        c_b64 = base64.b64encode(bytes(out))
        return ast.Call(
            func=ast.Name(id="__sx__", ctx=ast.Load()),
            args=[
                ast.Constant(value=c_b64, kind=None),
                ast.Constant(value=k,     kind=None),
                ast.Constant(value=s,     kind=None),
            ],
            keywords=[]
        )

def _make_int_expr(n: int) -> ast.expr:
    if n == 0:
        a = random.randint(1, 2**31 - 1)
        return ast.BinOp(
            left=ast.Constant(value=a, kind=None),
            op=ast.BitXor(),
            right=ast.Constant(value=a, kind=None),
        )
    if n < 0:
        inner = _make_int_expr(-n)
        return ast.UnaryOp(op=ast.USub(), operand=inner)
    r1 = random.randint(1, 2**31 - 1)
    r2 = n ^ r1
    return ast.BinOp(
        left=ast.Constant(value=r1, kind=None),
        op=ast.BitXor(),
        right=ast.Constant(value=r2, kind=None),
    )

class _NumberObfuscator(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant):
        v = node.value
        if isinstance(v, bool):
            return node
        if isinstance(v, int):
            return _make_int_expr(v)
        return node

def obfuscate_strings(source_code: str) -> str:
    tree = ast.parse(source_code)
    doc_keep_ids = _collect_docstring_const_nodes(tree)
    tree = _StringObfuscator(doc_keep_ids).visit(tree)
    ast.fix_missing_locations(tree)
    if NASR_NUMBERS:
        tree = _NumberObfuscator().visit(tree)
        ast.fix_missing_locations(tree)
    pre_tree = ast.parse(_OBF_PREAMBLE)
    merged = ast.Module(body=pre_tree.body + tree.body, type_ignores=[])
    if hasattr(ast, "unparse"):
        return ast.unparse(merged)
    return source_code

_INTEGRITY_TEMPLATE = r'''
# === Integrity Guard (no password) ===
import hashlib, hmac, binascii, sys

__NASR_SECRET_HEX = "{SECRET_HEX}"
__NASR_INTEGRITY  = "{INTEGRITY_HEX}"
__NASR_TAG        = "NASR_OBF_V3_NUM"

def __nasr_check_integrity(payload_bytes: bytes):
    try:
        key = binascii.unhexlify(__NASR_SECRET_HEX)
    except Exception:
        sys.exit(1)
    calc = hmac.new(key, payload_bytes, hashlib.sha256).hexdigest()
    if calc != __NASR_INTEGRITY:
        sys.exit(1)
'''

def _minify_code(src: str) -> str:
    src = re.sub(r'[ \t]+(?=\r?\n)', '', src)
    lines = src.splitlines()
    new_lines = []
    empty_count = 0
    for line in lines:
        if line.strip() == "":
            empty_count += 1
            if empty_count > 1:
                continue
        else:
            empty_count = 0
        new_lines.append(line)
    return "\n".join(new_lines) + "\n"

# ================== الطبقة الأولى – NASR OBF V3 + HMAC ==================

def stage1_obf_and_guard(src_path: str, out_path: str) -> None:
    with open(src_path, "r", encoding="utf-8") as f:
        src = f.read()
    src = strip_top_banner_and_comments(src)
    obf_src = obfuscate_strings(src)
    payload_bytes = obf_src.encode("utf-8")

    secret = os.urandom(32)
    secret_hex = binascii.hexlify(secret).decode("ascii")
    integrity_hex = hmac.new(secret, payload_bytes, hashlib.sha256).hexdigest()

    guard = _INTEGRITY_TEMPLATE.format(
        SECRET_HEX=secret_hex,
        INTEGRITY_HEX=integrity_hex
    )

    wrapped = f"""{guard}

def __nasr_run_app():
{textwrap.indent(obf_src, '    ')}

if __name__ == "__main__":
    __payload = {repr(payload_bytes)}
    __nasr_check_integrity(__payload)
    __nasr_run_app()
"""

    if NASR_MINIFY:
        wrapped = _minify_code(wrapped)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(wrapped)

# ================== الطبقة الثانية – marshal + zlib + XOR ==================

def _xor_bytes_stage2(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("empty key")
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def stage2_pack_xor(src_path: str, out_path: str) -> None:
    with open(src_path, "r", encoding="utf-8") as f:
        src = f.read()
    code_obj   = compile(src, src_path or "<src>", "exec")
    marshalled = marshal.dumps(code_obj)
    compressed = zlib.compress(marshalled, 9)
    key_bytes  = os.urandom(32)
    mask_bytes = os.urandom(32)
    encrypted  = _xor_bytes_stage2(compressed, key_bytes)
    masked_key = _xor_bytes_stage2(key_bytes, mask_bytes)
    key_b64  = base64.b64encode(masked_key).decode("ascii")
    mask_b64 = base64.b64encode(mask_bytes).decode("ascii")
    blob_b64 = base64.b64encode(encrypted).decode("ascii")

    loader = f'''# Auto-generated loader (zlib + XOR + marshal)
import zlib, base64, marshal

def xor_bytes(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("empty key")
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

_KEY_B64  = {key_b64!r}
_MASK_B64 = {mask_b64!r}
_BLOB_B64 = {blob_b64!r}

_masked_key = base64.b64decode(_KEY_B64)
_mask       = base64.b64decode(_MASK_B64)
_key        = xor_bytes(_masked_key, _mask)

_encrypted    = base64.b64decode(_BLOB_B64)
_decompressed = zlib.decompress(xor_bytes(_encrypted, _key))
_code         = marshal.loads(_decompressed)

exec(_code, {{"__name__": "__main__"}})
'''
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(loader)

# ================== الطبقة الثالثة – Advanced Encryptor V7 ==================

DEFAULT_ALG = int(os.environ.get("ALG", "1"))
DEFAULT_COMPRESS_ALGO = os.environ.get("COMPRESS_ALGO", "zlib").lower().strip()

try:
    from Crypto.Cipher import ChaCha20_Poly1305
    from Crypto.Random import get_random_bytes
except Exception:
    try:
        from Cryptodome.Cipher import ChaCha20_Poly1305
        from Cryptodome.Random import get_random_bytes
    except:
        pass

try:
    from argon2.low_level import hash_secret_raw, Type as ArgonType
    HAVE_ARGON2 = True
except Exception:
    HAVE_ARGON2 = False

try:
    from Crypto.Cipher import AES as _AES_CHECK
    HAVE_AES = True
except Exception:
    try:
        from Cryptodome.Cipher import AES as _AES_CHECK
        HAVE_AES = True
    except:
        HAVE_AES = False

MAGIC = b"CHCH7"
VER   = 2

KDF_SCRYPT = 1
KDF_PBKDF2 = 2
KDF_MIXED  = 4
KDF_TRIPLE = 8

ALG_CHACHA20  = 1
ALG_XCHACHA20 = 2
ALG_AESGCM    = 3
ALG_AESSIV    = 4

SCRYPT_DEFAULT_N = 1 << 15
SCRYPT_MIN_N     = 1 << 12
SCRYPT_r         = 8
SCRYPT_p         = 1
DEFAULT_SCRYPT_MEM_MB = int(os.environ.get("SCRYPT_MEM_MB", "16"))

PBKDF2_ITERS = 1_000_000
PBKDF2_DKLEN = 32

ARGON2_TIME_COST   = int(os.environ.get("ARGON2_TIME", "2"))
ARGON2_MEMORY_KB   = int(os.environ.get("ARGON2_MEM_KB", "65536"))
ARGON2_PARALLELISM = int(os.environ.get("ARGON2_PAR", "2"))
ARGON2_OUTLEN      = 32

IF_MAGIC = b"IFv7"
FLAG_COMPRESSED = 0x01
FLAG_ZPAD_PWR2  = 0x02
FLAG_MARSHAL    = 0x04
FLAG_LZMA       = 0x08

LEN_HIDE_MODE = "random_range"
PAD_MIN = 64
PAD_MAX = 1024
B64_CHUNK = 96

def _hkdf_like_v7(key_material: bytes, salt: bytes, out_len: int = 32) -> bytes:
    digest = hmac.new(salt, key_material, hashlib.sha256).digest()
    if out_len <= len(digest):
        return digest[:out_len]
    out = bytearray()
    block = digest
    while len(out) < out_len:
        out.extend(block)
        block = hashlib.sha256(block + salt).digest()
    return bytes(out[:out_len])

def _next_power_of_two(n: int) -> int:
    if n <= 1: return 1
    return 1 << (n - 1).bit_length()

def _sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def _scrypt_memory_required(n: int, r: int, p: int) -> int:
    return 128 * r * n * p

def kdf_scrypt_autotune(password: str, salt: bytes,
                        start_n: int = SCRYPT_DEFAULT_N,
                        min_n: int = SCRYPT_MIN_N,
                        r: int = SCRYPT_r,
                        p: int = SCRYPT_p,
                        target_mb: int = DEFAULT_SCRYPT_MEM_MB):
    target_bytes = max(1, target_mb) * 1024 * 1024
    n = start_n
    while _scrypt_memory_required(n, r, p) > target_bytes and n > min_n:
        n //= 2
    last_err = None
    while n >= min_n:
        try:
            key = hashlib.scrypt(password.encode(), salt=salt, n=n, r=r, p=p, dklen=32)
            return key, (n, r, p)
        except Exception as e:
            last_err = e
            n //= 2
    raise RuntimeError(f"scrypt autotune failed down to N={min_n}: {last_err}")

def kdf_pbkdf2(password: str, salt: bytes, iters: int = PBKDF2_ITERS, dklen: int = PBKDF2_DKLEN) -> bytes:
    return hashlib.pbkdf2_hmac('sha512', password.encode(), salt, iters, dklen=dklen)

def kdf_argon2id(password: str, salt: bytes) -> bytes:
    if not HAVE_ARGON2:
        return _sha256(password.encode() + salt)[:32]
    return hash_secret_raw(
        secret=password.encode(),
        salt=salt,
        time_cost=ARGON2_TIME_COST,
        memory_cost=ARGON2_MEMORY_KB,
        parallelism=ARGON2_PARALLELISM,
        hash_len=ARGON2_OUTLEN,
        type=ArgonType.ID
    )

def pack_kdf_params(kdf_id: int, scrypt_params=None,
                    pbkdf2_iters: int = PBKDF2_ITERS,
                    argon2_params=None) -> bytes:
    if kdf_id == KDF_TRIPLE:
        n, r, p = scrypt_params
        t, mem_kb, par, outlen = argon2_params
        return struct.pack("<III IIII I", n, r, p, t, mem_kb, par, outlen, pbkdf2_iters)
    elif kdf_id == KDF_MIXED:
        n, r, p = scrypt_params
        return struct.pack("<III I", n, r, p, pbkdf2_iters)
    elif kdf_id == KDF_SCRYPT:
        n, r, p = scrypt_params
        return struct.pack("<III", n, r, p)
    elif kdf_id == KDF_PBKDF2:
        return struct.pack("<I", pbkdf2_iters)
    else:
        raise ValueError("Unknown KDF id")

def derive_key(password: str, salt: bytes, pepper: str = ""):
    pwd = password + (pepper or "")
    try:
        s_key, (n, r, p) = kdf_scrypt_autotune(pwd, salt)
        have_scrypt = True
    except Exception:
        have_scrypt = False
        s_key = b""
        n, r, p = (SCRYPT_MIN_N, SCRYPT_r, SCRYPT_p)

    p_key = kdf_pbkdf2(pwd, salt, PBKDF2_ITERS, dklen=32)

    if HAVE_ARGON2:
        a_key = kdf_argon2id(pwd, salt)
        if have_scrypt:
            mix = _hkdf_like_v7(s_key + a_key + p_key, salt, 32)
            params = pack_kdf_params(KDF_TRIPLE, (n, r, p), PBKDF2_ITERS,
                                     argon2_params=(ARGON2_TIME_COST, ARGON2_MEMORY_KB, ARGON2_PARALLELISM, ARGON2_OUTLEN))
            return KDF_TRIPLE, mix, params
        else:
            mix = _hkdf_like_v7(a_key + p_key, salt, 32)
            params = pack_kdf_params(KDF_PBKDF2, None, PBKDF2_ITERS)
            return KDF_PBKDF2, mix, params
    else:
        if have_scrypt:
            mix = _hkdf_like_v7(s_key + p_key, salt, 32)
            params = pack_kdf_params(KDF_MIXED, (n, r, p), PBKDF2_ITERS)
            return KDF_MIXED, mix, params
        else:
            mix = _hkdf_like_v7(p_key, salt, 32)
            params = pack_kdf_params(KDF_PBKDF2, None, PBKDF2_ITERS)
            return KDF_PBKDF2, mix, params

def prepare_inner_plaintext(raw: bytes, filename_hint: str = "", as_marshal: bool = True, compress_algo: str = "zlib") -> bytes:
    flags = 0
    if compress_algo == "lzma":
        import lzma
        data = lzma.compress(raw, preset=9)
        flags |= (FLAG_COMPRESSED | FLAG_LZMA)
    elif compress_algo == "zlib":
        comp = zlib.compress(raw, 6)
        data = comp if len(comp) < len(raw) else raw
        if data is comp:
            flags |= FLAG_COMPRESSED
    else:
        data = raw

    if as_marshal:
        flags |= FLAG_MARSHAL

    meta = {
        "sha256": _sha256(raw).hex(),
        "created_at": int(_time_mod.time()),
        "name": os.path.basename(filename_hint) if filename_hint else ""
    }
    meta_b = json.dumps(meta, separators=(",", ":")).encode("utf-8")

    if LEN_HIDE_MODE == "power2":
        total_no_pad = 4 + 1 + 4 + 4 + 4 + len(meta_b) + len(data)
        target = _next_power_of_two(total_no_pad + PAD_MIN)
        pad_len = max(0, target - total_no_pad); flags |= FLAG_ZPAD_PWR2
    else:
        pad_len = (os.urandom(1)[0] % (PAD_MAX - PAD_MIN + 1) + PAD_MIN) if PAD_MAX >= PAD_MIN else 0

    padding = os.urandom(pad_len) if pad_len else b""
    head = IF_MAGIC + bytes([flags]) + struct.pack("<I", len(raw)) + struct.pack("<I", pad_len) + struct.pack("<I", len(meta_b))
    return head + meta_b + data + padding

def encrypt_blob(plaintext_compiled_or_raw: bytes, password: str, filename_hint: str, as_marshal: bool, alg: int, compress_algo: str) -> bytes:
    inner = prepare_inner_plaintext(plaintext_compiled_or_raw, filename_hint, as_marshal=as_marshal, compress_algo=compress_algo)
    salt = get_random_bytes(16)

    pepper_env = os.environ.get("PEPPER_ENV", "")
    pepper = os.environ.get(pepper_env, "") if pepper_env else ""

    kdf_id, key, kdfparams = derive_key(password, salt, pepper=pepper)

    head_fixed = MAGIC + bytes([VER, kdf_id, alg]) + salt + kdfparams

    if alg == ALG_CHACHA20:
        nonce = get_random_bytes(12)
        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        cipher.update(head_fixed)
        ct, tag = cipher.encrypt_and_digest(inner)
        return head_fixed + nonce + tag + ct
    elif alg == ALG_AESGCM:
        if not HAVE_AES:
            raise RuntimeError("AES backend not available for AES-GCM")
        from Crypto.Cipher import AES
        nonce = get_random_bytes(12)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        cipher.update(head_fixed)
        ct, tag = cipher.encrypt_and_digest(inner)
        return head_fixed + nonce + tag + ct
    elif alg == ALG_AESSIV:
        if not HAVE_AES:
            raise RuntimeError("AES backend not available for AES-SIV")
        from Crypto.Cipher import AES
        cipher = AES.new(key, AES.MODE_SIV)
        cipher.update(head_fixed)
        ct, tag = cipher.encrypt_and_digest(inner)
        return head_fixed + tag + ct
    elif alg == ALG_XCHACHA20:
        try:
            from nacl.bindings import crypto_aead_xchacha20poly1305_ietf_encrypt
        except Exception:
            raise RuntimeError("PyNaCl not available for XChaCha20-Poly1305")
        nonce = get_random_bytes(24)
        aad = head_fixed
        ct = crypto_aead_xchacha20poly1305_ietf_encrypt(inner, aad, nonce, key)
        return head_fixed + nonce + ct
    else:
        raise ValueError("Unknown ALG")

def chunk_b64(s: str, n: int):
    return [s[i:i+n] for i in range(0, len(s), n)]

def _xor_bytes_v7(data: bytes, key: int) -> bytes:
    key &= 0xFF
    return bytes((b ^ key) for b in data)

def _obfuscate_pw_parts(pw: str):
    parts = [pw[i:i+4] for i in range(0, len(pw), 4)] if pw else []
    order = list(range(len(parts)))
    if len(order) >= 4:
        order = [2, 0, 3, 1] + list(range(4, len(order)))
    enc_hex_parts = []
    keys = []
    for part in parts:
        k = random.randint(1, 255)
        enc = _xor_bytes_v7(part.encode("utf-8"), k)
        enc_hex_parts.append(binascii.hexlify(enc).decode("ascii"))
        keys.append(k)
    return enc_hex_parts, keys, order

def build_loader_v7(b64_blob: str, output_loader: str, internal_password: str, ver: int,
                    integrity_tag: str, src_hash: str, runtime_secret_sha256: str):
    enc_parts_hex, keys, order = _obfuscate_pw_parts(internal_password)
    enc_parts_lit = ', '.join([f'"{p}"' for p in enc_parts_hex])
    keys_lit = ', '.join([str(k) for k in keys])
    order_lit = ', '.join([str(i) for i in order])

    b64_parts = chunk_b64(b64_blob, B64_CHUNK)
    b64_lit   = ',\n    '.join([f'"{p}"' for p in b64_parts])

    mangle = "_" + base64.b64encode(os.urandom(6)).decode("ascii").rstrip("=\n").replace("/","A").replace("+","B")

    loader_code = f'''# NASR
import base64, hashlib, struct, sys, os, time, zlib, hmac, json, marshal, binascii, socket
try:
    from Crypto.Cipher import ChaCha20_Poly1305
except Exception:
    try: from Cryptodome.Cipher import ChaCha20_Poly1305
    except: pass
try:
    from Crypto.Cipher import AES
    _HAVE_AES = True
except Exception:
    try: from Cryptodome.Cipher import AES; _HAVE_AES=True
    except: _HAVE_AES=False

MAGIC = b"CHCH7"; VER={ver}
KDF_SCRYPT=1; KDF_PBKDF2=2; KDF_MIXED=4; KDF_TRIPLE=8
ALG_CHACHA20=1; ALG_XCHACHA20=2; ALG_AESGCM=3; ALG_AESSIV=4
IF_MAGIC = b"IFv7"
FLAG_COMPRESSED = 0x01
FLAG_ZPAD_PWR2  = 0x02
FLAG_MARSHAL    = 0x04
FLAG_LZMA       = 0x08
integrity_tag = "{integrity_tag}"
_src_hash = "{src_hash}"
RUNTIME_SECRET_SHA256 = "{runtime_secret_sha256}"
_encrypted_parts = [
    {b64_lit}
]
encrypted_b64 = "".join(_encrypted_parts)
_pw_enc_hex = [{enc_parts_lit}]
_pw_keys    = [{keys_lit}]
_order      = [{order_lit}]
def _collect_pepper():
    pe = os.environ.get("PEPPER_ENV","")
    pv = os.environ.get(pe, "") if pe else ""
    pel = os.environ.get("PEPPER_ENV_LIST","")
    if pel:
        for name in [x.strip() for x in pel.split(",") if x.strip()]:
            pv += os.environ.get(name, "")
    return pv
def _anti_debug():
    if os.environ.get("ANTIDEBUG","0") != "1":
        return
    try:
        if sys.gettrace() is not None or getattr(sys, "getprofile", lambda: None)() is not None:
            sys.exit(1)
        if sys.platform.startswith("linux"):
            try:
                with open("/proc/self/status","r") as f:
                    for ln in f:
                        if ln.startswith("TracerPid:") and int(ln.split()[1]) != 0:
                            sys.exit(1)
            except Exception: pass
        t0 = time.perf_counter()
        x = 0
        for _ in range(200000):
            x += 1
        if (time.perf_counter() - t0) > 0.25:
            sys.exit(1)
    except Exception:
        pass
def _anti_vm():
    try:
        flags = []
        if os.path.exists("/proc/cpuinfo"):
            txt = open("/proc/cpuinfo","r",errors="ignore").read().lower()
            if any(k in txt for k in ("hypervisor", "kvm", "qemu", "vmware", "virtualbox")):
                flags.append("cpuinfo")
        suspicious = ["/system/bin/qemu-props", "/dev/vboxguest", "/dev/vmci", "/dev/kvm"]
        if any(os.path.exists(p) for p in suspicious):
            flags.append("files")
        try:
            hn = socket.gethostname().lower()
            if any(k in hn for k in ("vm", "qemu", "vbox", "test")):
                flags.append("hostname")
        except Exception: pass
        if flags:
            sys.exit(1)
    except Exception:
        pass
def _hkdf_like(key_material: bytes, salt: bytes, out_len: int = 32) -> bytes:
    digest = hmac.new(salt, key_material, hashlib.sha256).digest()
    if out_len <= len(digest):
        return digest[:out_len]
    out = bytearray()
    block = digest
    while len(out) < out_len:
        out.extend(block)
        block = hashlib.sha256(block + salt).digest()
    return bytes(out[:out_len])
def _get_internal_pw():
    parts = []
    for i in _order:
        if i < len(_pw_enc_hex):
            try:
                raw = bytearray(binascii.unhexlify(_pw_enc_hex[i]))
                k = _pw_keys[i] & 0xFF if i < len(_pw_keys) else 0
                for j in range(len(raw)):
                    raw[j] ^= k
                parts.append(raw.decode("utf-8","strict"))
            except Exception:
                pass
    return "".join(parts)
def _parse_inner(blob: bytes):
    pos=0
    if blob[:4] != IF_MAGIC: raise ValueError("Bad inner magic")
    pos+=4
    flags = blob[pos]; pos+=1
    (orig_len,) = struct.unpack("<I", blob[pos:pos+4]); pos+=4
    (pad_len,)  = struct.unpack("<I", blob[pos:pos+4]); pos+=4
    (meta_len,) = struct.unpack("<I", blob[pos:pos+4]); pos+=4
    total = len(blob)
    if meta_len > total - pos: raise ValueError("Corrupt inner (meta_len)")
    meta_b = blob[pos:pos+meta_len]; pos+=meta_len
    if pad_len > total - pos: raise ValueError("Corrupt inner (pad)")
    data_len = total - pos - pad_len
    if data_len < 0: raise ValueError("Corrupt inner (len)")
    data = blob[pos:pos+data_len]
    if (flags & FLAG_COMPRESSED):
        if (flags & FLAG_LZMA):
            import lzma
            out = lzma.decompress(data)
        else:
            out = zlib.decompress(data)
    else:
        out = data
    if len(out) != orig_len: raise ValueError("Inner length mismatch")
    try:
        meta = json.loads(meta_b.decode("utf-8"))
    except Exception:
        meta = {{}}
    return out, meta, flags
def _derive_key_for_decrypt(kdf_id: int, enc: bytes, pos: int, pw: str, salt: bytes):
    if kdf_id == KDF_TRIPLE:
        n, r, p, t, mem_kb, par, outlen, iters = struct.unpack("<III IIII I", enc[pos:pos+4*9]); pos += 4*9
        try:
            from argon2.low_level import hash_secret_raw, Type as ArgonType
            a_key = hash_secret_raw(secret=pw.encode(), salt=salt, time_cost=t, memory_cost=mem_kb, parallelism=par, hash_len=outlen, type=ArgonType.ID)
        except Exception:
            a_key = hashlib.sha256(pw.encode()+salt).digest()[:32]
        s_key = hashlib.scrypt(pw.encode(), salt=salt, n=n, r=r, p=p, dklen=32)
        p_key = hashlib.pbkdf2_hmac('sha512', pw.encode(), salt, iters, dklen=32)
        key   = _hkdf_like(s_key + a_key + p_key, salt, 32)
        return key, pos
    elif kdf_id == KDF_MIXED:
        n,r,p, iters = struct.unpack("<III I", enc[pos:pos+16]); pos += 16
        s_key = hashlib.scrypt(pw.encode(), salt=salt, n=n, r=r, p=p, dklen=32)
        p_key = hashlib.pbkdf2_hmac('sha512', pw.encode(), salt, iters, dklen=32)
        key   = _hkdf_like(s_key + p_key, salt, 32)
        return key, pos
    elif kdf_id == KDF_SCRYPT:
        n,r,p = struct.unpack("<III", enc[pos:pos+12]); pos += 12
        key = hashlib.scrypt(pw.encode(), salt=salt, n=n, r=r, p=p, dklen=32)
        return key, pos
    elif kdf_id == KDF_PBKDF2:
        (iters,) = struct.unpack("<I", enc[pos:pos+4]); pos += 4
        key = hashlib.pbkdf2_hmac('sha512', pw.encode(), salt, iters, dklen=32)
        return key, pos
    else:
        raise ValueError("Unknown KDF")
def _check_integrity(pw: str):
    key = hashlib.sha256(pw.encode()).digest()
    calc = hmac.new(key, encrypted_b64.encode('utf-8'), hashlib.sha256).hexdigest()
    if calc != integrity_tag:
        sys.exit(1)
def _decrypt(enc: bytes, pw: str) -> bytes:
    pos=0
    if enc[:5] != MAGIC: raise ValueError("Bad magic")
    pos+=5
    ver = enc[pos]; pos+=1
    if ver != VER: raise ValueError("Bad version")
    kdf_id = enc[pos]; pos+=1
    alg    = enc[pos]; pos+=1
    salt = enc[pos:pos+16]; pos+=16
    key, pos = _derive_key_for_decrypt(kdf_id, enc, pos, pw, salt)
    head_fixed = enc[:pos]
    if alg == ALG_CHACHA20:
        nonce = enc[pos:pos+12]; pos+=12
        tag   = enc[pos:pos+16]; pos+=16
        ct    = enc[pos:]
        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        cipher.update(head_fixed)
        inner = cipher.decrypt_and_verify(ct, tag)
    elif alg == ALG_AESGCM:
        if not _HAVE_AES: raise RuntimeError("AES not available for AES-GCM")
        nonce = enc[pos:pos+12]; pos+=12
        tag   = enc[pos:pos+16]; pos+=16
        ct    = enc[pos:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        cipher.update(head_fixed)
        inner = cipher.decrypt_and_verify(ct, tag)
    elif alg == ALG_AESSIV:
        if not _HAVE_AES: raise RuntimeError("AES not available for AES-SIV")
        tag = enc[pos:pos+16]; pos+=16
        ct  = enc[pos:]
        cipher = AES.new(key, AES.MODE_SIV)
        cipher.update(head_fixed)
        inner = cipher.decrypt_and_verify(ct, tag)
    elif alg == ALG_XCHACHA20:
        try:
            from nacl.bindings import crypto_aead_xchacha20poly1305_ietf_decrypt
        except Exception:
            raise RuntimeError("PyNaCl not available for XChaCha20-Poly1305")
        nonce = enc[pos:pos+24]; pos+=24
        ct = enc[pos:]
        inner = crypto_aead_xchacha20poly1305_ietf_decrypt(ct, head_fixed, nonce, key)
    else:
        raise ValueError("Unknown ALG")
    return inner
def __chk_src(code_bytes: bytes):
    try:
        if _src_hash:
            h = hashlib.sha256(code_bytes).hexdigest()
            if h != _src_hash:
                sys.exit(1)
    except Exception:
        pass
def _wipe(b):
    try:
        for i in range(len(b)): b[i]=0
    except Exception: pass
def _auto_pw():
    try:
        pw = _get_internal_pw()
        env_name = os.environ.get("EXTRA_PW_ENV", "")
        if env_name:
            pw += os.environ.get(env_name, "")
        pepper_val = _collect_pepper()
        if pepper_val:
            pw += pepper_val
        try:
            _ = hashlib.pbkdf2_hmac("sha512", pw.encode(), hashlib.sha256(pw.encode()).digest(), 5000, dklen=32)
        except Exception:
            pass
        return pw
    except Exception:
        sys.exit(1)
if __name__ == "__main__":
    _anti_debug()
    _anti_vm()
    pw = _auto_pw()
    _check_integrity(pw)
    enc = base64.b64decode(encrypted_b64)
    try:
        inner = _decrypt(enc, pw)
        blob, meta, flags = _parse_inner(inner)
    except Exception:
        sys.exit(1)
    try:
        ns = {{}}
        if (flags & FLAG_MARSHAL):
            __chk_src(blob)
            codeobj = marshal.loads(blob)
            exec(codeobj, ns, ns)
        else:
            __chk_src(blob)
            code = blob.decode("utf-8")
            exec(compile(code, "<secured>", "exec"), ns, ns)
    except Exception:
        sys.exit(1)
    try:
        if isinstance(blob, (bytes, bytearray)):
            ba = bytearray(blob)
            for i in range(len(ba)):
                ba[i] = 0
    except Exception:
        pass
'''
    for sym in ["_anti_debug","_anti_vm","_check_integrity","_get_internal_pw",
                "_hkdf_like","_parse_inner","_derive_key_for_decrypt","_decrypt",
                "_wipe","_collect_pepper","__chk_src","_auto_pw"]:
        loader_code = loader_code.replace(sym, sym + mangle)

    with open(output_loader, "w", encoding="utf-8") as f:
        f.write(loader_code)

def stage3_encrypt_v7(src_path: str, out_path: str) -> None:
    with open(src_path, "r", encoding="utf-8") as f:
        src = f.read()
    src = strip_top_banner_and_comments(src)
    obf_src = obfuscate_strings(src)
    codeobj = compile(obf_src, "<secured>", "exec")
    marshaled = marshal.dumps(codeobj)
    internal_pw = ""
    alg = DEFAULT_ALG
    comp_algo = DEFAULT_COMPRESS_ALGO if DEFAULT_COMPRESS_ALGO in ("zlib","lzma","none") else "zlib"
    blob = encrypt_blob(marshaled, internal_pw, filename_hint=src_path, as_marshal=True, alg=alg, compress_algo=comp_algo)
    b64  = base64.b64encode(blob).decode("ascii")
    tag_key = hashlib.sha256(internal_pw.encode()).digest()
    integrity_tag = hmac.new(tag_key, b64.encode('utf-8'), hashlib.sha256).hexdigest()
    src_hash = hashlib.sha256(marshaled).hexdigest()
    RUNTIME_PW_PLAIN = "@#@#$@%&^@>>×<<×<>JSJWJHSHSHSHSHSHSBSBSBSHWHSHSHUWU272727227UWUSHSHSHSBYBYBYBSBHSUEUنينيتينينينينهيهثههثثهههثنثنينينيزيزيميممصححصحصخثخثمثنثنثنينويوويوييزز٨٢٧٢٧٢٧٢٧٢٧٢٧٧٧٢٨١٩١٠١٠٠٠١٠١٩خخ٢خ٢ه٢ه٣ه٣هه٣هتيتيتيتيتيتتيتت!^^@^@^@&&@*!((!(!(@*@*&@&@@^^@&@*(@!))!@@*@*@&&#&##&#&HSHSHAJAJJAJJJJjjsjsjhsshhhHhhhehwhwhhhHhhshshshshsjeiieiei82828282282ii2jwjsjsnssnsbbsنتنتننصنسنسنصنصنصنثهههثهثنثنيوييويوتييننيينينينينينينينينينينثننثنثنثنذ&@&×&×>>××>>×&@&@&@&@&@،@@[×[×٠٢٠٢٩٢٩٨٢>>÷&#&#&#"
    runtime_secret_sha256 = hashlib.sha256(RUNTIME_PW_PLAIN.encode()).hexdigest()
    build_loader_v7(
        b64,
        out_path,
        internal_password=internal_pw,
        ver=VER,
        integrity_tag=integrity_tag,
        src_hash=src_hash,
        runtime_secret_sha256=runtime_secret_sha256
    )

# ================== الطبقة الرابعة – minify بصمت ==================

def stage4_minify(path: str) -> None:
    if not python_minifier:
        return
    try:
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
        try:
            minified = python_minifier.minify(source)
        except Exception:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(minified)
    except Exception:
        return

# ========= المرحلة الخامسة – تغليف ملف Loader إلى ملف ثنائي .nasr =========

MAGIC_NASR = b"NSRP"
VER_NASR   = 1

# مفتاح التشفير المتوافق مع المشغل الجديد
_MASTER_KEY_XOR_HEX = "2554c02644076615d1c04778691e0f3c2dd2c3f0e19687b4a55a4b78691e0f3c"

def _get_master_key_bytes():
    """
    استخراج المفتاح الحقيقي لاستخدامه في تشفير ملف الـ .nasr
    """
    raw = bytes.fromhex(_MASTER_KEY_XOR_HEX)
    return bytes((b ^ 0x5A) for b in raw)

try:
    from Crypto.Cipher import AES as _NASR_AES
except Exception:
    try:
        from Cryptodome.Cipher import AES as _NASR_AES
    except Exception:
        _NASR_AES = None

def _derive_key_player(master_key: bytes, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256",
        master_key,
        salt,
        200_000,
        dklen=32
    )

def wrap_for_player(loader_path: str, nasr_path: str) -> None:
    if not os.path.isfile(loader_path):
        print(f"[-] ملف الـ Loader غير موجود: {loader_path}")
        raise SystemExit(1)

    if _NASR_AES is None:
        print("[-] مكتبة AES (Crypto / Cryptodome) غير متوفرة. الرجاء تثبيت pycryptodome")
        raise SystemExit(1)

    with open(loader_path, "rb") as f:
        plain = f.read()

    # توليد salt + nonce
    from os import urandom
    salt  = urandom(16)
    nonce = urandom(12)

    master_key_bytes = _get_master_key_bytes()
    key = _derive_key_player(master_key_bytes, salt)

    cipher = _NASR_AES.new(key, _NASR_AES.MODE_GCM, nonce=nonce)
    header = MAGIC_NASR + bytes([VER_NASR])
    cipher.update(header)
    ct, tag = cipher.encrypt_and_digest(plain)

    blob = header + salt + nonce + tag + ct

    with open(nasr_path, "wb") as f:
        f.write(blob)

# ================== دورة تشفير كاملة (المراحل 1–4) ==================

def run_full_encrypt_round(src: str, out: str) -> None:
    base = os.path.splitext(out)[0]
    tmp1 = base + ".nasr1.tmp.py"
    tmp2 = base + ".nasr2.tmp.py"
    try:
        stage1_obf_and_guard(src, tmp1)
        stage2_pack_xor(tmp1, tmp2)
        stage3_encrypt_v7(tmp2, out)
        stage4_minify(out)
    finally:
        for p in (tmp1, tmp2):
            try:
                if os.path.exists(p):
                    os.remove(p)
            except Exception:
                pass

# ================== الدالة الرئيسية – 4 مراحل + تغليف .nasr ==================

def main_encrypt():
    src = input("أدخل اسم ملف البايثون لتشفيره: ").strip()
    base_name = input("أدخل اسم الملف النهائي (بدون امتداد، مثلاً nasr_tool): ").strip()

    if not src or not os.path.isfile(src):
        print("❌ ملف الإدخال غير موجود.")
        return
    if not base_name:
        print("❌ لم يتم تحديد اسم الملف.")
        return

    base_out   = os.path.splitext(base_name)[0]
    round1_out = base_out + ".round1.tmp.py"
    loader_out = base_out + ".loader.tmp.py"
    nasr_out   = base_out + ".nasr"

    hide_cursor()
    try:
        wait_bar(20)

        # أولاً: 4 مراحل كاملة كما هي (stage1+2+3+4) → round1_out
        run_full_encrypt_round(src, round1_out)

        # ثانياً: إعادة تشفير round1_out بطبقة OBF+HMAC + minify
        stage1_obf_and_guard(round1_out, loader_out)
        stage4_minify(loader_out)

        # ثالثاً: تغليف loader_out داخل ملف ثنائي .nasr المتوافق مع المشغل
        wrap_for_player(loader_out, nasr_out)

    finally:
        show_cursor()
        for p in (round1_out, loader_out):
            try:
                if os.path.exists(p) and p != nasr_out:
                    os.remove(p)
            except Exception:
                pass

    print("\n" + "=" * 60)
    print("✅ تم إنشاء ملف NASR مغلق لا يعمل إلا مع أداة التشغيل:")
    print(f"   → {nasr_out}")
    print("=" * 60)

# ================== نقطة الدخول ==================

if __name__ == "__main__":
    try:
        if not check_connection():
            nasser_lock()
        main_encrypt()
    except KeyboardInterrupt:
        print("\nتم الإنهاء بواسطة المستخدم.")
