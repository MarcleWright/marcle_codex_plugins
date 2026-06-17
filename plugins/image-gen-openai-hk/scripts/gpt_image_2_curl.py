#!/usr/bin/env python
"""Curl-compatible gpt-image-2 wrapper for the local Codex plugin.

Text-to-image:
  python gpt_image_2_curl.py "a white siamese cat"

Image edit:
  python gpt_image_2_curl.py "make a product poster" --image ref1.png --image ref2.png

Requires OPENAI_HK_IMAGE_KEY, openai-hk_image_key, or a local .env file on each device.
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import shlex
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Iterable

DEFAULT_API_BASE = "https://api.openai-hk.com"
PLUGIN_NAME = "image-gen-openai-hk"
ENV_KEYS = ("OPENAI_HK_IMAGE_KEY", "openai-hk_image_key")


def plugin_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip().lstrip("\ufeff")
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_env_files() -> None:
    load_env_file(plugin_root() / ".env")
    load_env_file(Path.home() / ".image-gen-openai-hk.env")


def load_api_key() -> str:
    load_env_files()
    for key_name in ENV_KEYS:
        value = os.getenv(key_name)
        if value:
            return value
    raise RuntimeError(
        "No image API key is set. Add openai-hk_image_key=your_key to "
        f"{plugin_root() / '.env'}, add it to {Path.home() / '.image-gen-openai-hk.env'}, "
        "or set OPENAI_HK_IMAGE_KEY."
    )


def default_output_dir() -> Path:
    project_name = safe_path_segment(Path.cwd().name or "workspace")
    return Path.home() / "Pictures" / "codex-generated" / PLUGIN_NAME / project_name


def safe_path_segment(text: str) -> str:
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "-", text).strip(" .-")
    return text[:80] or "workspace"


def safe_name(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9_.-]+", "-", text).strip("-")
    return text[:80] or "image"


def request_json(url: str, api_key: str, payload: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=240) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"OpenAI-HK API error HTTP {exc.code}: {body}") from exc


def multipart_body(fields: dict[str, str], files: Iterable[tuple[str, Path]]) -> tuple[bytes, str]:
    boundary = "----CodexOpenAIHK" + uuid.uuid4().hex
    chunks: list[bytes] = []

    def add(data: str | bytes) -> None:
        chunks.append(data.encode("utf-8") if isinstance(data, str) else data)

    for name, value in fields.items():
        add(f"--{boundary}\r\n")
        add(f'Content-Disposition: form-data; name="{name}"\r\n\r\n')
        add(str(value))
        add("\r\n")

    for field_name, path in files:
        content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        add(f"--{boundary}\r\n")
        add(
            f'Content-Disposition: form-data; name="{field_name}"; filename="{path.name}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        )
        chunks.append(path.read_bytes())
        add("\r\n")

    add(f"--{boundary}--\r\n")
    return b"".join(chunks), boundary


def request_multipart(url: str, api_key: str, fields: dict[str, str], image_paths: list[Path]) -> dict:
    files = [("image[]", path) for path in image_paths]
    body, boundary = multipart_body(fields, files)
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=240) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"OpenAI-HK API error HTTP {exc.code}: {body_text}") from exc


def save_b64_image(b64_text: str, output_dir: Path, model: str, index: int) -> Path:
    if "," in b64_text and b64_text.lower().startswith("data:image"):
        b64_text = b64_text.split(",", 1)[1]
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    out = output_dir / f"openai-hk_{safe_name(model)}_{ts}_{index}.png"
    out.write_bytes(base64.b64decode(b64_text))
    return out


def download_url_image(url: str, output_dir: Path, model: str, index: int) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    suffix = Path(urllib.parse.urlparse(url).path).suffix or ".png"
    out = output_dir / f"openai-hk_{safe_name(model)}_{ts}_{index}{suffix}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Referer": "https://api.openai-hk.com/",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=240) as resp:
        out.write_bytes(resp.read())
    return out


def save_response_images(result: dict, output_dir: Path, model: str, download_url: bool) -> list[Path]:
    saved: list[Path] = []
    for index, item in enumerate(result.get("data") or [], start=1):
        if item.get("b64_json"):
            saved.append(save_b64_image(item["b64_json"], output_dir, model, index))
        elif item.get("url") and download_url:
            saved.append(download_url_image(item["url"], output_dir, model, index))
    return saved


SIZE_BY_RATIO_AND_K = {
    ("1:1", "1k"): "1024x1024",
    ("1:1", "2k"): "2048x2048",
    ("1:1", "4k"): "2880x2880",
    ("16:9", "1k"): "1280x720",
    ("16:9", "2k"): "2048x1152",
    ("16:9", "4k"): "3840x2160",
    ("9:16", "1k"): "720x1280",
    ("9:16", "2k"): "1152x2048",
    ("9:16", "4k"): "2160x3840",
    ("5:4", "1k"): "1040x832",
    ("5:4", "2k"): "2080x1664",
    ("5:4", "4k"): "3200x2560",
    ("4:5", "1k"): "832x1040",
    ("4:5", "2k"): "1664x2080",
    ("4:5", "4k"): "2560x3200",
    ("4:3", "1k"): "1024x768",
    ("4:3", "2k"): "2048x1536",
    ("4:3", "4k"): "3264x2448",
    ("3:4", "1k"): "768x1024",
    ("3:4", "2k"): "1536x2048",
    ("3:4", "4k"): "2448x3264",
    ("3:2", "1k"): "1008x672",
    ("3:2", "2k"): "2064x1376",
    ("3:2", "4k"): "3504x2336",
    ("2:3", "1k"): "672x1008",
    ("2:3", "2k"): "1376x2064",
    ("2:3", "4k"): "2336x3504",
    ("21:9", "1k"): "1344x576",
    ("21:9", "2k"): "2016x864",
    ("21:9", "4k"): "3808x1632",
}

RATIO_ALIASES = {
    "square": "1:1",
    "widescreen": "16:9",
    "story": "9:16",
    "print": "5:4",
    "feed": "4:5",
    "classic": "4:3",
    "vertical": "3:4",
    "photo": "3:2",
    "portrait": "2:3",
    "exclusive": "21:9",
}


def normalize_ratio(value: str) -> str:
    value = value.strip().lower().replace("：", ":").replace("×", "x")
    value = RATIO_ALIASES.get(value, value)
    if re.fullmatch(r"\d+\s*[:x/]\s*\d+", value):
        left, right = re.split(r"[:x/]", value)
        return f"{int(left)}:{int(right)}"
    return value


def normalize_k(value: str) -> str:
    value = value.strip().lower().replace(" ", "")
    if value in {"1", "2", "4"}:
        return value + "k"
    return value


def size_from_ratio_k(ratio: str | None, k: str | None) -> str | None:
    if not ratio and not k:
        return None
    if not ratio or not k:
        raise ValueError("Both --ratio and --k are required when using ratio/K auto sizing.")
    key = (normalize_ratio(ratio), normalize_k(k))
    if key not in SIZE_BY_RATIO_AND_K:
        supported = ", ".join(f"{r} {kk}" for r, kk in sorted(SIZE_BY_RATIO_AND_K))
        raise ValueError(f"Unsupported ratio/K combination: {ratio} {k}. Supported: {supported}")
    return SIZE_BY_RATIO_AND_K[key]


def resolve_size(size: str, ratio: str | None, k: str | None) -> str:
    resolved = size_from_ratio_k(ratio, k)
    return resolved or size


def quote_for_curl(value: str) -> str:
    if os.name == "nt":
        return '"' + value.replace('"', '\\"') + '"'
    return shlex.quote(value)


def redacted_curl(args: argparse.Namespace, resolved_size: str, image_paths: list[Path]) -> str:
    api_base = args.api_base.rstrip("/")
    auth_header = "Authorization: Bearer ${env:OPENAI_HK_IMAGE_KEY}"
    if image_paths:
        parts = [
            "curl.exe -X POST " + quote_for_curl(f"{api_base}/v1/images/edits"),
            "  -H " + quote_for_curl(auth_header),
            "  -F " + quote_for_curl(f"model={args.model}"),
            "  -F " + quote_for_curl(f"prompt={args.prompt}"),
            "  -F " + quote_for_curl(f"n={args.n}"),
            "  -F " + quote_for_curl(f"size={resolved_size}"),
            "  -F " + quote_for_curl(f"quality={args.quality}"),
            "  -F " + quote_for_curl(f"response_format={args.response_format}"),
        ]
        parts.extend("  -F " + quote_for_curl(f"image[]=@{path}") for path in image_paths)
    else:
        payload = {
            "model": args.model,
            "prompt": args.prompt,
            "n": args.n,
            "size": resolved_size,
            "quality": args.quality,
            "response_format": args.response_format,
        }
        parts = [
            "curl.exe -X POST " + quote_for_curl(f"{api_base}/v1/images/generations"),
            "  -H " + quote_for_curl(auth_header),
            "  -H " + quote_for_curl("Content-Type: application/json"),
            "  -d " + quote_for_curl(json.dumps(payload, ensure_ascii=False, separators=(",", ":"))),
        ]
    return " `\n".join(parts)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate/edit images using the gpt-image-2 OpenAI-HK API.")
    parser.add_argument("prompt", help="Image prompt")
    parser.add_argument("--model", default="gpt-image-2", help="Model: gpt-image-2, gpt-image-1, gpt-image-1.5")
    parser.add_argument("--api-base", default=DEFAULT_API_BASE, help="API base URL")
    parser.add_argument("--size", default="1024x1024", help="Image size, e.g. 1024x1024 or 2048x1152")
    parser.add_argument("--ratio", help="Optional aspect ratio for auto size lookup, e.g. 16:9, 9:16, 1:1")
    parser.add_argument("--k", help="Optional resolution tier for auto size lookup: 1K, 2K, or 4K")
    parser.add_argument("--quality", default="medium", help="Quality: low, medium, high, auto")
    parser.add_argument("--n", type=int, default=1, help="Number of images")
    parser.add_argument("--response-format", default="url", choices=["url", "b64_json"], help="API response format")
    parser.add_argument("--output", default=str(default_output_dir()), help="Output directory")
    parser.add_argument("--image", action="append", default=[], help="Reference image path for /v1/images/edits. Repeatable.")
    parser.add_argument("--no-download-url", action="store_true", help="Do not download returned image URLs; only print them.")
    parser.add_argument("--show-curl", action="store_true", help="Print a redacted curl command and exit without calling the API.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        output_dir = Path(args.output).expanduser()
        resolved_size = resolve_size(args.size, args.ratio, args.k)
        image_paths = [Path(path).expanduser() for path in args.image]
        for path in image_paths:
            if not path.exists():
                raise RuntimeError(f"Reference image not found: {path}")

        if args.show_curl:
            print(redacted_curl(args, resolved_size, image_paths))
            return 0

        api_key = load_api_key()
        api_base = args.api_base.rstrip("/")

        if image_paths:
            fields = {
                "model": args.model,
                "prompt": args.prompt,
                "n": str(args.n),
                "size": resolved_size,
                "quality": args.quality,
                "response_format": args.response_format,
            }
            result = request_multipart(f"{api_base}/v1/images/edits", api_key, fields, image_paths)
            mode = "edit"
        else:
            payload = {
                "model": args.model,
                "prompt": args.prompt,
                "n": args.n,
                "size": resolved_size,
                "quality": args.quality,
                "response_format": args.response_format,
            }
            result = request_json(f"{api_base}/v1/images/generations", api_key, payload)
            mode = "generation"

        saved = save_response_images(result, output_dir, args.model, download_url=not args.no_download_url)
        urls = [item.get("url") for item in (result.get("data") or []) if item.get("url")]
        print(json.dumps({
            "success": True,
            "mode": mode,
            "model": args.model,
            "size": resolved_size,
            "quality": args.quality,
            "paths": [str(path) for path in saved],
            "urls": urls,
            "usage": result.get("usage"),
        }, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
