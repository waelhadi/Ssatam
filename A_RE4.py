#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, subprocess, textwrap, secrets, shutil, marshal, base64

def run(cmd, cwd=None, shell=False):
    p = subprocess.run(cmd, cwd=cwd, shell=shell,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT,
                       text=True)
    return p.returncode, p.stdout

def which(x):
    return shutil.which(x)

def ensure_pkgs():
    try:
        import Cython  # noqa
        import setuptools  # noqa
        return True
    except Exception:
        print("[-] تثبيت المتطلبات: cython setuptools wheel")
        rc, out = run([sys.executable, "-m", "pip", "install", "-U", "cython", "setuptools", "wheel"])
        print(out)
        return rc == 0

def is_pydroid():
    return "ru.iiec.pydroid3" in sys.executable or "ru.iiec.pydroid3" in sys.prefix

def get_writable_sitepackages():
    import site
    cands = []
    try:
        cands += list(site.getsitepackages())
    except Exception:
        pass
    try:
        cands.append(site.getusersitepackages())
    except Exception:
        pass
    for p in cands:
        if p and os.path.isdir(p) and os.access(p, os.W_OK):
            return p
    fb = os.path.join(sys.prefix, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages")
    os.makedirs(fb, exist_ok=True)
    if os.access(fb, os.W_OK):
        return fb
    return None

def make_workdir():
    # ✅ على Pydroid لازم يكون داخل /data وليس /storage
    if is_pydroid():
        wd = os.path.join(sys.prefix, "tmp_nasr_build_ext")
    else:
        wd = os.path.abspath("nasr_build_ext")
    os.makedirs(wd, exist_ok=True)
    return wd

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def try_strip(path):
    # جرّب strip/llvm-strip إن توفر
    for s in ("strip", "llvm-strip"):
        if which(s):
            rc, out = run([s, "--strip-unneeded", path])
            if rc == 0:
                return True, f"[+] stripped: {os.path.basename(path)} via {s}"
    return False, f"[-] strip not available for {os.path.basename(path)}"

# ================= Templates =================

SETUP_PY = """
from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [
    Extension(
        name="nasr_ext",
        sources=["nasr_ext.pyx"],
        extra_compile_args=["-O3","-fvisibility=hidden","-ffunction-sections","-fdata-sections"],
        extra_link_args=["-Wl,--gc-sections","-Wl,--strip-all"],
    )
]

setup(
    name="nasr_ext",
    version="1.0.0",
    ext_modules=cythonize(ext_modules, compiler_directives={"language_level": "3"}),
)
"""

CYTHON_PYX = """
# cython: language_level=3, boundscheck=False, wraparound=False, nonecheck=False

cdef bytes _PASSPHRASE = {PASSPHRASE_BYTES}
cdef int _KDF_ITERS = {KDF_ITERS}

cpdef str pack_payload(bytes marshalled):
    import os, zlib, base64, hashlib, hmac

    salt = os.urandom(16)
    master = hashlib.pbkdf2_hmac("sha256", _PASSPHRASE, salt, _KDF_ITERS, dklen=32)

    enc_key = hashlib.sha256(master + b"enc").digest()
    mac_key = hashlib.sha256(master + b"mac").digest()

    n = len(marshalled)
    out = bytearray(n)

    block = 0
    i = 0
    while i < n:
        ctr = block.to_bytes(8, "little", signed=False)
        ks = hashlib.blake2b(ctr, key=enc_key, digest_size=64).digest()
        j = 0
        while j < 64 and i < n:
            out[i] = (<unsigned char>marshalled[i]) ^ (<unsigned char>ks[j])
            i += 1
            j += 1
        block += 1

    ciphertext = bytes(out)
    tag = hmac.new(mac_key, salt + ciphertext, hashlib.sha256).digest()

    packed = salt + tag + ciphertext
    return base64.b64encode(zlib.compress(packed, 9)).decode("utf-8")


cpdef void run_payload(str payload_b64):
    import zlib, base64, hashlib, hmac, marshal

    blob = zlib.decompress(base64.b64decode(payload_b64.encode("utf-8")))
    if len(blob) < (16 + 32 + 1):
        raise RuntimeError("BAD_PAYLOAD")

    salt = blob[0:16]
    tag  = blob[16:48]
    ciphertext = blob[48:]

    master = hashlib.pbkdf2_hmac("sha256", _PASSPHRASE, salt, _KDF_ITERS, dklen=32)
    enc_key = hashlib.sha256(master + b"enc").digest()
    mac_key = hashlib.sha256(master + b"mac").digest()

    expect = hmac.new(mac_key, salt + ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expect):
        raise RuntimeError("TAMPERED_OR_WRONG_KEY")

    n = len(ciphertext)
    plain = bytearray(n)

    block = 0
    i = 0
    while i < n:
        ctr = block.to_bytes(8, "little", signed=False)
        ks = hashlib.blake2b(ctr, key=enc_key, digest_size=64).digest()
        j = 0
        while j < 64 and i < n:
            plain[i] = (<unsigned char>ciphertext[i]) ^ (<unsigned char>ks[j])
            i += 1
            j += 1
        block += 1

    codeobj = marshal.loads(bytes(plain))
    exec(codeobj, {"__name__": "__main__"})
"""

# ================= Build ELF executable runner (optional) =================

def build_elf_runner(build_dir, payload, out_dir):
    """
    يبني ELF executable اسمه nasr_run (اختياري)، يحتاج cython + clang + python3-config.
    مناسب جدًا لـ Termux.
    """
    if not which("clang"):
        return False, "[-] clang غير موجود => تخطي بناء ELF executable"

    cfg = which("python3-config") or which("python-config")
    if not cfg:
        return False, "[-] python3-config غير موجود => تخطي بناء ELF executable"

    runner_py = os.path.join(build_dir, "_runner.py")
    runner_c  = os.path.join(build_dir, "_runner.c")
    out_bin   = os.path.join(out_dir, "nasr_run")

    # runner Python (سيتم embed داخل C)
    write_file(runner_py, f"""# -*- coding: utf-8 -*-
import nasr_ext
PAYLOAD = {payload!r}
nasr_ext.run_payload(PAYLOAD)
""")

    # cython --embed
    rc, out = run([sys.executable, "-m", "Cython", "--embed", "-3", runner_py, "-o", runner_c], cwd=build_dir)
    if rc != 0:
        return False, "[-] فشل cython --embed:\n" + out

    # get flags from python3-config
    rc1, cflags = run([cfg, "--cflags"])
    rc2, ldflags = run([cfg, "--ldflags"])
    if rc1 != 0 or rc2 != 0:
        return False, "[-] فشل python3-config flags:\n" + cflags + "\n" + ldflags

    cmd = ["clang"] + cflags.split() + [runner_c, "-o", out_bin] + ldflags.split()
    rc, out = run(cmd, cwd=build_dir)
    if rc != 0:
        return False, "[-] فشل clang build:\n" + out

    ok, msg = try_strip(out_bin)
    return True, "[+] تم إنشاء ELF executable: " + out_bin + ("\n" + msg if msg else "")

# ================= Main =================

def main():
    print("=== NASR All-in-One (ELF .so + optional ELF runner + Embedded SO Loader) ===")

    if not ensure_pkgs():
        print("❌ ثبّت يدويًا: pip install -U cython setuptools wheel")
        return

    file_in = input("أدخل ملف بايثون المراد حمايته (مثال: 4.py): ").strip()
    if not os.path.isfile(file_in):
        print("❌ الملف غير موجود:", file_in)
        return

    out_name = input("أدخل اسم ملف الإخراج المحمي (مثال: 5.py): ").strip()
    if not out_name:
        print("❌ اسم الإخراج فارغ")
        return

    # كلمة سر داخلية عشوائية (لا سؤال ولا طباعة)
    passphrase_bytes = repr(secrets.token_bytes(64))
    kdf_iters = 200000

    build_dir = make_workdir()
    print("[*] مجلد البناء:", build_dir)

    write_file(os.path.join(build_dir, "setup.py"), textwrap.dedent(SETUP_PY).strip() + "\n")
    pyx = CYTHON_PYX.replace("{PASSPHRASE_BYTES}", passphrase_bytes).replace("{KDF_ITERS}", str(kdf_iters))
    write_file(os.path.join(build_dir, "nasr_ext.pyx"), textwrap.dedent(pyx).strip() + "\n")

    print("[*] بناء Extension (ELF .so) ...")
    rc, out = run([sys.executable, "setup.py", "build_ext", "--inplace"], cwd=build_dir)
    print(out)
    if rc != 0:
        print("❌ فشل البناء.")
        return

    ext_files = [f for f in os.listdir(build_dir) if f.startswith("nasr_ext") and f.endswith(".so")]
    if not ext_files:
        # ويندوز .pyd
        ext_files = [f for f in os.listdir(build_dir) if f.startswith("nasr_ext") and f.endswith(".pyd")]
    if not ext_files:
        print("❌ لم أجد ملف Extension الناتج.")
        return

    ext_file = ext_files[0]
    ext_src = os.path.join(build_dir, ext_file)
    ext_suffix = os.path.splitext(ext_file)[1]  # ".so" أو ".pyd"

    # strip للـ .so لو ممكن
    ok, msg = try_strip(ext_src)
    print(msg)

    # تثبيت .so داخل site-packages على Pydroid (للاستخدام المحلي فقط، مش للهدف)
    if is_pydroid():
        sp = get_writable_sitepackages()
        if not sp:
            print("❌ لم أجد site-packages قابل للكتابة داخل Pydroid.")
            return
        ext_dst = os.path.join(sp, ext_file)
        shutil.copy2(ext_src, ext_dst)
        print("[+] تم تثبيت الإكستنشن داخل:", ext_dst)

    # import extension لاستخدام pack_payload أثناء البناء
    sys.path.insert(0, build_dir)
    import importlib
    nasr_ext = importlib.import_module("nasr_ext")

    with open(file_in, "r", encoding="utf-8") as f:
        src = f.read()

    marshalled = marshal.dumps(compile(src, file_in, "exec"))
    payload = nasr_ext.pack_payload(marshalled)

    # اقرأ ملف .so كـ bytes وحوّله Base64 لدمجه داخل الـ Loader
    with open(ext_src, "rb") as f:
        so_bytes = f.read()
    so_b64 = base64.b64encode(so_bytes).decode("ascii")

    out_abs = os.path.abspath(out_name)
    out_dir = os.path.dirname(out_abs) or os.getcwd()
    os.makedirs(out_dir, exist_ok=True)

    # Loader مع دمج nasr_ext.so كـ Base64 + استخراج مؤقت + حذف فوري
    loader = f"""# -*- coding: utf-8 -*-
import sys, os, base64, tempfile, importlib.util, importlib.machinery

NASR_SO_B64 = {so_b64!r}
PAYLOAD = {payload!r}

def _load_nasr_ext():
    data = base64.b64decode(NASR_SO_B64.encode("ascii"))
    # ملف مؤقت باسم عشوائي + اللاحقة الأصلية (.so / .pyd)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix={ext_suffix!r})
    so_path = tmp.name
    try:
        tmp.write(data)
        tmp.flush()
    finally:
        tmp.close()

    try:
        loader = importlib.machinery.ExtensionFileLoader("nasr_ext", so_path)
        spec = importlib.util.spec_from_loader("nasr_ext", loader)
        mod = importlib.util.module_from_spec(spec)
        loader.exec_module(mod)
        sys.modules["nasr_ext"] = mod
        return mod
    finally:
        # حذف ملف الإكستنشن فورًا بعد التحميل
        try:
            os.remove(so_path)
        except OSError:
            pass

nasr_ext = _load_nasr_ext()
nasr_ext.run_payload(PAYLOAD)
"""

    with open(out_abs, "w", encoding="utf-8") as f:
        f.write(loader)

    # حاول تبني ELF executable runner (اختياري)
    built, info = build_elf_runner(build_dir, payload, out_dir)
    print(info)

    print("\\n✅ الناتج:")
    print(" - Loader محمي (بداخله nasr_ext.so مدموج):", out_abs)
    if built:
        print(" - ELF runner:", os.path.join(out_dir, "nasr_run"))
    print("\\n[*] تشغيل عبر بايثون:")
    print(f"{{sys.executable}} {{out_abs}}")
    if built:
        print("[*] تشغيل ELF runner:")
        print(f"{{os.path.join(out_dir, 'nasr_run')}}")

if __name__ == "__main__":
    main()