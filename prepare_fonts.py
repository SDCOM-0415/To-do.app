"""准备未修改的 HarmonyOS Sans SC 字体和原始授权文件。

可指定本地官方 ZIP；不指定时从华为官方地址下载。
产物始终使用 SHA-256 验证，避免打包错误字体或非官方变体。
"""
from __future__ import annotations

import argparse
import hashlib
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

SOURCE_URL = "https://developer.huawei.com/images/download/general/HarmonyOS-Sans.zip"
FONT_NAME = "HarmonyOS_Sans_SC_Regular.ttf"
FONT_HASH = "297b088424be212207df2ce8b98e335468b782aa6b96832af0b8b773d711e2b1"
ZIP_PREFIX = "HarmonyOS Sans/HarmonyOS_Sans_SC/"
MAX_ZIP_BYTES = 120 * 1024 * 1024


def target_directory(edition: str) -> Path:
    if edition == "tk":
        return Path(__file__).resolve().parent / "res" / "fonts"
    if edition == "flet":
        return Path(__file__).resolve().parent / "assets" / "fonts"
    raise ValueError("edition 必须是 tk 或 flet")


def prepare(edition: str, source: str | None = None) -> Path:
    target = target_directory(edition)
    existing = target / FONT_NAME
    license_file = target / "LICENSE.txt"
    if existing.exists() and license_file.exists():
        if hashlib.sha256(existing.read_bytes()).hexdigest() == FONT_HASH:
            return existing

    if source:
        archive = Path(source).read_bytes()
    else:
        with urllib.request.urlopen(
            urllib.request.Request(SOURCE_URL, headers={"User-Agent": "TodoApp-font-assets/0.3.2"}),
            timeout=90
        ) as response:
            archive = response.read(MAX_ZIP_BYTES + 1)
    if len(archive) > MAX_ZIP_BYTES:
        raise ValueError("字体压缩包过大，已拒绝处理")

    with zipfile.ZipFile(io.BytesIO(archive)) as fonts:
        font_data = fonts.read(ZIP_PREFIX + FONT_NAME)
        license_data = fonts.read(ZIP_PREFIX + "LICENSE.txt")
    if hashlib.sha256(font_data).hexdigest() != FONT_HASH:
        raise ValueError("字体 SHA-256 不匹配，拒绝打包")
    if b"HarmonyOS Sans Fonts License Agreement" not in license_data:
        raise ValueError("授权协议缺失，拒绝打包")
    target.mkdir(parents=True, exist_ok=True)
    existing.write_bytes(font_data)
    license_file.write_bytes(license_data)
    print(f"Font asset ready: {existing} ({len(font_data):,} bytes)")
    return existing


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--edition", choices=("tk", "flet"), required=True)
    parser.add_argument("--zip", help="使用本地 HarmonyOS-Sans.zip")
    args = parser.parse_args()
    try:
        prepare(args.edition, args.zip)
    except Exception as exc:
        print("Font preparation failed: " + str(exc).encode("ascii", "backslashreplace").decode("ascii"), file=sys.stderr)
        raise SystemExit(1)
