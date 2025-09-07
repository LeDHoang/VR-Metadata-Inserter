import os
import shutil
import webbrowser
from typing import Dict, List, Tuple

from flask import Flask, jsonify, request, render_template


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "raw")
FIXED_DIR = os.path.join(BASE_DIR, "fixed_metadata")
CONVENTION_FILE = os.path.join(BASE_DIR, "naming_convention.txt")


def _normalize_section_name(header_line: str) -> str:
    text = header_line.strip().rstrip(":")
    text_upper = text.upper()
    if text_upper.startswith("UNIVERSAL PATTERNS"):
        return "Universal"
    if text_upper.startswith("PLAYA VR") or text_upper.startswith("PLAYA VR SPECIFIC"):
        return "PLAY'A VR"
    if text_upper.startswith("SKYBOX VR"):
        return "Skybox VR Player"
    if text_upper.startswith("PIGASUS"):
        return "Pigasus VR"
    if text_upper.startswith("RAD TV"):
        return "Rad TV"
    if text_upper.startswith("COMMEDIA"):
        return "Commedia"
    if text_upper.startswith("OCULUS"):
        return "Oculus Video App"
    return text


def parse_naming_conventions(file_path: str) -> Dict[str, List[str]]:
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    conventions: Dict[str, List[str]] = {}
    current_section: str = ""

    for line in lines:
        if not line.strip():
            continue

        # Section header ends with ':' in the source file
        if line.strip().endswith(":"):
            current_section = _normalize_section_name(line)
            if current_section not in conventions:
                conventions[current_section] = []
            continue

        if current_section == "":
            continue

        # Expect lines like: "_180_LR = description" or "_3dh, _LR, _SBS = ..."
        if "=" in line:
            left = line.split("=", 1)[0]
            tokens = [t.strip() for t in left.split(",")]
        else:
            tokens = [line.strip()]

        for token in tokens:
            if not token:
                continue
            # keep only patterns that look like filename hints (start with underscore)
            if token.startswith("_") and token not in conventions[current_section]:
                conventions[current_section].append(token)

    # Ensure deterministic ordering
    for key in conventions.keys():
        conventions[key] = sorted(conventions[key], key=lambda s: s.lower())

    return conventions


def list_raw_mp4s() -> List[str]:
    if not os.path.isdir(RAW_DIR):
        return []
    return sorted([f for f in os.listdir(RAW_DIR) if f.lower().endswith(".mp4")])


def build_new_name(original_name: str, pattern: str) -> str:
    name, ext = os.path.splitext(original_name)
    if pattern in name:
        return f"{name}{ext}"
    return f"{name}{pattern}{ext}"


def ensure_dirs() -> None:
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(FIXED_DIR, exist_ok=True)


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/players", methods=["GET"])
def api_players():
    conventions = parse_naming_conventions(CONVENTION_FILE)
    players = sorted(conventions.keys())
    return jsonify({"players": players})


@app.route("/api/conventions", methods=["GET"]) 
def api_conventions():
    player = request.args.get("player", "").strip()
    conventions = parse_naming_conventions(CONVENTION_FILE)
    patterns = conventions.get(player, [])
    return jsonify({"player": player, "patterns": patterns})


@app.route("/api/files", methods=["GET"]) 
def api_files():
    ensure_dirs()
    files = list_raw_mp4s()
    return jsonify({"raw_dir": os.path.relpath(RAW_DIR, BASE_DIR), "files": files})


@app.route("/api/preview", methods=["POST"]) 
def api_preview():
    payload = request.get_json(force=True) or {}
    files: List[str] = payload.get("files", [])
    pattern: str = payload.get("pattern", "")
    mapping: List[Tuple[str, str]] = []
    for f in files:
        mapping.append((f, build_new_name(f, pattern)))
    return jsonify({"preview": [{"original": o, "new": n} for o, n in mapping]})


@app.route("/api/export", methods=["POST"]) 
def api_export():
    ensure_dirs()
    payload = request.get_json(force=True) or {}
    files: List[str] = payload.get("files", [])
    pattern: str = payload.get("pattern", "")

    results = []
    for f in files:
        src = os.path.join(RAW_DIR, f)
        if not os.path.isfile(src):
            results.append({"file": f, "status": "missing"})
            continue
        new_name = build_new_name(f, pattern)
        dst = os.path.join(FIXED_DIR, new_name)
        shutil.copy2(src, dst)
        results.append({"file": f, "copied_to": os.path.relpath(dst, BASE_DIR), "status": "ok"})

    return jsonify({"results": results})


def open_browser(port: int) -> None:
    try:
        webbrowser.open_new(f"http://127.0.0.1:{port}")
    except Exception:
        pass


if __name__ == "__main__":
    ensure_dirs()
    port = int(os.environ.get("PORT", "5001"))
    open_browser(port)
    app.run(host="127.0.0.1", port=port, debug=False)


